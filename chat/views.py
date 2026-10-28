from django.shortcuts import render, redirect, get_object_or_404


from django.conf import settings

from django.contrib.auth.decorators import login_required


from django.contrib.auth.models import User


from django.core.cache import cache


from .models import ChatGroup, ChatMessage, GroupInvite, Notification


from .forms import CreateGroupForm, InviteUserForm


from asgiref.sync import async_to_sync


from channels.layers import get_channel_layer


import secrets


from django.http import JsonResponse

from django.views.decorators.http import require_POST


def reply_preview(message):


    if not message:


        return None


    if message.content:


        content = message.content.strip()


        return content[:50] + ('...' if len(content) > 50 else '')


    return {


        'image': 'تصویر',


        'audio': 'پیام صوتی',


        'video': 'ویدیو',


        'file': 'فایل',


    }.get(message.file_type, 'پیام')


def broadcast_chat_message(msg):


    channel_layer = get_channel_layer()


    if channel_layer:


        async_to_sync(channel_layer.group_send)(


            f'chat_{msg.group.id}',


            {


                'type': 'chat_message',


                'message': {


                    'id': msg.id,


                    'author_username': msg.author.username,


                    'content': msg.content,


                    'time': msg.created_at.strftime("%H:%M"),


                    'is_me': False,


                    'file_url': msg.file.url if msg.file else None,


                    'file_name': msg.file.name.split('/')[-1] if msg.file else None,


                    'file_type': msg.file_type if msg.file else None,


                    'parent_id': msg.parent_id,


                    'parent_author': msg.parent.author.username if msg.parent else None,


                    'parent_content': reply_preview(msg.parent),


                    'read_status': msg.read_status_text,


                    'read_by_count': msg.read_by_count,


                    'recipient_count': msg.recipient_count,


                }


            }


        )


def mark_group_notifications_read(user, group):


    unread_notifications = list(
        Notification.objects.filter(
            recipient=user,
            group=group,
            is_read=False,
        ).values_list('id', 'message_id')
    )


    if not unread_notifications:


        return []


    notification_ids = [notification_id for notification_id, _ in unread_notifications]

    message_ids = list({message_id for _, message_id in unread_notifications})


    Notification.objects.filter(id__in=notification_ids).update(is_read=True)


    receipts = []


    for message in ChatMessage.objects.filter(id__in=message_ids, group=group):


        receipts.append({
            'message_id': message.id,
            'read_status': message.read_status_text,
        })


    channel_layer = get_channel_layer()


    if channel_layer and receipts:


        async_to_sync(channel_layer.group_send)(
            f'chat_{group.id}',
            {
                'type': 'read_receipt',
                'receipts': receipts,
            }
        )


    return receipts


@login_required


def chat_list(request):


    groups = request.user.chat_groups.prefetch_related('members').all()


    unread_counts = {}


    for note in Notification.objects.filter(recipient=request.user, is_read=False).select_related('group'):


        unread_counts[note.group_id] = unread_counts.get(note.group_id, 0) + 1


    for group in groups:


        group.last_message = group.messages.order_by('-created_at').select_related('author').first()


        group.unread_count = unread_counts.get(group.id, 0)


        if group.last_message:


            content = group.last_message.content or ''


            if not content and group.last_message.file:


                content = 'فایل ضمیمه شده'


            group.preview_text = content[:45] + ('...' if len(content) > 45 else '')


        else:


            group.preview_text = 'هیچ پیامی هنوز ارسال نشده است.'


        if group.is_direct_message:


            other_member = None


            for member in group.members.all():


                if member != request.user:


                    other_member = member


                    break


            group.display_name = other_member.username if other_member else 'چت خصوصی'


            if other_member and hasattr(other_member, 'userprofile') and getattr(other_member.userprofile, 'avatar'):


                group.avatar_url = other_member.userprofile.avatar.url


            else:


                group.avatar_url = '/static/default-avatar.png'


        else:


            group.display_name = group.name


            group.avatar_url = '/static/default-avatar.png'


    private_groups = [group for group in groups if group.is_private]


    public_groups = [group for group in groups if not group.is_private]


    return render(request, 'chat/chat_list.html', {


        'private_groups': private_groups,


        'public_groups': public_groups,


    })


@login_required


