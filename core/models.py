from django.db import models


from django.contrib.auth.models import User


from django.utils import timezone


import os


import re


import uuid


from django.urls import reverse


from django.utils.deconstruct import deconstructible


@deconstructible


class PathAndRename(object):


    def __init__(self, sub_path):


        self.path = sub_path


    def __call__(self, instance, filename):


        ext = filename.split('.')[-1]


        filename = '{}.{}'.format(uuid.uuid4().hex, ext)


        return os.path.join(self.path, filename)


path_and_rename_avatars = PathAndRename("avatars/")


path_and_rename_posts = PathAndRename("posts/")


path_and_rename_blog = PathAndRename("blog_images/")

path_and_rename_blog_media = PathAndRename("blog_media/")

path_and_rename_communities = PathAndRename("communities/")

path_and_rename_ads = PathAndRename("ads/")

path_and_rename_team_projects = PathAndRename("team_projects/")


class ProfileTag(models.Model):


    name = models.CharField(max_length=50, verbose_name='نام تگ')


    color = models.CharField(max_length=7, default='#007bff', verbose_name='رنگ متن')


    background_color = models.CharField(max_length=7, default='#e7f1ff', verbose_name='رنگ پس‌زمینه')


    icon = models.CharField(max_length=20, blank=True, verbose_name='آیکون (emoji)')


    is_active = models.BooleanField(default=True, verbose_name='فعال')


    is_admin_only = models.BooleanField(default=False, verbose_name='فقط برای ادمین')


    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب')


    class Meta:


        verbose_name = 'تگ پروفایل'


        verbose_name_plural = 'تگ‌های پروفایل'


        ordering = ['order', 'name']


    def __str__(self):


        return self.name


class UserProfile(models.Model):


    user = models.OneToOneField(User, on_delete=models.CASCADE)


    bio = models.TextField(blank=True, null=True, verbose_name='بیوگرافی')


    avatar = models.ImageField(upload_to=path_and_rename_avatars, blank=True, null=True, verbose_name='تصویر پروفایل')


    background_color = models.CharField(max_length=7, default='#ffffff', verbose_name='رنگ پس‌زمینه')


    text_color = models.CharField(max_length=7, default='#000000', verbose_name='رنگ متن')


    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')


    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name='شماره موبایل')


    interests = models.TextField(blank=True, null=True, verbose_name='علاقه‌مندی‌ها')


    personality_traits = models.TextField(blank=True, null=True, verbose_name='صفات شخصیتی')
    selected_tag = models.ForeignKey(


        ProfileTag,


        on_delete=models.SET_NULL,


        null=True,


        blank=True,


        verbose_name='تگ انتخابی'


    )


    def __str__(self):


        return self.user.username


