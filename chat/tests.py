from asgiref.sync import async_to_sync

from channels.routing import URLRouter

from channels.testing import WebsocketCommunicator

from django.contrib.auth.models import User

from django.test import TestCase, TransactionTestCase

from django.urls import re_path, reverse


from .consumers import CallNotificationConsumer, ChatConsumer

from .models import ChatGroup, ChatMessage, GroupInvite, Notification

from .views import mark_group_notifications_read


class DeleteGroupTests(TestCase):


    def setUp(self):


        self.owner = User.objects.create_user(username='owner', password='password')


        self.member = User.objects.create_user(username='member', password='password')


        self.group = ChatGroup.objects.create(name='Test group', created_by=self.owner)


        self.group.members.add(self.owner, self.member)


        self.message = ChatMessage.objects.create(


            group=self.group,


            author=self.owner,


            content='Hello',


        )


        GroupInvite.objects.create(group=self.group, token='test-token', created_by=self.owner)


        Notification.objects.create(


            recipient=self.member,


            group=self.group,


            message=self.message,


        )


        self.delete_url = reverse('delete_group', args=[self.group.id])


    def test_owner_can_delete_group_for_every_member(self):


        self.client.force_login(self.owner)


        response = self.client.post(self.delete_url)


        self.assertRedirects(response, reverse('chat_list'))


        self.assertFalse(ChatGroup.objects.filter(id=self.group.id).exists())


        self.assertFalse(self.owner.chat_groups.filter(id=self.group.id).exists())


        self.assertFalse(self.member.chat_groups.filter(id=self.group.id).exists())


        self.assertFalse(ChatMessage.objects.filter(id=self.message.id).exists())


        self.assertFalse(GroupInvite.objects.filter(group_id=self.group.id).exists())


        self.assertFalse(Notification.objects.filter(group_id=self.group.id).exists())


    def test_non_owner_cannot_delete_group(self):


        self.client.force_login(self.member)


        response = self.client.post(self.delete_url)


        self.assertEqual(response.status_code, 403)


        self.assertTrue(ChatGroup.objects.filter(id=self.group.id).exists())


    def test_delete_group_rejects_get_requests(self):


        self.client.force_login(self.owner)


        response = self.client.get(self.delete_url)


        self.assertEqual(response.status_code, 405)


        self.assertTrue(ChatGroup.objects.filter(id=self.group.id).exists())


