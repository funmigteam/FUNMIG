

from django.contrib import admin


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from django.contrib.auth.models import User


from django.forms import Widget


from django.db import models


from django.utils.safestring import mark_safe


from .models import (


    UserProfile, Post, Like, Comment, ProfileTag, PostMedia,


    Hashtag, PostHashtag, SiteNotification, PostView, Community, BlogPost, BlogMedia,
    CommunityMembership, Banner, Announcement, TeamPortfolio,
    TeamPortfolioProject


)


class AdminReadabilityMixin:


    class Media:


        css = {'all': ('admin/css/funmig_admin_readability.css',)}


class TeamPortfolioProjectInline(admin.TabularInline):


    model = TeamPortfolioProject

    extra = 1

    fields = ('order', 'title', 'description', 'image', 'image_preview', 'project_url', 'is_active')

    readonly_fields = ('image_preview',)


    @admin.display(description='پیش نمایش عکس')

    def image_preview(self, obj):


        if obj and obj.image:


            return mark_safe(
                f'<img src="{obj.image.url}" width="90" height="56" '
                f'style="object-fit:cover;border-radius:6px;border:1px solid #ddd;">'
            )


        return '-'


@admin.register(TeamPortfolio)

class TeamPortfolioAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('title', 'is_active', 'updated_at', 'open_site')

    readonly_fields = ('updated_at',)

    inlines = (TeamPortfolioProjectInline,)

    fieldsets = (
        ('معرفی اصلی', {
            'fields': ('title', 'subtitle', 'intro', 'mission', 'is_active')
        }),
        ('محتوای صفحه', {
            'fields': ('stats', 'services', 'team_members', 'tools', 'process')
        }),
        ('تماس و دعوت به اقدام', {
            'fields': ('cta_title', 'cta_text', 'phone', 'telegram_url', 'email', 'address')
        }),
        ('سیستمی', {
            'fields': ('updated_at',)
        }),
    )


    def has_add_permission(self, request):


        return not TeamPortfolio.objects.exists()


    def has_delete_permission(self, request, obj=None):


        return False


    @admin.display(description='نمایش سایت')

    def open_site(self, obj):


        return mark_safe('<a href="https://funmig.com/" target="_blank">باز کردن funmig.com</a>')


@admin.register(TeamPortfolioProject)

class TeamPortfolioProjectAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('title', 'portfolio', 'project_link', 'is_active', 'order', 'updated_at')

    list_editable = ('is_active', 'order')

    list_filter = ('is_active', 'created_at')

    search_fields = ('title', 'description', 'project_url')

    readonly_fields = ('created_at', 'updated_at', 'image_preview')

    fields = (
        'portfolio', 'title', 'description', 'image', 'image_preview',
        'project_url', 'is_active', 'order', 'created_at', 'updated_at'
    )


    @admin.display(description='لینک')

    def project_link(self, obj):


        if obj.project_url:


            return mark_safe(f'<a href="{obj.project_url}" target="_blank">باز کردن</a>')


        return 'بدون لینک'


    @admin.display(description='پیش نمایش عکس')

    def image_preview(self, obj):


        if obj and obj.image:


            return mark_safe(
                f'<img src="{obj.image.url}" width="180" height="110" '
                f'style="object-fit:cover;border-radius:6px;border:1px solid #ddd;">'
            )


        return '-'


class ColorPickerWidget(Widget):


    def __init__(self, attrs=None):


        default_attrs = {'style': 'width:60px;height:35px;padding:2px;'}


        if attrs:


            default_attrs.update(attrs)


        super().__init__(default_attrs)


    def render(self, name, value, attrs=None, renderer=None):


        if value is None:


            value = '#007bff'


        field_id = attrs.get('id') if attrs else f'id_{name}'


        color_id = f'{field_id}_color'


        return mark_safe(f'''
        <div class="color-picker-wrapper" style="display:flex;align-items:center;gap:10px;">
            <input type="color" name="{name}_color" value="{value}" 
                   id="{color_id}"
                   style="width:50px;height:35px;padding:2px;cursor:pointer;"
                   onchange="document.getElementById('{field_id}').value = this.value">
            <input type="text" name="{name}" value="{value}" 
                   id="{field_id}" 
                   style="width:80px;direction:ltr;" 
                   maxlength="7" 
                   pattern="^#[0-9A-Fa-f]{ 6} $"
                   onchange="if(/^#[0-9A-Fa-f]{ 6} $/.test(this.value))document.getElementById('{color_id}').value = this.value">
        </div>
        ''')