class TeamPortfolio(models.Model):


    title = models.CharField(max_length=120, default='تیم فان میگ', verbose_name='عنوان اصلی')

    subtitle = models.CharField(
        max_length=220,
        default='طراحی، توسعه و رشد محصول دیجیتال با تمرکز روی تجربه اجتماعی و ابزارهای کاربردی',
        verbose_name='زیرعنوان',
    )

    intro = models.TextField(
        default='ما تیم فان میگ هستیم؛ یک تیم محصول محور که از ایده تا طراحی، توسعه، انتشار و پشتیبانی کنار کسب و کارها می ایستد.',
        verbose_name='معرفی کوتاه',
    )

    mission = models.TextField(
        default='ماموریت ما ساخت تجربه هایی است که ساده، سریع، امن و برای کاربران واقعی دوست داشتنی باشند.',
        verbose_name='ماموریت',
    )

    services = models.TextField(
        default='طراحی و توسعه وب اپلیکیشن|ساخت پنل های مدیریتی، شبکه اجتماعی، مارکت پلیس و ابزارهای اختصاصی\nاتوماسیون و ابزارهای دیجیتال|طراحی فرایندهای سریع، داشبوردهای عملیاتی و ابزارهای اختصاصی\nطراحی تجربه کاربری|طراحی مسیر کاربر، رابط کاربری، هویت بصری و بهینه سازی نرخ تبدیل\nزیرساخت و نگهداری|استقرار، مانیتورینگ، امنیت، بهینه سازی سرعت و پشتیبانی فنی',
        verbose_name='خدمات (هر خط: عنوان|توضیح)',
    )

    stats = models.TextField(
        default='24/7|پشتیبانی\n+10|ماژول محصولی\nUX|تمرکز روی تجربه کاربر\nPWA|آماده نصب روی موبایل',
        verbose_name='آمار (هر خط: عدد|عنوان)',
    )

    team_members = models.TextField(
        default='مدیریت محصول|استراتژی، نقشه راه و هماهنگی تیم\nتوسعه بک اند|Django، API، امنیت و دیتابیس\nتوسعه فرانت اند|رابط کاربری، ریسپانسیو و تجربه سریع\nطراحی و محتوا|هویت بصری، متن محصول و ارتباط با کاربر',
        verbose_name='اعضای تیم (هر خط: نقش|توضیح)',
    )

    projects = models.TextField(
        default='FUNMIG|شبکه اجتماعی، وبلاگ، چت و ابزارهای ارتباطی در یک محصول\nپنل مدیریت فان میگ|مدیریت کاربران، محتوا، پرداخت، بنرها، اعلامیه ها و پشتیبانی\nسیستم محتوای دیجیتال|تولید، مدیریت و انتشار محتوای متنی و رسانه ای',
        verbose_name='نمونه کارها (هر خط: عنوان|توضیح)',
    )

    tools = models.TextField(
        default='Django\nChannels\nNginx\nNSSM\nSQLite/PostgreSQL\nPWA\nHTML/CSS/JavaScript',
        verbose_name='تکنولوژی ها (هر خط یک مورد)',
    )

    process = models.TextField(
        default='شناخت نیاز|بررسی هدف، مخاطب، محدودیت ها و اولویت های محصول\nطراحی راه حل|ساخت ساختار، وایرفریم، UI و معماری فنی\nتوسعه و تست|پیاده سازی مرحله ای، تست، بازبینی و آماده سازی انتشار\nاستقرار و رشد|دیپلوی، مانیتورینگ، بهبود سرعت و اضافه کردن قابلیت های بعدی',
        verbose_name='فرایند همکاری (هر خط: عنوان|توضیح)',
    )

    cta_title = models.CharField(max_length=160, default='آماده ایم محصول بعدی را با شما بسازیم', verbose_name='عنوان دعوت به اقدام')

    cta_text = models.TextField(default='برای همکاری، مشاوره یا توسعه یک محصول اختصاصی با تیم فان میگ در ارتباط باشید.', verbose_name='متن دعوت به اقدام')

    phone = models.CharField(max_length=40, default='09993397299', verbose_name='شماره تماس')

    telegram_url = models.URLField(max_length=255, default='https://t.me/FUNMIGweb', verbose_name='لینک تلگرام')

    email = models.EmailField(default='admin@funmig.com', verbose_name='ایمیل')

    address = models.CharField(max_length=255, default='مشهد، امامت ۱۸، پلاک ۱۲۶', verbose_name='آدرس')

    is_active = models.BooleanField(default=True, verbose_name='فعال')

    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')


    class Meta:


        verbose_name = 'پروفایلوی تیم فان میگ'

        verbose_name_plural = 'پروفایلوی تیم فان میگ'


    def save(self, *args, **kwargs):


        self.pk = 1

        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):


        return


    def _split_pairs(self, value):


        items = []

        for line in (value or '').splitlines():

            line = line.strip()

            if not line:

                continue

            title, sep, text = line.partition('|')

            items.append({'title': title.strip(), 'text': text.strip() if sep else ''})

        return items


    def _split_lines(self, value):


        return [line.strip() for line in (value or '').splitlines() if line.strip()]


    @property

    def service_items(self):


        return self._split_pairs(self.services)


    @property

    def stat_items(self):


        return self._split_pairs(self.stats)


    @property

    def team_items(self):


        return self._split_pairs(self.team_members)


    @property

    def project_items(self):


        return self._split_pairs(self.projects)


    @property

    def tool_items(self):


        return self._split_lines(self.tools)


    @property

    def process_items(self):


        return self._split_pairs(self.process)


    def __str__(self):


        return self.title