def create_group(request):


    group_type = request.GET.get('group_type', ChatGroup.GROUP_TYPE_GROUP)


    if group_type not in [ChatGroup.GROUP_TYPE_GROUP, ChatGroup.GROUP_TYPE_CHANNEL]:


        group_type = ChatGroup.GROUP_TYPE_GROUP


    initial_data = {


        'group_type': group_type,


        'is_private': request.GET.get('is_private') in ['1', 'true', 'True', 'on'],


    }


    if request.method == 'POST':


        form = CreateGroupForm(request.POST)


        if form.is_valid():


            group = form.save(commit=False)


            group.created_by = request.user


            group.save()


            group.members.add(request.user)


            if group.is_channel:


                group.can_write_users.add(request.user)


            return redirect('chat_room', group_id=group.id)


    else:


        form = CreateGroupForm(initial=initial_data)


    name_placeholder = 'نام چنل را وارد کنید...' if form['group_type'].value() == ChatGroup.GROUP_TYPE_CHANNEL else 'نام گروه را وارد کنید...'


    form.fields['name'].widget.attrs['placeholder'] = name_placeholder


    is_channel_form = form['group_type'].value() == ChatGroup.GROUP_TYPE_CHANNEL


    return render(request, 'chat/create_group.html', {


        'form': form,


        'is_channel_form': is_channel_form,


    })


@login_required


def discover_groups(request):


    available_groups = ChatGroup.objects.filter(is_private=False).prefetch_related('members').order_by('group_type', 'name')


    joined_group_ids = set(request.user.chat_groups.filter(is_private=False).values_list('id', flat=True))


    for group in available_groups:


        group.is_joined = group.id in joined_group_ids


    return render(request, 'chat/discover_groups.html', {


        'available_groups': available_groups,


    })


@login_required


def join_public_group(request, group_id):


    group = get_object_or_404(ChatGroup, id=group_id, is_private=False)


    if request.method == 'POST':


        if request.user not in group.members.all():


            group.members.add(request.user)


        if request.POST.get('call') == '1':


            return redirect(f'/chat/room/{group.id}/?call=1')


        return redirect('chat_room', group_id=group.id)


    return redirect('discover_groups')


@login_required


def chat_room(request, group_id):


    group = get_object_or_404(ChatGroup, id=group_id)


    if request.user not in group.members.all():


        return redirect('chat_list')


    can_write = group.can_user_write(request.user)


    if request.user in group.members.all():


        mark_group_notifications_read(request.user, group)


    MESSAGE_PAGE_SIZE = 50


    recent_messages = group.messages.select_related('author', 'parent__author').order_by('-created_at')[:MESSAGE_PAGE_SIZE]


    messages = list(reversed(recent_messages))


    first_message_id = messages[0].id if messages else 0


    last_message_id = messages[-1].id if messages else 0


    has_more_messages = False


    if first_message_id:


        has_more_messages = ChatMessage.objects.filter(group=group, id__lt=first_message_id).exists()


    invite_link = None


    invite_error = None


    if request.method == 'POST' and 'generate_invite' in request.POST:


        if group.is_direct_message:


            invite_error = 'برای چت دونفره نمی‌توان لینک دعوت ساخت.'


        else:


            token = secrets.token_urlsafe(32)


            invite = GroupInvite.objects.create(group=group, token=token, created_by=request.user)


            invite_link = request.build_absolute_uri(f'/chat/join/{token}/')


    if request.method == 'POST' and 'content' in request.POST:


        return handle_message_creation(request, group)


    return render(request, 'chat/chat_room.html', {


        'group': group,


        'messages': messages,


        'invite_link': invite_link,


        'invite_error': invite_error,


        'first_message_id': first_message_id,


        'last_message_id': last_message_id,


        'has_more_messages': has_more_messages,


        'can_write': can_write,


        'webrtc_ice_servers': settings.WEBRTC_ICE_SERVERS,


    })


