from django.db import models


from django.contrib.auth.models import User


class ChatGroup(models.Model):


    GROUP_TYPE_GROUP = 'group'


    GROUP_TYPE_CHANNEL = 'channel'


    GROUP_TYPE_CHOICES = [


        (GROUP_TYPE_GROUP, 'گروه'),


        (GROUP_TYPE_CHANNEL, 'چنل'),


    ]


    name = models.CharField(max_length=100, verbose_name='نام گروه')


    members = models.ManyToManyField(User, related_name='chat_groups', verbose_name='اعضا')


    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups', verbose_name='سازنده')


    created_at = models.DateTimeField(auto_now_add=True)


    is_private = models.BooleanField(default=False, verbose_name='چت خصوصی')


    is_direct_message = models.BooleanField(default=False, verbose_name='چت مستقیم')


    group_type = models.CharField(


        max_length=10,


        choices=GROUP_TYPE_CHOICES,


        default=GROUP_TYPE_GROUP,


        verbose_name='نوع گروه'


    )


    can_write_users = models.ManyToManyField(


        User,


        blank=True,


        related_name='writable_channels',


        verbose_name='کاربران قادر به نوشتن'


    )


    def __str__(self):


        return self.name


    @property


    def is_channel(self):


        return self.group_type == self.GROUP_TYPE_CHANNEL


    def can_user_write(self, user):


        if not self.is_channel:


            return True


        return self.created_by == user or self.can_write_users.filter(id=user.id).exists()


    @classmethod


    def get_or_create_private_chat(cls, user1, user2):


        private_chats = cls.objects.filter(
            is_private=True,
            is_direct_message=True,
            members=user1,
        ).filter(members=user2)


        if private_chats.exists():


            return private_chats.first(), False 


        else:


            chat = cls.objects.create(
                name=f"Private {user1.username}-{user2.username}",
                is_private=True,
                is_direct_message=True,
                created_by=user1,
            )


            chat.members.add(user1, user2)


            return chat, True 


class ChatMessage(models.Model):


    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='messages', verbose_name='گروه')


    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='فرستنده')


    content = models.TextField(blank=True, null=True, verbose_name='متن پیام')


    file = models.FileField(upload_to='chat_files/', blank=True, null=True, verbose_name='فایل پیوست')


    file_type = models.CharField(max_length=20, blank=True, null=True, verbose_name='نوع فایل')


    is_video_message = models.BooleanField(default=False, verbose_name='آیا ویدیو مسیج است؟')


    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name='پاسخ به')


    created_at = models.DateTimeField(auto_now_add=True)


    @property


    def recipient_count(self):


        return self.group.members.exclude(id=self.author_id).count()


    @property


    def read_by_count(self):


        return self.notification_set.filter(is_read=True).count()


    @property


    def read_status_text(self):


        total = self.recipient_count


        if total == 0:


            return ''


        read_count = self.read_by_count


        if read_count == total:


            return 'خوانده شده'


        if read_count > 0:


            return f'خوانده شده توسط {read_count}/{total}'


        return ''


    def __str__(self):


        return f'{self.author.username}: {self.content[:20] if self.content else "File"}'


class GroupInvite(models.Model):


    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='invites', verbose_name='گروه')


    token = models.CharField(max_length=64, unique=True, verbose_name='توکن دعوت')


    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invites', verbose_name='فرستنده دعوت')


    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):


        return f"Invite to {self.group.name}"


class Notification(models.Model):


    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='گیرنده')


    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, verbose_name='گروه مربوطه')


    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, verbose_name='پیام مربوطه')


    is_read = models.BooleanField(default=False, verbose_name='خوانده شده')


    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):


        return f'Notification for {self.recipient.username}'