class TeamPortfolioProject(models.Model):


    portfolio = models.ForeignKey(
        TeamPortfolio,
        on_delete=models.CASCADE,
        related_name='project_cards',
        verbose_name='پروفایلو',
    )

    title = models.CharField(max_length=140, verbose_name='عنوان پروژه')

    description = models.TextField(blank=True, verbose_name='توضیح پروژه')

    image = models.ImageField(
        upload_to=path_and_rename_team_projects,
        blank=True,
        null=True,
        verbose_name='عکس پروژه',
    )

    project_url = models.URLField(max_length=500, blank=True, verbose_name='لینک پروژه (اختیاری)')

    is_active = models.BooleanField(default=True, verbose_name='فعال')

    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')


    class Meta:


        ordering = ['order', '-created_at']

        verbose_name = 'پروژه پروفایلوی تیم'

        verbose_name_plural = 'پروژه های پروفایلوی تیم'


    def __str__(self):


        return self.title


class Community(models.Model):


    name = models.CharField(max_length=80, unique=True, verbose_name='نام انجمن')

    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name='نشانی انجمن')

    description = models.TextField(max_length=500, verbose_name='معرفی انجمن')

    rules = models.TextField(blank=True, verbose_name='قوانین انجمن')

    cover = models.ImageField(
        upload_to=path_and_rename_communities,
        blank=True,
        null=True,
        verbose_name='تصویر انجمن'
    )

    color = models.CharField(max_length=7, default='#8b5cf6', verbose_name='رنگ انجمن')

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_communities',
        verbose_name='سازنده'
    )

    members = models.ManyToManyField(
        User,
        through='CommunityMembership',
        related_name='communities',
        verbose_name='اعضا'
    )

    is_active = models.BooleanField(default=True, verbose_name='فعال')

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


    class Meta:

        ordering = ['-created_at']

        verbose_name = 'انجمن'

        verbose_name_plural = 'انجمن‌ها'


    def __str__(self):

        return self.name


class CommunityMembership(models.Model):


    ROLE_MEMBER = 'member'

    ROLE_MODERATOR = 'moderator'

    ROLE_CHOICES = (
        (ROLE_MEMBER, 'عضو'),
        (ROLE_MODERATOR, 'مدیر'),
    )


    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name='انجمن'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='community_memberships',
        verbose_name='کاربر'
    )

    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default=ROLE_MEMBER)

    joined_at = models.DateTimeField(auto_now_add=True)


    class Meta:

        unique_together = ('community', 'user')

        ordering = ['-joined_at']

        verbose_name = 'عضویت انجمن'

        verbose_name_plural = 'عضویت‌های انجمن'


    def __str__(self):

        return f'{self.user.username} - {self.community.name}'


class Post(models.Model):


    author = models.ForeignKey(User, on_delete=models.CASCADE)


    content = models.TextField(blank=True, verbose_name='محتوا')


    image = models.ImageField(upload_to=path_and_rename_posts, blank=True, null=True, verbose_name='تصویر پست')


    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name='ریپلای به')

    community = models.ForeignKey(
        Community,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='انجمن'
    )

    submission_token = models.UUIDField(null=True, blank=True, unique=True, editable=False)


    is_pinned = models.BooleanField(default=False, verbose_name='پین شده')


    created_at = models.DateTimeField(default=timezone.now)


    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):


        return f'{self.author.username} - {self.content[:20]}'


    def total_likes(self):


        return self.like_set.count()


    @property

    def total_views(self):


        return self.views.count()


    @property

    def total_reactions(self):


        return 0


    @property

    def total_shares(self):


        return 0


    @property

    def reactions_breakdown(self):


        return []


    def is_reply(self):


        return self.parent is not None


    def active_media(self):


        return self.media.filter(is_active=True).order_by('order')