def handle_message_creation(request, group):


    wants_json = request.headers.get('X-Requested-With') == 'XMLHttpRequest'


    def message_error(error, status=400):


        if wants_json:


            return JsonResponse({'status': 'error', 'error': error}, status=status)


        return redirect('chat_room', group_id=group.id)


    if request.user not in group.members.all():


        return message_error('شما اجازه ارسال پیام ندارید', status=403)


    if group.is_channel and not group.can_user_write(request.user):


        return message_error('شما اجازه ارسال پیام در این چنل را ندارید', status=403)


    content = request.POST.get('content', '').strip()


    file = request.FILES.get('file')


    parent_id = request.POST.get('parent_id')


    if not content and not file:


        return message_error('پیام خالی است', status=400)


    parent_msg = None


    if parent_id:


        try:


            parent_msg = ChatMessage.objects.get(id=parent_id, group=group)


        except (ChatMessage.DoesNotExist, ValueError, TypeError):


            return message_error('پیامی که به آن پاسخ می‌دهید پیدا نشد', status=400)


    try:


        msg = ChatMessage.objects.create(


            group=group,


            author=request.user,


            content=content if content else "",


            parent=parent_msg,


        )


        if file:


            msg.file = file


            if file.content_type.startswith('image'):


                msg.file_type = 'image'


            elif file.content_type.startswith('audio'):


                msg.file_type = 'audio'


            elif file.content_type.startswith('video'):


                msg.file_type = 'video'


            else:


                msg.file_type = 'file'


            msg.save()


        members = group.members.exclude(id=request.user.id)


        Notification.objects.bulk_create([


            Notification(


                recipient=member,


                group=group,


                message=msg


            )


            for member in members


        ])


        broadcast_chat_message(msg)


        response_data = {


            'status': 'success',


            'message': {


                'id': msg.id,


                'author_username': msg.author.username,


                'content': msg.content,


                'time': msg.created_at.strftime("%H:%M"),


                'is_me': True,


                'file_url': msg.file.url if msg.file else None,


                'file_name': msg.file.name.split('/')[-1] if msg.file else None,


                'file_type': msg.file_type if msg.file else None,


                'parent_id': msg.parent_id,


                'parent_author': msg.parent.author.username if msg.parent else None,


                'parent_content': reply_preview(msg.parent),


                'read_status': msg.read_status_text,


                'read_by_count': msg.read_by_count,


                'recipient_count': msg.recipient_count


            }


        }


        if wants_json:


            return JsonResponse(response_data)


        return redirect('chat_room', group_id=group.id)


    except Exception as e:


        print(f"Error creating message: {e}")


        return message_error('خطایی در سرور رخ داد', status=500)


@login_required


def get_new_messages(request, group_id, last_id):


    try:


        group = get_object_or_404(ChatGroup, id=group_id)


        if request.user not in group.members.all():


            return JsonResponse({'status': 'error'}, status=403)


        new_messages = ChatMessage.objects.select_related('author', 'parent__author').filter(


            group=group,


            id__gt=last_id


        ).order_by('created_at')[:100]


        mark_group_notifications_read(request.user, group)


        messages_data = []


        for msg in new_messages:


            messages_data.append({


                'id': msg.id,


                'author_username': msg.author.username,


                'content': msg.content,


                'time': msg.created_at.strftime("%H:%M"),


                'is_me': msg.author == request.user,


                'file_url': msg.file.url if msg.file else None,


                'file_type': msg.file_type if msg.file else None,


                'file_name': msg.file.name.split('/')[-1] if msg.file else None,


                'parent_id': msg.parent_id,


                'parent_author': msg.parent.author.username if msg.parent else None,


                'parent_content': reply_preview(msg.parent),


                'read_status': msg.read_status_text,


                'read_by_count': msg.read_by_count,


                'recipient_count': msg.recipient_count


            })


        return JsonResponse({'messages': messages_data})


    except Exception as e:


        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)


@login_required


def get_older_messages(request, group_id, before_id):


    try:


        group = get_object_or_404(ChatGroup, id=group_id)


        if request.user not in group.members.all():


            return JsonResponse({'status': 'error'}, status=403)


        older_messages_qs = ChatMessage.objects.select_related('author', 'parent__author').filter(


            group=group,


            id__lt=before_id


        ).order_by('-created_at')[:50]


        older_messages = list(reversed(older_messages_qs))


        messages_data = []


        for msg in older_messages:


            messages_data.append({


                'id': msg.id,


                'author_username': msg.author.username,


                'content': msg.content,


                'time': msg.created_at.strftime("%H:%M"),


                'is_me': msg.author == request.user,


                'file_url': msg.file.url if msg.file else None,


                'file_type': msg.file_type if msg.file else None,


                'file_name': msg.file.name.split('/')[-1] if msg.file else None,


                'parent_id': msg.parent_id,


                'parent_author': msg.parent.author.username if msg.parent else None,


                'parent_content': reply_preview(msg.parent),


                'read_status': msg.read_status_text,


                'read_by_count': msg.read_by_count,


                'recipient_count': msg.recipient_count


            })


        has_more = False


        if older_messages:


            has_more = ChatMessage.objects.filter(group=group, id__lt=older_messages[0].id).exists()


        return JsonResponse({'messages': messages_data, 'has_more': has_more})


    except Exception as e:


        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)