class ChatRoomReplyStateTests(TestCase):


    def setUp(self):


        self.user = User.objects.create_user(username='sender', password='password')


        self.group = ChatGroup.objects.create(name='Reply test', created_by=self.user)


        self.group.members.add(self.user)


    def test_successful_send_clears_reply_state(self):


        self.client.force_login(self.user)


        response = self.client.get(reverse('chat_room', args=[self.group.id]))


        self.assertContains(response, 'messageForm.reset();')


        self.assertContains(response, 'cancelReply();')


    def test_reply_is_saved_and_returned_to_realtime_client(self):


        parent = ChatMessage.objects.create(
            group=self.group,
            author=self.user,
            content='Original message',
        )


        self.client.force_login(self.user)


        response = self.client.post(
            reverse('chat_room', args=[self.group.id]),
            {
                'content': 'Reply message',
                'parent_id': parent.id,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )


        self.assertEqual(response.status_code, 200)


        reply = ChatMessage.objects.get(content='Reply message')


        self.assertEqual(reply.parent, parent)


        self.assertEqual(response.json()['message']['parent_id'], parent.id)


        self.assertEqual(
            response.json()['message']['parent_content'],
            'Original message',
        )


    def test_reply_to_message_from_another_group_is_rejected(self):


        other_group = ChatGroup.objects.create(
            name='Other group',
            created_by=self.user,
        )


        other_group.members.add(self.user)


        foreign_message = ChatMessage.objects.create(
            group=other_group,
            author=self.user,
            content='Not in this room',
        )


        self.client.force_login(self.user)


        response = self.client.post(
            reverse('chat_room', args=[self.group.id]),
            {
                'content': 'Invalid reply',
                'parent_id': foreign_message.id,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )


        self.assertEqual(response.status_code, 400)


        self.assertFalse(
            ChatMessage.objects.filter(content='Invalid reply').exists()
        )


class PrivateGroupInviteTests(TestCase):


    def setUp(self):


        self.owner = User.objects.create_user(username='invite-owner', password='password')


        self.guest = User.objects.create_user(username='invite-guest', password='password')


        self.group = ChatGroup.objects.create(
            name='Private group',
            created_by=self.owner,
            is_private=True,
        )


        self.group.members.add(self.owner)


    def test_private_group_member_can_create_and_share_invite_link(self):


        self.client.force_login(self.owner)


        response = self.client.post(
            reverse('chat_room', args=[self.group.id]),
            {'generate_invite': '1'},
        )


        invite = GroupInvite.objects.get(group=self.group)


        self.assertContains(response, reverse('join_group_via_link', args=[invite.token]))


        self.client.force_login(self.guest)


        response = self.client.get(reverse('join_group_via_link', args=[invite.token]))


        self.assertRedirects(response, reverse('chat_room', args=[self.group.id]))


        self.assertTrue(self.group.members.filter(id=self.guest.id).exists())


    def test_direct_message_does_not_offer_or_create_invite_link(self):


        direct_chat = ChatGroup.objects.create(
            name='Private invite-owner-invite-guest',
            created_by=self.owner,
            is_private=True,
            is_direct_message=True,
        )


        direct_chat.members.add(self.owner, self.guest)


        self.client.force_login(self.owner)


        response = self.client.get(reverse('chat_room', args=[direct_chat.id]))


        self.assertNotContains(response, 'title="ساخت لینک دعوت"')


        response = self.client.post(reverse('create_invite_link', args=[direct_chat.id]))


        self.assertEqual(response.status_code, 403)


        self.assertFalse(GroupInvite.objects.filter(group=direct_chat).exists())


class RealtimeReadReceiptTests(TestCase):


    def setUp(self):


        self.sender = User.objects.create_user(username='read-sender', password='password')


        self.reader = User.objects.create_user(username='read-reader', password='password')


        self.group = ChatGroup.objects.create(name='Read receipt', created_by=self.sender)


        self.group.members.add(self.sender, self.reader)


        self.message = ChatMessage.objects.create(
            group=self.group,
            author=self.sender,
            content='Read me',
        )


        self.notification = Notification.objects.create(
            recipient=self.reader,
            group=self.group,
            message=self.message,
        )


    def test_marking_group_read_returns_realtime_receipt(self):


        receipts = mark_group_notifications_read(self.reader, self.group)


        self.notification.refresh_from_db()


        self.assertTrue(self.notification.is_read)


        self.assertEqual(
            receipts,
            [{'message_id': self.message.id, 'read_status': 'خوانده شده'}],
        )


    def test_chat_page_contains_realtime_read_receipt_client(self):


        self.client.force_login(self.sender)


        response = self.client.get(reverse('chat_room', args=[self.group.id]))


        self.assertContains(response, "data.type === 'read_receipt'")


        self.assertContains(response, "sendReadReceipt([data.message.id])")


        self.assertContains(response, "document.visibilityState !== 'visible'")


class AudioCallPageTests(TestCase):


    def setUp(self):


        self.caller = User.objects.create_user(
            username='audio-caller',
            password='password',
        )


        self.recipient = User.objects.create_user(
            username='audio-recipient',
            password='password',
        )


    def test_direct_message_contains_audio_call_client(self):


        direct_chat = ChatGroup.objects.create(
            name='Audio call',
            created_by=self.caller,
            is_private=True,
            is_direct_message=True,
        )


        direct_chat.members.add(self.caller, self.recipient)


        self.client.force_login(self.caller)


        response = self.client.get(reverse('chat_room', args=[direct_chat.id]))


        self.assertContains(response, 'id="start-call-btn"')


        self.assertContains(response, 'video: false')


        self.assertContains(response, "sendCallSignal('call_offer'")


        self.assertNotContains(response, 'createPeerConnection(pendingCallOffer.username)')


    def test_group_chat_contains_audio_call_button(self):


        group = ChatGroup.objects.create(
            name='Group calls',
            created_by=self.caller,
        )


        group.members.add(self.caller, self.recipient)


        self.client.force_login(self.caller)


        response = self.client.get(reverse('chat_room', args=[group.id]))


        self.assertContains(response, 'id="start-call-btn"')


        self.assertContains(response, 'id="call-modal"')


    def test_chat_list_does_not_show_group_call_entry(self):


        group = ChatGroup.objects.create(
            name='Group list calls',
            created_by=self.caller,
        )


        group.members.add(self.caller, self.recipient)


        self.client.force_login(self.caller)


        response = self.client.get(reverse('chat_list'))


        self.assertContains(response, f'/chat/room/{group.id}/')


        self.assertNotContains(response, f'/chat/room/{group.id}/?call=1')


    def test_join_public_group_can_redirect_to_call(self):


        group = ChatGroup.objects.create(
            name='Join and call',
            created_by=self.caller,
            is_private=False,
        )


        self.client.force_login(self.recipient)


        response = self.client.post(
            reverse('join_public_group', args=[group.id]),
            {'call': '1'},
        )


        self.assertRedirects(
            response,
            f'/chat/room/{group.id}/?call=1',
            fetch_redirect_response=False,
        )


        self.assertTrue(group.members.filter(id=self.recipient.id).exists())


    def test_channel_chat_contains_audio_call_button(self):


        channel = ChatGroup.objects.create(
            name='Channel calls',
            created_by=self.caller,
            group_type=ChatGroup.GROUP_TYPE_CHANNEL,
        )


        channel.members.add(self.caller, self.recipient)


        self.client.force_login(self.caller)


        response = self.client.get(reverse('chat_room', args=[channel.id]))


        self.assertContains(response, 'id="start-call-btn"')


    def test_authenticated_pages_include_global_call_listener(self):


        self.client.force_login(self.recipient)


        response = self.client.get(reverse('chat_list'))


        self.assertContains(response, 'id="global-call-modal"')


        self.assertContains(response, '/ws/calls/')


        self.assertContains(response, 'acceptGlobalIncomingCall')


class AudioCallSignalingTests(TransactionTestCase):


    def setUp(self):


        self.caller = User.objects.create_user(
            username='signal-caller',
            password='password',
        )


        self.recipient = User.objects.create_user(
            username='signal-recipient',
            password='password',
        )


        self.group = ChatGroup.objects.create(
            name='Signaling',
            created_by=self.caller,
            is_private=True,
            is_direct_message=True,
        )


        self.group.members.add(self.caller, self.recipient)


    def test_offer_is_relayed_to_group_members(self):


        async_to_sync(self._run_offer_relay)()


    async def _run_offer_relay(self):


        application = URLRouter([
            re_path(
                r'ws/calls/$',
                CallNotificationConsumer.as_asgi(),
            ),
            re_path(
                r'ws/chat/(?P<group_id>\d+)/$',
                ChatConsumer.as_asgi(),
            ),
        ])


        caller_socket = WebsocketCommunicator(
            application,
            f'/ws/chat/{self.group.id}/',
        )


        recipient_socket = WebsocketCommunicator(
            application,
            f'/ws/chat/{self.group.id}/',
        )


        global_socket = WebsocketCommunicator(
            application,
            '/ws/calls/',
        )


        caller_socket.scope['user'] = self.caller


        recipient_socket.scope['user'] = self.recipient


        global_socket.scope['user'] = self.recipient


        self.assertTrue((await caller_socket.connect())[0])


        self.assertTrue((await recipient_socket.connect())[0])


        self.assertTrue((await global_socket.connect())[0])


        await caller_socket.send_json_to({
            'type': 'call_offer',
            'call_id': 'test-call',
            'payload': {'type': 'offer', 'sdp': 'test-sdp'},
        })


        signal = await recipient_socket.receive_json_from()


        self.assertEqual(signal['type'], 'call_offer')


        self.assertEqual(signal['call_id'], 'test-call')


        self.assertEqual(signal['username'], self.caller.username)


        global_signal = await global_socket.receive_json_from()


        self.assertEqual(global_signal['type'], 'incoming_call')


        self.assertEqual(global_signal['group_id'], self.group.id)


        self.assertEqual(global_signal['call_id'], 'test-call')


        self.assertEqual(
            global_signal['room_url'],
            f'/chat/room/{self.group.id}/',
        )


        self.assertTrue(await caller_socket.receive_nothing(timeout=0.1))


        await caller_socket.disconnect()


        await recipient_socket.disconnect()


        await global_socket.disconnect()


    def test_group_offer_is_relayed_to_other_members(self):


        async_to_sync(self._run_group_offer_relay)()


    async def _run_group_offer_relay(self):


        third_member = await User.objects.acreate(
            username='signal-third',
            password='password',
        )


        group = await ChatGroup.objects.acreate(
            name='Group signaling',
            created_by=self.caller,
        )


        await group.members.aadd(self.caller, self.recipient, third_member)


        application = URLRouter([
            re_path(
                r'ws/calls/$',
                CallNotificationConsumer.as_asgi(),
            ),
            re_path(
                r'ws/chat/(?P<group_id>\d+)/$',
                ChatConsumer.as_asgi(),
            ),
        ])


        caller_socket = WebsocketCommunicator(
            application,
            f'/ws/chat/{group.id}/',
        )


        recipient_socket = WebsocketCommunicator(
            application,
            f'/ws/chat/{group.id}/',
        )


        global_socket = WebsocketCommunicator(
            application,
            '/ws/calls/',
        )


        caller_socket.scope['user'] = self.caller


        recipient_socket.scope['user'] = self.recipient


        global_socket.scope['user'] = third_member


        self.assertTrue((await caller_socket.connect())[0])


        self.assertTrue((await recipient_socket.connect())[0])


        self.assertTrue((await global_socket.connect())[0])


        await caller_socket.send_json_to({
            'type': 'call_offer',
            'call_id': 'group-call',
            'payload': {'type': 'offer', 'sdp': 'test-sdp'},
        })


        signal = await recipient_socket.receive_json_from()


        self.assertEqual(signal['type'], 'call_offer')


        self.assertEqual(signal['call_id'], 'group-call')


        global_signal = await global_socket.receive_json_from()


        self.assertEqual(global_signal['type'], 'incoming_call')


        self.assertEqual(global_signal['group_id'], group.id)


        self.assertFalse(global_signal['is_direct_message'])


        await recipient_socket.send_json_to({
            'type': 'call_join',
            'call_id': 'group-call',
            'target_username': self.caller.username,
        })


        join_signal = await caller_socket.receive_json_from()


        self.assertEqual(join_signal['type'], 'call_join')


        self.assertEqual(join_signal['call_id'], 'group-call')


        self.assertEqual(join_signal['username'], self.recipient.username)


        self.assertEqual(join_signal['target_username'], self.caller.username)


        await caller_socket.send_json_to({
            'type': 'call_offer',
            'call_id': 'group-call',
            'payload': {'type': 'offer', 'sdp': 'targeted-sdp'},
            'target_username': self.recipient.username,
        })


        targeted_signal = await recipient_socket.receive_json_from()


        self.assertEqual(targeted_signal['type'], 'call_offer')


        self.assertEqual(
            targeted_signal['target_username'],
            self.recipient.username,
        )


        self.assertTrue(await global_socket.receive_nothing(timeout=0.1))


        self.assertTrue(await caller_socket.receive_nothing(timeout=0.1))


        await caller_socket.disconnect()


        await recipient_socket.disconnect()


        await global_socket.disconnect()