class Like(models.Model):


    post = models.ForeignKey(Post, on_delete=models.CASCADE)


    user = models.ForeignKey(User, on_delete=models.CASCADE)


    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:


        unique_together = ('post', 'user')


class PostView(models.Model):


    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views')


    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)


    ip_address = models.GenericIPAddressField(blank=True, null=True)


    viewed_at = models.DateTimeField(auto_now_add=True)


    class Meta:


        ordering = ['-viewed_at']


        indexes = [


            models.Index(fields=['post', '-viewed_at']),


            models.Index(fields=['user', '-viewed_at']),


            models.Index(fields=['ip_address', '-viewed_at']),


        ]


class Comment(models.Model):


    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')


    author = models.ForeignKey(User, on_delete=models.CASCADE)


    text = models.TextField(verbose_name='متن کامنت')


    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name='پاسخ به')


    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):


        return f'{self.author.username} - {self.text[:20]}'


class SavedPost(models.Model):


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts')


    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved_by')


    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:


        unique_together = ('user', 'post')


        verbose_name = 'پست ذخیره‌شده'


        verbose_name_plural = 'پست‌های ذخیره‌شده'


        ordering = ['-created_at']


    def __str__(self):


        return f'{self.user.username} saved {self.post.id}'


class Hashtag(models.Model):


    name = models.CharField(max_length=80, unique=True, db_index=True, verbose_name='نام هشتگ')


    post_count = models.PositiveIntegerField(default=0, verbose_name='تعداد پست')


    created_at = models.DateTimeField(auto_now_add=True)


    updated_at = models.DateTimeField(auto_now=True)


    class Meta:


        ordering = ['-post_count', 'name']


        verbose_name = 'هشتگ'


        verbose_name_plural = 'هشتگ‌ها'


    def __str__(self):


        return f'#{self.name}'


class PostHashtag(models.Model):


    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_hashtags')


    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE, related_name='post_links')


    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:


        unique_together = ('post', 'hashtag')


        indexes = [


            models.Index(fields=['post', 'hashtag']),


            models.Index(fields=['hashtag', 'created_at']),


        ]


        verbose_name = 'هشتگ پست'


        verbose_name_plural = 'هشتگ‌های پست'


    def __str__(self):


        return f'{self.post_id} -> #{self.hashtag.name}'


class PostMedia(models.Model):


    MEDIA_CHOICES = (


        ('image', 'Image'),


        ('video', 'Video'),


        ('audio', 'Audio'),


        ('file', 'File'),


    )


    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')


    file = models.FileField(upload_to=path_and_rename_posts, verbose_name='فایل رسانه')


    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES, default='image')


    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب')


    is_active = models.BooleanField(default=False, verbose_name='فعال (نمایش داشته باشد)')


    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:


        ordering = ['order', '-created_at']


        verbose_name = 'رسانه پست'


        verbose_name_plural = 'رسانه‌های پست'


    def __str__(self):


        return f'{self.media_type} for post {self.post.id} ({self.id})'