@login_required


def typing_status(request, group_id):


    group = get_object_or_404(ChatGroup, id=group_id)


    if request.user not in group.members.all():


        return JsonResponse({'status': 'error'}, status=403)


    cache_key = f'chat_typing_{group_id}_{request.user.id}'


    if request.method == 'POST':


        typing = request.POST.get('typing') == 'true'


        if typing:


            cache.set(cache_key, True, timeout=5)


        else:


            cache.delete(cache_key)


        return JsonResponse({'status': 'ok'})


    active_typers = []


    for member in group.members.exclude(id=request.user.id):


        if cache.get(f'chat_typing_{group_id}_{member.id}'):


            active_typers.append(member.username)


    return JsonResponse({'typers': active_typers})


@login_required


def join_group_via_link(request, token):


    invite = get_object_or_404(GroupInvite, token=token)


    if invite.group.is_direct_message:


        return redirect('chat_list')


    if request.user not in invite.group.members.all():


        invite.group.members.add(request.user)


    return redirect('chat_room', group_id=invite.group.id)


@login_required

@require_POST

def delete_group(request, group_id):


    group = get_object_or_404(ChatGroup, id=group_id)


    if group.created_by != request.user:


        return JsonResponse({'error': 'فقط سازنده گروه یا چنل می‌تواند آن را حذف کند.'}, status=403)


    channel_layer = get_channel_layer()


    if channel_layer:


        async_to_sync(channel_layer.group_send)(


            f'chat_{group.id}',


            {


                'type': 'group_deleted',


                'group_id': group.id,


            }


        )


    group.delete()


    return redirect('chat_list')


@login_required


def create_invite_link(request, group_id):


    group = get_object_or_404(ChatGroup, id=group_id)


    if request.user not in group.members.all():


        return JsonResponse({'error': 'Access denied'}, status=403)


    if group.is_direct_message:


        return JsonResponse({'error': 'برای چت دونفره نمی‌توان لینک دعوت ساخت.'}, status=403)


    if request.method == 'POST':


        try:


            token = secrets.token_urlsafe(32)


            invite = GroupInvite.objects.create(group=group, token=token, created_by=request.user)


            link = request.build_absolute_uri(f'/chat/join/{token}/')


            return JsonResponse({'link': link})


        except Exception:


            return JsonResponse({'error': 'خطا در ایجاد لینک'}, status=500)


    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required


def delete_message(request, message_id):


    message = get_object_or_404(ChatMessage, id=message_id)


    if message.author != request.user:


        return JsonResponse({'error': 'Access denied'}, status=403)


    message.delete()


    return JsonResponse({'success': True})


@login_required


def leave_group(request, group_id):


    group = get_object_or_404(ChatGroup, id=group_id)


    if request.user in group.members.all():


        group.members.remove(request.user)


        if not group.is_private and group.members.count() == 0:


            group.delete()


        return redirect('chat_list')


@login_required


def start_private_chat(request):


    target_username = request.GET.get('username', None)


    chat = None


    error = None


    if target_username:


        try:


            target_user = User.objects.get(username=target_username)


            if target_user == request.user:


                error = "نمی‌توانید با خودتان چت خصوصی داشته باشید!"


            else:


                chat, created = ChatGroup.get_or_create_private_chat(request.user, target_user)


                if not created:


                    if request.user not in chat.members.all():


                        chat.members.add(request.user)


                if created:


                    ChatMessage.objects.create(


                        group=chat,


                        author=request.user,


                        content="چت خصوصی شروع شد."


                    )


                return redirect('chat_room', group_id=chat.id)


        except User.DoesNotExist:


            error = "کاربری با این نام یافت نشد."


    return render(request, 'chat/chat_list.html', {'error': error})


@login_required


def notifications_list(request):


    notifications = request.user.notifications.all().order_by('-created_at')


    return render(request, 'chat/notifications.html', {'notifications': notifications})


@login_required


def clear_notifications(request):


    request.user.notifications.all().delete()


    return redirect('notifications_list')