def content_preview(obj):


    return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content


content_preview.short_description = 'متن پست'


def is_reply(obj):


    result = obj.parent is not None


    return result


is_reply.boolean = True


is_reply.short_description = 'ریپلای است؟'


def text_preview(obj):


    return obj.text[:30] + "..."


text_preview.short_description = 'متن نظر'


class UserProfileInline(admin.StackedInline):


    model = UserProfile


    can_delete = False


    verbose_name_plural = 'پروفایل کاربر'


    fields = (


        'avatar', 'bio', 'background_color', 'text_color',


        'birth_date', 'phone_number',


        'interests', 'personality_traits', 'selected_tag'


    )


    formfield_overrides = {


        models.CharField: {'widget': ColorPickerWidget},


    }


class UserAdmin(AdminReadabilityMixin, BaseUserAdmin):


    inlines = (UserProfileInline,)


admin.site.unregister(User)


admin.site.register(User, UserAdmin)


@admin.register(Post)


class PostAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('author', content_preview, 'community', 'created_at', is_reply, 'is_pinned')


    list_filter = ('created_at', 'author', 'community', 'is_pinned')


    search_fields = ('content', 'author__username')


    readonly_fields = ('created_at', 'updated_at')


@admin.register(Community)

class CommunityAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('name', 'owner', 'is_active', 'created_at')

    list_filter = ('is_active', 'created_at')

    search_fields = ('name', 'description', 'owner__username')

    prepopulated_fields = {'slug': ('name',)}


@admin.register(CommunityMembership)

class CommunityMembershipAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('user', 'community', 'role', 'joined_at')

    list_filter = ('role', 'community')

    search_fields = ('user__username', 'community__name')


@admin.register(Comment)


class CommentAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('author', 'post', text_preview, 'parent', 'created_at')


    list_filter = ('created_at',)


    search_fields = ('text', 'author__username')


@admin.register(Like)


class LikeAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('user', 'post', 'created_at')


    list_filter = ('created_at',)


@admin.register(PostView)

class PostViewAdmin(AdminReadabilityMixin, admin.ModelAdmin):

    list_display = ('post', 'user', 'ip_address', 'viewed_at')

    list_filter = ('viewed_at',)

    search_fields = ('post__content', 'user__username', 'ip_address')

    readonly_fields = ('viewed_at',)


@admin.register(UserProfile)


class UserProfileAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('user', 'avatar_preview', 'background_color_preview', 'text_color_preview')


    search_fields = ('user__username', 'user__email')


    def get_form(self, request, obj=None, **kwargs):


        form = super().get_form(request, obj, **kwargs)


        for field_name in ['background_color', 'text_color']:


            if field_name in form.base_fields:


                form.base_fields[field_name].widget = ColorPickerWidget()


        return form


    def avatar_preview(self, obj):


        if obj.avatar:


            return mark_safe(f'<img src="{obj.avatar.url}" width="40" height="40" style="border-radius:50%;">')


        return '-'


    avatar_preview.short_description = 'آواتار'


    def background_color_preview(self, obj):


        return mark_safe(f'<div style="width:30px;height:30px;background-color:{obj.background_color};border-radius:4px;border:1px solid #ddd;"></div>')


    background_color_preview.short_description = 'رنگ پس‌زمینه'


    def text_color_preview(self, obj):


        return mark_safe(f'<div style="width:30px;height:30px;background-color:{obj.text_color};border-radius:4px;border:1px solid #ddd;"></div>')


    text_color_preview.short_description = 'رنگ متن'


@admin.register(BlogPost)

class BlogPostAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('title', 'author', 'status', 'created_at', 'updated_at')


    list_filter = ('status', 'created_at')


    search_fields = ('title', 'description', 'content', 'tags', 'source')


    prepopulated_fields = {'slug': ('title',)}


    readonly_fields = ('created_at', 'updated_at')


    fields = (
        'author', 'title', 'slug', 'description', 'tags',
        'source', 'source_url', 'image', 'content', 'status',
        'created_at', 'updated_at'
    )


@admin.register(BlogMedia)

class BlogMediaAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('file', 'media_type', 'uploader', 'created_at')


    list_filter = ('media_type', 'created_at')


    search_fields = ('file', 'uploader__username')


    readonly_fields = ('created_at',)


@admin.register(Banner)

class BannerAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('title', 'placement', 'is_active', 'starts_at', 'ends_at', 'created_by', 'created_at')


    list_filter = ('is_active', 'placement', 'created_at')


    search_fields = ('title', 'description', 'link')


    readonly_fields = ('created_at', 'updated_at')


    fields = (
        'title', 'description', 'link', 'image', 'placement',
        'background_color', 'text_color', 'is_active', 'is_dismissible',
        'starts_at', 'ends_at', 'created_by', 'created_at', 'updated_at'
    )


    def save_model(self, request, obj, form, change):


        if not obj.created_by:


            obj.created_by = request.user


        super().save_model(request, obj, form, change)


@admin.register(Announcement)

class AnnouncementAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('title', 'announcement_type', 'is_active', 'starts_at', 'ends_at', 'created_by', 'created_at')


    list_filter = ('announcement_type', 'is_active', 'created_at')


    search_fields = ('title', 'message', 'link')


    readonly_fields = ('created_at', 'updated_at')


    fields = (
        'title', 'message', 'announcement_type', 'link', 'link_label',
        'is_active', 'is_dismissible', 'starts_at', 'ends_at',
        'created_by', 'created_at', 'updated_at'
    )


    def save_model(self, request, obj, form, change):


        if not obj.created_by:


            obj.created_by = request.user


        super().save_model(request, obj, form, change)


@admin.register(PostMedia)


class PostMediaAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('post', 'media_type', 'order', 'is_active', 'created_at')


    list_filter = ('media_type', 'is_active', 'created_at')


    search_fields = ('post__content', 'post__author__username')


@admin.register(Hashtag)


class HashtagAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('name', 'post_count', 'updated_at')


    search_fields = ('name',)


    readonly_fields = ('post_count', 'created_at', 'updated_at')


@admin.register(PostHashtag)


class PostHashtagAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('post', 'hashtag', 'created_at')


    search_fields = ('post__content', 'hashtag__name')


    list_filter = ('created_at',)


@admin.register(SiteNotification)


class SiteNotificationAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('recipient', 'actor', 'notification_type', 'title', 'is_read', 'created_at')


    list_filter = ('notification_type', 'is_read', 'created_at')


    search_fields = ('recipient__username', 'actor__username', 'title', 'message')


    readonly_fields = ('created_at',)


@admin.register(ProfileTag)


class ProfileTagAdmin(AdminReadabilityMixin, admin.ModelAdmin):


    list_display = ('name', 'icon', 'color_preview', 'background_color_preview', 'is_active', 'is_admin_only', 'order')


    list_editable = ('is_active', 'is_admin_only', 'order')


    search_fields = ('name',)


    list_filter = ('is_active', 'is_admin_only')


    ordering = ('order', 'name')


    def get_form(self, request, obj=None, **kwargs):


        form = super().get_form(request, obj, **kwargs)


        for field_name in ['color', 'background_color']:


            if field_name in form.base_fields:


                form.base_fields[field_name].widget = ColorPickerWidget()


        return form


    def color_preview(self, obj):


        return mark_safe(f'<div style="width:30px;height:30px;background-color:{obj.color};border-radius:4px;border:1px solid #ddd;"></div>')


    color_preview.short_description = 'رنگ متن'


    def background_color_preview(self, obj):


        return mark_safe(f'<div style="width:30px;height:30px;background-color:{obj.background_color};border-radius:4px;border:1px solid #ddd;"></div>')


    background_color_preview.short_description = 'رنگ پس‌زمینه'
