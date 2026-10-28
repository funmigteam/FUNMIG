import json


from channels.db import database_sync_to_async

from channels.generic.websocket import AsyncJsonWebsocketConsumer


from .models import ChatGroup, ChatMessage, Notification


class ChatConsumer(AsyncJsonWebsocketConsumer):

    CALL_SIGNAL_TYPES = {
        'call_offer',
        'call_answer',
        'call_ice_candidate',
        'call_join',
        'call_reject',
        'call_hangup',
        'call_busy',
    }


    async def connect(self):

        self.group_id = self.scope['url_route']['kwargs']['group_id']

        self.room_group_name = f'chat_{self.group_id}'

        self.user = self.scope['user']


        if self.user.is_anonymous:

            await self.close()

            return


        self.chat_group = await self.get_group()

        if not self.chat_group or not await self.is_member():

            await self.close()

            return


        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )


    async def receive_json(self, content, **kwargs):

        message_type = content.get('type')


        if message_type == 'typing':

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_message',
                    'username': self.user.username,
                    'typing': bool(content.get('typing', False)),
                },
            )

        elif message_type == 'read':

            receipts = await self.mark_messages_read(content.get('message_ids'))

            if receipts:

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'read_receipt',
                        'receipts': receipts,
                    },
                )

        elif message_type in self.CALL_SIGNAL_TYPES:

            await self.relay_call_signal(message_type, content)


    async def relay_call_signal(self, message_type, content):

        call_id = content.get('call_id')

        if not isinstance(call_id, str) or not call_id or len(call_id) > 100:

            return


        payload = content.get('payload')

        if payload is not None:

            try:

                if len(json.dumps(payload)) > 65536:

                    return

            except (TypeError, ValueError):

                return


        target_username = content.get('target_username')

        if target_username is not None and (
            not isinstance(target_username, str) or len(target_username) > 150
        ):

            return


        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_signal',
                'signal_type': message_type,
                'call_id': call_id,
                'payload': payload,
                'target_username': target_username,
                'username': self.user.username,
                'sender_channel': self.channel_name,
            },
        )


        if message_type in {
            'call_offer',
            'call_reject',
            'call_hangup',
            'call_busy',
        } and not target_username:

            recipient_ids = await self.get_other_member_ids()

            notification_type = (
                'incoming_call'
                if message_type == 'call_offer'
                else 'call_status'
            )

            for recipient_id in recipient_ids:

                await self.channel_layer.group_send(
                    f'user_calls_{recipient_id}',
                    {
                        'type': notification_type,
                        'signal_type': message_type,
                        'group_id': self.chat_group.id,
                        'call_id': call_id,
                        'payload': payload,
                        'username': self.user.username,
                        'is_direct_message': self.chat_group.is_direct_message,
                    },
                )

    async def chat_message(self, event):

        await self.send_json({
            'type': 'message',
            'message': event['message'],
        })


    async def typing_message(self, event):

        await self.send_json({
            'type': 'typing',
            'username': event['username'],
            'typing': event['typing'],
        })


    async def read_receipt(self, event):

        await self.send_json({
            'type': 'read_receipt',
            'receipts': event['receipts'],
        })


    async def call_signal(self, event):

        if event.get('sender_channel') == self.channel_name:

            return


        await self.send_json({
            'type': event['signal_type'],
            'call_id': event['call_id'],
            'payload': event.get('payload'),
            'target_username': event.get('target_username'),
            'username': event['username'],
        })


    async def group_deleted(self, event):

        await self.send_json({
            'type': 'group_deleted',
            'group_id': event['group_id'],
        })

        await self.close()


    @database_sync_to_async

    def get_group(self):

        try:

            return ChatGroup.objects.get(id=self.group_id)

        except ChatGroup.DoesNotExist:

            return None


    @database_sync_to_async

    def is_member(self):

        return self.chat_group.members.filter(id=self.user.id).exists()


    @database_sync_to_async

    def get_other_member_ids(self):

        return list(
            self.chat_group.members.exclude(id=self.user.id)
            .values_list('id', flat=True)
        )


    @database_sync_to_async

    def mark_messages_read(self, message_ids=None):

        notifications = Notification.objects.filter(
            recipient=self.user,
            group=self.chat_group,
            is_read=False,
        )


        if message_ids:

            notifications = notifications.filter(message_id__in=message_ids)


        unread_notifications = list(
            notifications.values_list('id', 'message_id')
        )

        if not unread_notifications:

            return []


        notification_ids = [
            notification_id
            for notification_id, _ in unread_notifications
        ]

        affected_message_ids = list({
            message_id
            for _, message_id in unread_notifications
        })


        Notification.objects.filter(id__in=notification_ids).update(is_read=True)


        return [
            {
                'message_id': message.id,
                'read_status': message.read_status_text,
            }
            for message in ChatMessage.objects.filter(
                id__in=affected_message_ids,
                group=self.chat_group,
            )
        ]


class CallNotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = self.scope['user']

        if self.user.is_anonymous:

            await self.close()

            return


        self.user_group_name = f'user_calls_{self.user.id}'

        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name,
        )

        await self.accept()


    async def disconnect(self, close_code):

        if hasattr(self, 'user_group_name'):

            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name,
            )


    async def receive_json(self, content, **kwargs):

        signal_type = content.get('type')

        if signal_type not in {'call_reject', 'call_busy', 'call_claimed'}:

            return


        group_id = content.get('group_id')

        call_id = content.get('call_id')

        if (
            not isinstance(group_id, int)
            or not isinstance(call_id, str)
            or not call_id
            or len(call_id) > 100
        ):

            return


        chat_group = await self.get_chat_group(group_id)

        if not chat_group:

            return


        if signal_type != 'call_claimed' and (
            signal_type != 'call_reject' or chat_group.is_direct_message
        ):

            await self.channel_layer.group_send(
                f'chat_{group_id}',
                {
                    'type': 'call_signal',
                    'signal_type': signal_type,
                    'call_id': call_id,
                    'payload': None,
                    'username': self.user.username,
                    'sender_channel': self.channel_name,
                },
            )


        for member_id in await self.get_member_ids(chat_group):

            await self.channel_layer.group_send(
                f'user_calls_{member_id}',
                    {
                        'type': 'call_status',
                        'signal_type': signal_type,
                        'group_id': group_id,
                        'call_id': call_id,
                        'payload': None,
                        'username': self.user.username,
                        'is_direct_message': chat_group.is_direct_message,
                    },
                )


    async def incoming_call(self, event):

        await self.send_json({
            'type': 'incoming_call',
            'signal_type': event['signal_type'],
            'group_id': event['group_id'],
            'call_id': event['call_id'],
            'payload': event.get('payload'),
            'username': event['username'],
            'is_direct_message': event.get('is_direct_message', False),
            'room_url': f"/chat/room/{event['group_id']}/",
        })


    async def call_status(self, event):

        await self.send_json({
            'type': 'call_status',
            'signal_type': event['signal_type'],
            'group_id': event['group_id'],
            'call_id': event['call_id'],
            'username': event['username'],
            'is_direct_message': event.get('is_direct_message', False),
        })


    @database_sync_to_async

    def get_chat_group(self, group_id):

        try:

            return ChatGroup.objects.get(
                id=group_id,
                members=self.user,
            )

        except ChatGroup.DoesNotExist:

            return None


    @database_sync_to_async

    def get_member_ids(self, chat_group):

        return list(chat_group.members.values_list('id', flat=True))