class BlogPost(models.Model):


    STATUS_CHOICES = (


        ('published', 'منتشر شده'),


    )


    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')


    title = models.CharField(max_length=200, verbose_name='عنوان مقاله')


    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')


    description = models.TextField(blank=True, verbose_name='خلاصه مقاله')


    category = models.CharField(max_length=100, blank=True, verbose_name='دسته‌بندی')


    tags = models.CharField(max_length=200, blank=True, verbose_name='برچسب‌ها')


    source = models.CharField(max_length=255, blank=True, verbose_name='نام منبع')


    source_url = models.URLField(max_length=500, blank=True, verbose_name='لینک منبع')


    content = models.TextField(verbose_name='محتوای مقاله')


    image = models.ImageField(upload_to=path_and_rename_blog, blank=True, null=True, verbose_name='تصویر مقاله')


    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')


    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')


    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published', verbose_name='وضعیت')


    class Meta:


        verbose_name = 'مقاله وبلاگ'


        verbose_name_plural = 'مقالات وبلاگ'


        ordering = ['-created_at']


    def __str__(self):


        return self.title


    def get_absolute_url(self):


        return reverse('blog_detail', kwargs={'slug': self.slug})


    @property


    def reading_time(self):


        content_text = re.sub(r'<[^>]+>', '', self.content or '')


        word_count = len(re.findall(r'\w+', content_text))


        return max(1, (word_count + 199) // 200)


    @property


    def excerpt(self):


        if self.description:


            return self.description.strip()


        content_text = re.sub(r'<[^>]+>', '', self.content or '')

        return content_text.strip()[:180] + ('...' if len(content_text) > 180 else '')


class BlogMedia(models.Model):


    MEDIA_CHOICES = (


        ('image', 'تصویر'),


        ('audio', 'صوت'),


    )


    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='آپلودکننده')


    file = models.FileField(upload_to=path_and_rename_blog_media, verbose_name='فایل')


    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES, verbose_name='نوع رسانه')


    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')


    class Meta:


        verbose_name = 'رسانه وبلاگ'


        verbose_name_plural = 'رسانه‌های وبلاگ'


        ordering = ['-created_at']


    def __str__(self):


        return f'{self.get_media_type_display()} - {self.created_at:%Y-%m-%d}'


class Ticket(models.Model):


    STATUS_CHOICES = (


        ('open', 'باز'),


        ('closed', 'بسته'),


    )


    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')


    subject = models.CharField(max_length=200, verbose_name='موضوع')


    message = models.TextField(verbose_name='پیام')


    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open', verbose_name='وضعیت')


    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')


    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')


    class Meta:


        verbose_name = 'تیکت'


        verbose_name_plural = 'تیکت‌ها'


        ordering = ['-created_at']


    def __str__(self):


        return f"{self.user.username} - {self.subject}"


class TicketReply(models.Model):


    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies', verbose_name='تیکت')


    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')


    message = models.TextField(verbose_name='پیام')


    is_admin = models.BooleanField(default=False, verbose_name='پاسخ ادمین')


    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')


    class Meta:


        verbose_name = 'پاسخ تیکت'


        verbose_name_plural = 'پاسخ‌های تیکت'


        ordering = ['created_at']


    def __str__(self):


        return f"پاسخ به {self.ticket.subject}"


class Banner(models.Model):


    title = models.CharField(max_length=100, verbose_name='عنوان بنر')


    description = models.TextField(verbose_name='متن بنر')


    link = models.CharField(max_length=255, blank=True, null=True, verbose_name='لینک (اختیاری)')


    image = models.ImageField(upload_to=path_and_rename_ads, blank=True, null=True, verbose_name='تصویر تبلیغ')


    placement = models.CharField(max_length=50, default='site_top', verbose_name='جایگاه نمایش')


    background_color = models.CharField(max_length=7, default='#6366f1', verbose_name='رنگ پس‌زمینه')


    text_color = models.CharField(max_length=7, default='#ffffff', verbose_name='رنگ متن')


    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')


    is_dismissible = models.BooleanField(default=True, verbose_name='قابلیت بستن توسط کاربر')


    starts_at = models.DateTimeField(blank=True, null=True, verbose_name='شروع نمایش')


    ends_at = models.DateTimeField(blank=True, null=True, verbose_name='پایان نمایش')


    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='ایجادکننده')


    created_at = models.DateTimeField(auto_now_add=True)


    updated_at = models.DateTimeField(auto_now=True)


    class Meta:


        verbose_name = 'بنر'


        verbose_name_plural = 'بنرها'


        ordering = ['-created_at']


    def __str__(self):


        return self.title


    def is_currently_active(self):


        now = timezone.now()


        if not self.is_active:


            return False


        if self.starts_at and self.starts_at > now:


            return False


        if self.ends_at and self.ends_at < now:


            return False


        return True


