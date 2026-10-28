import re


from django import template


from django.utils.safestring import mark_safe


register = template.Library()


@register.filter


def linkify(text):


    if not text:


        return text


    url_pattern = r'(http[s]?://\S+)'


    linked_text = re.sub(url_pattern, r'<a href="\1" target="_blank" style="color:var(--primary-color); text-decoration:underline;">\1</a>', text)


    simple_url_pattern = r'(?<!http://)(?<!https://)(www\.\S+)'


    linked_text = re.sub(simple_url_pattern, r'<a href="http://\1" target="_blank" style="color:var(--primary-color); text-decoration:underline;">\1</a>', linked_text)


    return mark_safe(linked_text)


@register.filter


def is_followed_by(user, current_user):


    if not current_user.is_authenticated:


        return False


    if user == current_user:


        return False


    from django.apps import apps


    try:


        Follow = apps.get_model('core', 'Follow')  


    except Exception:


        return False


    return Follow.objects.filter(follower=current_user, following=user).exists()


@register.filter


def unread_site_notifications_count(user):


    if not getattr(user, 'is_authenticated', False):


        return 0


    return user.site_notifications.filter(is_read=False).count()


@register.filter


def format_post_text(text):


    if not text:


        return text


    url_pattern = re.compile(r'(http[s]?://\S+|www\.\S+)')


    def replace_url(match):


        url = match.group(0)


        href = url if url.startswith(('http://', 'https://')) else f'http://{url}'


        return f'<a href="{href}" target="_blank" rel="noopener noreferrer" style="color:var(--primary-color); text-decoration:underline;">{url}</a>'


    text = url_pattern.sub(replace_url, text)


    tag_pattern = re.compile(r'(?<!\w)#([\wآ-یءئ]+)')


    def replace_tag(match):


        tag = match.group(1)


        return f'<a href="/hashtag/{tag}/" style="color:var(--primary-color); text-decoration:none; font-weight:600;">#{tag}</a>'


    text = tag_pattern.sub(replace_tag, text)


    return mark_safe(text)