class Announcement(models.Model):


    TYPE_INFO = 'info'

    TYPE_UPDATE = 'update'

    TYPE_WARNING = 'warning'

    TYPE_CHOICES = (
        (TYPE_INFO, 'اطلاعیه'),
        (TYPE_UPDATE, 'آپدیت'),
        (TYPE_WARNING, 'مهم'),
    )


    title = models.CharField(max_length=120, verbose_name='عنوان اعلامیه')


    message = models.TextField(verbose_name='متن اعلامیه')


    announcement_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_INFO, verbose_name='نوع اعلامیه')


    link = models.CharField(max_length=255, blank=True, null=True, verbose_name='لینک (اختیاری)')


    link_label = models.CharField(max_length=40, default='جزئیات', verbose_name='متن دکمه')


    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')


    is_dismissible = models.BooleanField(default=True, verbose_name='قابلیت بستن توسط کاربر')


    starts_at = models.DateTimeField(blank=True, null=True, verbose_name='شروع نمایش')


    ends_at = models.DateTimeField(blank=True, null=True, verbose_name='پایان نمایش')


    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='ایجادکننده')


    created_at = models.DateTimeField(auto_now_add=True)


    updated_at = models.DateTimeField(auto_now=True)


    class Meta:


        verbose_name = 'اعلامیه'


        verbose_name_plural = 'اعلامیه‌ها'


        ordering = ['-created_at']


    def __str__(self):


        return self.title


    def is_currently_active(self):


        now = timezone.now()


        if not self.is_active:


            return False


        if self.starts_at and self.starts_at > now:


            return False


        if self.ends_at and self.ends_at < now:


            return False


        return True


class Follow(models.Model):


    follower = models.ForeignKey(


        User,


        on_delete=models.CASCADE,


        related_name='following',


        verbose_name='دنبال‌کننده'


    )


    following = models.ForeignKey(


        User,


        on_delete=models.CASCADE,


        related_name='followers',


        verbose_name='دنبال‌شونده'


    )


    created_at = models.DateTimeField(default=timezone.now)


    class Meta:


        unique_together = ('follower', 'following')


        verbose_name = 'فالو'


        verbose_name_plural = 'فالوها'


        ordering = ['-created_at']


    def __str__(self):


        return f"{self.follower.username} فالو کرد {self.following.username}"


class SiteNotification(models.Model):


    TYPE_CHOICES = (


        ('like', 'لایک'),


        ('comment', 'کامنت'),


        ('reply', 'پاسخ'),


        ('follow', 'فالو'),


        ('save', 'ذخیره'),


        ('share', 'اشتراک'),


        ('mention', 'منشن'),


        ('payment', 'پرداخت'),


        ('system', 'سیستم'),


    )


    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='site_notifications')


    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_site_notifications')


    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='system')


    title = models.CharField(max_length=120)


    message = models.TextField(blank=True)


    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')


    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')


    url = models.CharField(max_length=255, blank=True)


    is_read = models.BooleanField(default=False)


    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:


        ordering = ['-created_at']


        indexes = [


            models.Index(fields=['recipient', 'is_read', '-created_at']),


            models.Index(fields=['notification_type', '-created_at']),


        ]


        verbose_name = 'نوتیفیکیشن سایت'


        verbose_name_plural = 'نوتیفیکیشن‌های سایت'


    def __str__(self):


        return f'{self.recipient.username} - {self.notification_type}'


class PushSubscription(models.Model):


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_subscriptions')


    subscription_data = models.JSONField()


    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):


        return f"Push subscription for {self.user.username}"


