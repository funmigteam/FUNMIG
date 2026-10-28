

from django.shortcuts import render, redirect, get_object_or_404


from django.contrib.auth.decorators import login_required, user_passes_test


from django.contrib.auth import login


from django.contrib.auth.forms import UserCreationForm


from django.contrib.auth.models import User


from django.http import JsonResponse, StreamingHttpResponse, FileResponse, Http404, HttpResponse


from django.urls import reverse


from django.conf import settings
from django.core import signing


from django.views.decorators.http import require_http_methods


from django.views.decorators.csrf import csrf_exempt


from django.utils import timezone

from django.utils.dateparse import parse_datetime


from django.db.models import Count, Max, Q

from django.db import IntegrityError


from django.core.paginator import Paginator


from django.contrib import messages


from django.template.loader import render_to_string


import requests


import json


import re




import random


import os


import uuid


from urllib.parse import urlparse


from django.views.decorators.http import require_POST


from django.views.decorators.csrf import csrf_exempt


import json


import time




import requests


import jwt


from cryptography.hazmat.primitives import serialization


from cryptography.hazmat.primitives.asymmetric import ec


from cryptography.hazmat.backends import default_backend


from chat.models import ChatMessage as UserChatMessage
from .forms import BlogPostForm, CommentForm, CommunityForm, PostForm, ProfileForm
from .models import (
    Announcement,
    Banner,
    BlogMedia,
    BlogPost,
    Comment,
    Community,
    CommunityMembership,
    Follow,
    Hashtag,
    Like,
    Post,
    PostHashtag,
    PostMedia,
    PostView,
    PushSubscription,
    SavedPost,
    SiteNotification,
    TeamPortfolio,
    TeamPortfolioProject,
    Ticket,
    TicketReply,
    UserProfile,
)
from .push_notifications import send_push_notification, get_vapid_public_key
from .portfolio_i18n import translations_json
from .seo import (
    absolute_url,
    article_schema,
    build_seo,
    organization_schema,
    portfolio_schema,
    sitemap_url,
    website_schema,
)


HASHTAG_PATTERN = re.compile(r'(?<!\w)#([\w\u0600-\u06FF_]+)')
MENTION_PATTERN = re.compile(r'(?<!\w)@([A-Za-z0-9_]{3,150})')


def download_image_to_media(*args, **kwargs):
    return None

def robots_txt(request):

    host = request.get_host().split(':')[0].lower()
    sitemap_origin = 'https://funmig.com' if host in {'funmig.com', 'www.funmig.com'} else absolute_url('/')

    lines = [
        'User-agent: *',
        'Disallow: /secret/',
        'Disallow: /admin/',
        'Disallow: /api/',
        'Disallow: /payment/',
        'Disallow: /notifications/',
        'Disallow: /ticket/',
        'Disallow: /chat/',
        'Allow: /blog/',
        'Allow: /about/',
        'Allow: /install/',
        f'Sitemap: {sitemap_origin.rstrip("/")}{reverse("sitemap_xml")}',
    ]

    if host in {'funmig.com', 'www.funmig.com'}:
        lines.extend([
            '',
            'User-agent: GPTBot',
            'Disallow: /secret/',
            'Disallow: /admin/',
            'Disallow: /api/',
            'Allow: /',
            '',
            'User-agent: OAI-SearchBot',
            'Disallow: /secret/',
            'Disallow: /admin/',
            'Disallow: /api/',
            'Allow: /',
            '',
            'User-agent: ChatGPT-User',
            'Disallow: /secret/',
            'Disallow: /admin/',
            'Disallow: /api/',
            'Allow: /',
            '',
            'User-agent: Google-Extended',
            'Disallow: /secret/',
            'Disallow: /admin/',
            'Disallow: /api/',
            'Allow: /',
        ])

    return HttpResponse('\n'.join(lines) + '\n', content_type='text/plain; charset=utf-8')


def llms_txt(request):
    host = request.get_host().split(':')[0].lower()
    if host not in {'funmig.com', 'www.funmig.com'}:
        raise Http404
    content = """# FUNMIG

> FUNMIG is a bilingual Persian and English product design and web development team based in Mashhad, Iran.

Canonical website: https://funmig.com/
English version: https://funmig.com/en/
Social platform: https://social.funmig.com/
Package mirror: https://mirror.funmig.com/

## Services
- Custom website and web application development
- Social platform and marketplace development
- Django, API, database, PWA and admin dashboard engineering
- Artificial intelligence integration and workflow automation
- UX/UI design, technical SEO, performance and security
- Deployment, monitoring and ongoing technical support

## Contact
- Email: admin@funmig.com
- Telegram: https://t.me/FUNMIGweb

## فارسی
فان میگ یک تیم طراحی محصول، طراحی سایت، برنامه نویسی وب، توسعه شبکه اجتماعی و یکپارچه سازی هوش مصنوعی در مشهد است.
نسخه فارسی: https://funmig.com/
"""
    return HttpResponse(content.rstrip() + '\n', content_type='text/plain; charset=utf-8')


def sitemap_xml(request):

    host = request.get_host().split(':')[0].lower()
    if host in {'funmig.com', 'www.funmig.com'}:
        portfolio = TeamPortfolio.objects.filter(pk=1).first()
        urls = [
            sitemap_url(
                'https://funmig.com/',
                lastmod=portfolio.updated_at if portfolio else None,
                changefreq='weekly',
                priority='1.0',
            ),
            sitemap_url(
                'https://funmig.com/en/',
                lastmod=portfolio.updated_at if portfolio else None,
                changefreq='weekly',
                priority='0.9',
            ),
        ]
        xml = '\n'.join([
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            *urls,
            '</urlset>',
        ])
        return HttpResponse(xml, content_type='application/xml; charset=utf-8')

    urls = [
        sitemap_url(reverse('blog_list'), changefreq='daily', priority='0.9'),
        sitemap_url(reverse('about'), changefreq='monthly', priority='0.6'),
        sitemap_url(reverse('install'), changefreq='monthly', priority='0.5'),
    ]


    for post in BlogPost.objects.filter(status='published').order_by('-updated_at')[:1000]:

        urls.append(
            sitemap_url(
                post.get_absolute_url(),
                lastmod=post.updated_at,
                changefreq='weekly',
                priority='0.8',
            )
        )


    xml = '\n'.join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        *urls,
        '</urlset>',
    ])

    return HttpResponse(xml, content_type='application/xml; charset=utf-8')


def parse_admin_datetime(value):


    parsed = parse_datetime(value or '')


    if parsed and timezone.is_naive(parsed):


        return timezone.make_aware(parsed, timezone.get_current_timezone())


    return parsed


def activate_payment_request(*args, **kwargs):
    return None

def team_portfolio(request, language='fa'):


    portfolio, _ = TeamPortfolio.objects.get_or_create(pk=1)

    is_english = language == 'en'
    seo = build_seo(
        request,
        title='FUNMIG | Custom Web Development, AI and Product Design' if is_english else 'طراحی سایت و برنامه نویسی وب | تیم توسعه FUNMIG',
        description='FUNMIG designs and develops custom websites, social platforms, AI integrations, web applications, admin dashboards and PWAs.' if is_english else 'طراحی سایت اختصاصی، برنامه نویسی وب، ساخت شبکه اجتماعی، وب اپلیکیشن، پنل مدیریت و PWA با تمرکز بر سرعت، امنیت و تجربه کاربری.',
        path='https://funmig.com/en/' if is_english else 'https://funmig.com/',
        image='https://funmig.com/static/logo.png',
        keywords='FUNMIG, custom web development, website design, AI integration, social platform development, Django, PWA, admin dashboard, UX design, Iran web development' if is_english else 'طراحی سایت, برنامه نویسی, برنامه نویسی وب, سایت نویسی, ساخت سایت, طراحی وب سایت, توسعه وب, طراحی شبکه اجتماعی, ساخت شبکه اجتماعی, وب اپلیکیشن, طراحی پنل مدیریت, طراحی رابط کاربری, PWA, جنگو, تیم برنامه نویسی, شرکت طراحی سایت, فان میگ',
        modified_time=portfolio.updated_at,
    )

    response = render(request, 'team_portfolio.html', {
        'portfolio': portfolio,
        'seo': seo,
        'seo_json_ld': portfolio_schema(portfolio, language=language),
        'language': language,
        'is_english': is_english,
        'translations_json': translations_json(),
    })
    response.set_cookie('funmig_portfolio_language', language, max_age=31536000, samesite='Lax', secure=request.is_secure())
    return response


def team_portfolio_en(request):
    return team_portfolio(request, language='en')


def site_root(request):


    host = request.get_host().split(':')[0].lower()

    if host in {'funmig.com', 'www.funmig.com'}:
        if request.COOKIES.get('funmig_portfolio_language') == 'en':
            return redirect('/en/')
        return team_portfolio(request)

    return home(request)


def funmig_ai_redirect(request, path=''):
    if request.user.is_authenticated:
        return funmig_ai_sso(request, path)

    target = settings.FUNMIG_AI_URL
    if path:
        target = f'{target}/{path.strip("/")}/'
    query_string = request.META.get('QUERY_STRING')
    if query_string:
        target = f'{target}?{query_string}'
    return redirect(target)


def funmig_ai_sso(request, path=''):
    target_path = f'/{path.strip("/")}/' if path else '/'
    token = signing.dumps(
        {
            'user_id': request.user.pk,
            'username': request.user.get_username(),
        },
        salt='funmigai-sso',
        compress=True,
    )
    return redirect(f'{settings.FUNMIG_AI_URL}/sso/?token={token}&next={target_path}')


def extract_hashtags(text):


    tags = []


    seen = set()


    for raw_tag in HASHTAG_PATTERN.findall(text or ''):


        tag = raw_tag.strip('_').lower()


        if tag and tag not in seen:


            seen.add(tag)


            tags.append(tag)


    return tags


def sync_post_hashtags(post):


    tag_names = extract_hashtags(post.content)


    hashtags = []


    for tag_name in tag_names:


        hashtag, _ = Hashtag.objects.get_or_create(name=tag_name)


        hashtags.append(hashtag)


    PostHashtag.objects.filter(post=post).exclude(hashtag__in=hashtags).delete()


    for hashtag in hashtags:


        PostHashtag.objects.get_or_create(post=post, hashtag=hashtag)


    changed_ids = [tag.id for tag in hashtags]


    Hashtag.objects.filter(id__in=changed_ids).update(updated_at=timezone.now())


    for hashtag in hashtags:


        count = PostHashtag.objects.filter(hashtag=hashtag).count()


        if hashtag.post_count != count:


            Hashtag.objects.filter(id=hashtag.id).update(post_count=count)


def notify_user(recipient, actor, notification_type, title, message='', post=None, comment=None, url=''):


    if not recipient or (actor and recipient.id == actor.id):


        return None


    if not url:


        if post:


            url = f'/?post={post.id}#post-{post.id}'


        elif actor:


            url = reverse('profile', args=[actor.username])


    return SiteNotification.objects.create(


        recipient=recipient,


        actor=actor,


        notification_type=notification_type,


        title=title,


        message=message,


        post=post,


        comment=comment,


        url=url


    )


def notify_mentions(actor, text, post=None, comment=None):


    mentioned = set()


    for username in MENTION_PATTERN.findall(text or ''):


        if username in mentioned:


            continue


        mentioned.add(username)


        user = User.objects.filter(username__iexact=username).first()


        if user:


            notify_user(


                user,


                actor,


                'mention',


                f'{actor.username} شما را منشن کرد',


                (text or '')[:160],


                post=post,


                comment=comment


            )


def get_client_ip(request):


    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')


    if forwarded_for:


        return forwarded_for.split(',')[0].strip()


    return request.META.get('REMOTE_ADDR')


def signup(request):


    if request.method == 'POST':


        form = UserCreationForm(request.POST)


        if form.is_valid():


            user = form.save()


            UserProfile.objects.create(user=user)


            login(request, user)


            return redirect('home')


    else:


        form = UserCreationForm()


    return render(request, 'registration/signup.html', {'form': form})


def home(request):


    pinned_posts = Post.objects.filter(is_pinned=True).order_by('updated_at')


    posts_list = Post.objects.exclude(is_pinned=True).order_by('-created_at')


    paginator = Paginator(posts_list, 10)


    page_number = request.GET.get('page')


    page_obj = paginator.get_page(page_number)


                                                                           
    if request.method == 'POST' and not request.user.is_authenticated:


        return redirect(f"{reverse('login')}?next={request.get_full_path()}")


    if request.method == 'POST':


        form = PostForm(request.POST, request.FILES, user=request.user)


        if form.is_valid():


            post = form.save(commit=False)


            post.author = request.user


            parent_id = request.POST.get('parent_id')


            if parent_id:


                try:


                    parent_post = Post.objects.get(id=parent_id)


                    post.parent = parent_post


                except Post.DoesNotExist:


                    pass


            post.save()


            files = request.FILES.getlist('media') or request.FILES.getlist('image')


            for idx, f in enumerate(files):


                ctype = getattr(f, 'content_type', '') or f.name.lower()


                if 'video' in ctype:


                    mtype = 'video'


                elif 'audio' in ctype:


                    mtype = 'audio'


                else:


                    mtype = 'image'


                PostMedia.objects.create(post=post, file=f, media_type=mtype, order=idx, is_active=True)


            sync_post_hashtags(post)


            notify_mentions(request.user, post.content, post=post)


            if post.parent:


                notify_user(


                    post.parent.author,


                    request.user,


                    'reply',


                    f'{request.user.username} به پست شما پاسخ داد',


                    post.content[:160],


                    post=post


                )


            return redirect('home')


    elif request.user.is_authenticated:


        form = PostForm(user=request.user)


    else:


        form = None


    saved_post_ids = set()


    joined_communities = Community.objects.none()


    if request.user.is_authenticated:


        saved_post_ids = set(request.user.saved_posts.values_list('post_id', flat=True))


        joined_communities = Community.objects.filter(
            is_active=True,
            memberships__user=request.user
        ).order_by('name')


    return render(request, 'home.html', {


        'posts': page_obj,


        'pinned_posts': pinned_posts,


        'form': form,


        'page_obj': page_obj,


        'saved_post_ids': saved_post_ids,
        'joined_communities': joined_communities


    })


@login_required


def edit_post(request, post_id):


    post = get_object_or_404(Post, id=post_id, author=request.user)


    if request.method == 'POST':


        form = PostForm(request.POST, instance=post, user=request.user)


        if form.is_valid():


            post = form.save()


            sync_post_hashtags(post)


            notify_mentions(request.user, post.content, post=post)


            return redirect('home')


    else:


        form = PostForm(instance=post, user=request.user)


    return render(request, 'edit_post.html', {'form': form, 'post': post})


def post_detail(request, post_id):


    post = get_object_or_404(Post, id=post_id)


    comments = post.comments.filter(parent__isnull=True).select_related('author').prefetch_related('replies')


    recommended_posts = Post.objects.exclude(id=post.id).exclude(is_pinned=True).order_by('-created_at')[:6]

    first_media = post.active_media().filter(media_type='image').first()

    post_image = first_media.file.url if first_media else None


    return render(request, 'post_detail.html', {


        'post': post,


        'comments': comments,


        'recommended_posts': recommended_posts,
        'seo': build_seo(
            request,
            title=f'پست {post.author.username}',
            description=post.content or f'پست منتشر شده توسط {post.author.username} در فان میگ',
            image=post_image,
            type='article',
            robots='noindex,follow',
        ),


    })


@login_required


def like_post(request, post_id):


    data = {}


    if request.method == 'POST':


        post = get_object_or_404(Post, id=post_id)


        like, created = Like.objects.get_or_create(post=post, user=request.user)


        if not created:


            like.delete()


            data['liked'] = False


        else:


            data['liked'] = True


            notify_user(


                post.author,


                request.user,


                'like',


                f'{request.user.username} پست شما را لایک کرد',


                post.content[:160],


                post=post


            )


        data['likes_count'] = post.total_likes()


        return JsonResponse(data)


    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required


@require_POST


def track_post_view(request, post_id):


    post = get_object_or_404(Post, id=post_id)


    today = timezone.localdate()


    existing = PostView.objects.filter(post=post, viewed_at__date=today)


    if request.user.is_authenticated:


        existing = existing.filter(user=request.user)


    else:


        existing = existing.filter(user__isnull=True, ip_address=get_client_ip(request))


    created = False


    if not existing.exists():


        PostView.objects.create(


            post=post,


            user=request.user if request.user.is_authenticated else None,


            ip_address=get_client_ip(request)


        )


        created = True


    return JsonResponse({


        'success': True,


        'created': created,


        'views_count': post.total_views,


    })


@login_required


def add_comment(request, post_id):


    if request.method == 'POST':


        post = get_object_or_404(Post, id=post_id)


        form = CommentForm(request.POST)


        if form.is_valid():


            comment = form.save(commit=False)


            comment.post = post


            comment.author = request.user


            parent_id = request.POST.get('parent_id')


            if parent_id:


                parent_comment = get_object_or_404(Comment, id=parent_id)


                comment.parent = parent_comment


            comment.save()


            if comment.parent:


                notify_user(


                    comment.parent.author,


                    request.user,


                    'reply',


                    f'{request.user.username} به کامنت شما پاسخ داد',


                    comment.text[:160],


                    post=post,


                    comment=comment


                )


            else:


                notify_user(


                    post.author,


                    request.user,


                    'comment',


                    f'{request.user.username} برای پست شما کامنت گذاشت',


                    comment.text[:160],


                    post=post,


                    comment=comment


                )


            notify_mentions(request.user, comment.text, post=post, comment=comment)


            return JsonResponse({


                'success': True,


                'comment_id': comment.id,


                'author': comment.author.username,


                'text': comment.text,


                'parent_id': parent_id if parent_id else None,


                'total_comments': post.comments.count()


            })


        else:


            return JsonResponse({'success': False, 'errors': form.errors}, status=400)


    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required


def profile(request, username):


    user = get_object_or_404(User, username=username)


    profile, created = UserProfile.objects.get_or_create(user=user)


    posts_queryset = Post.objects.filter(author=user, parent=None).order_by('-created_at')


    posts_paginator = Paginator(posts_queryset, 10)


    posts = posts_paginator.get_page(request.GET.get('page'))


    post_replies = Post.objects.filter(parent__author=user).order_by('-created_at')


    is_following = False


    if request.user != user:


        is_following = Follow.objects.filter(


            follower=request.user,


            following=user


        ).exists()


    followers_count = user.followers.count()


    following_count = user.following.count()


    if profile.avatar:


        avatar_url = profile.avatar.url


    else:


        avatar_url = '/static/default-avatar.png'


    if request.method == 'POST' and request.user == user:


        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)


        if form.is_valid():


            form.save()


            return redirect('profile', username=username)


    else:


        form = ProfileForm(instance=profile, user=request.user) if request.user == user else None


    return render(request, 'profile.html', {


        'profile': profile,


        'posts': posts,


        'posts_page': posts,


        'post_replies': post_replies,


        'form': form,


        'avatar_url': avatar_url,


        'is_following': is_following,


        'followers_count': followers_count,


        'following_count': following_count,


        'profile_user': user,
        'seo': build_seo(
            request,
            title=f'پروفایل {user.username}',
            description=f'پروفایل {user.username} در فان میگ، پست ها و فعالیت های کاربر را ببینید.',
            image=avatar_url,
            robots='noindex,follow',
        ),


    })


@login_required


def pricing_plans(request):
    return funmig_ai_redirect(request, 'plans')

@login_required


def request_manual_payment(request):
    return funmig_ai_redirect(request, 'plans')

@csrf_exempt

def jibit_payment_callback(request):
    return funmig_ai_redirect(request, 'plans')

@login_required


def upload_receipt(request, pk):
    return funmig_ai_redirect(request, 'plans')

@user_passes_test(lambda u: u.is_staff)


@login_required


def admin_payment_requests(request):
    return funmig_ai_redirect(request, 'account')

@login_required


def ai_assistant(request):
    return funmig_ai_redirect(request)

@login_required


@require_http_methods(["POST"])


def create_new_chat(request):
    return funmig_ai_redirect(request, 'tools/chat')

@login_required


@require_http_methods(["POST"])


def delete_chat_session(request):
    return funmig_ai_redirect(request, 'tools/chat')

@login_required


@require_http_methods(["POST"])


def archive_chat_session(request):
    return funmig_ai_redirect(request, 'tools/chat')

@login_required


def get_session_messages(request, session_id):
    return funmig_ai_redirect(request, 'tools/chat')

@login_required


def clear_chat_history(request):
    return funmig_ai_redirect(request, 'tools/chat')

@login_required


def activate_trial(request):
    return funmig_ai_redirect(request, 'plans')

@login_required


def delete_post(request, post_id):


    if request.method == 'POST':


        post = get_object_or_404(Post, id=post_id)


        if post.author == request.user:


            post.delete()


            return JsonResponse({'success': True})


        else:


            return JsonResponse({'success': False, 'error': 'شما اجازه حذف این پست را ندارید'}, status=403)


    return JsonResponse({'success': False, 'error': 'درخواست نامعتبر'}, status=400)


@login_required


@require_POST


def toggle_save_post(request, post_id):


    post = get_object_or_404(Post, id=post_id)


    saved_post, created = SavedPost.objects.get_or_create(user=request.user, post=post)


    if created:


        action = 'saved'


        notify_user(


            post.author,


            request.user,


            'save',


            f'{request.user.username} پست شما را ذخیره کرد',


            post.content[:160],


            post=post


        )


    else:


        saved_post.delete()


        action = 'unsaved'


    saved_count = post.saved_by.count()


    return JsonResponse({'success': True, 'action': action, 'saved_count': saved_count})


@login_required


def saved_posts(request):


    saved_posts_list = Post.objects.filter(saved_by__user=request.user).order_by('-saved_by__created_at')


    return render(request, 'saved_posts.html', {


        'saved_posts': saved_posts_list


    })


def csrf_failure_redirect(request, reason=""):


    return redirect('home')


@login_required


def delete_comment(request, comment_id):


    comment = get_object_or_404(Comment, id=comment_id)


    if comment.author == request.user or comment.post.author == request.user:


        comment.delete()


        return JsonResponse({'success': True})


    return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)


def blog_list(request):


    selected_tag = request.GET.get('tag', '').strip()


    posts = BlogPost.objects.filter(status='published')


    if selected_tag:


        posts = posts.filter(tags__icontains=selected_tag)


    posts = posts.order_by('-created_at')


    random_post = posts.order_by('?').first() if posts.exists() else None


    context = {


        'posts': posts,


        'random_post': random_post,


        'selected_tag': selected_tag,
        'seo': build_seo(
            request,
            title='بلاگ فان میگ',
            description='آخرین مقاله ها، راهنماها و خبرهای فان میگ را در بلاگ بخوانید.',
            keywords='فان میگ, بلاگ, سرگرمی, شبکه اجتماعی',
        ),
        'seo_json_ld': website_schema(),


    }


    return render(request, 'blog_list.html', context)


def blog_detail(request, slug):


    post = get_object_or_404(BlogPost, slug=slug, status='published')


    related_posts = BlogPost.objects.filter(status='published').exclude(id=post.id)


    if post.tags:


        tags = [tag.strip() for tag in post.tags.split(',') if tag.strip()]


        related_query = Q()


        for tag in tags:


            related_query |= Q(tags__icontains=tag)


        related_posts = related_posts.filter(related_query)


    related_posts = related_posts.order_by('-created_at')[:3]


    context = {


        'post': post,


        'related_posts': related_posts,
        'seo': build_seo(
            request,
            title=post.title,
            description=post.excerpt,
            path=post.get_absolute_url(),
            image=post.image.url if post.image else None,
            type='article',
            keywords=post.tags,
            published_time=post.created_at,
            modified_time=post.updated_at,
        ),
        'seo_json_ld': article_schema(post),


    }


    return render(request, 'blog_detail.html', context)


@user_passes_test(lambda u: u.is_staff)


@login_required


def create_blog_post(request):


    if request.method == 'POST':


        form = BlogPostForm(request.POST, request.FILES)


        if form.is_valid():


            post = form.save(commit=False)


            post.author = request.user

            post.status = 'published'


            post.save()


            messages.success(request, 'مقاله با موفقیت ایجاد شد.')


            return redirect('blog_detail', slug=post.slug)


    else:


        form = BlogPostForm()


    return render(request, 'create_blog.html', {'form': form, 'page_title': 'نوشتن مقاله جدید'})


@user_passes_test(lambda u: u.is_staff)

@login_required

@require_POST

def upload_blog_media(request):


    media_file = request.FILES.get('file')


    if not media_file:


        return JsonResponse({'success': False, 'error': 'فایلی انتخاب نشده است.'}, status=400)


    image_types = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}


    audio_types = {'audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/x-wav', 'audio/ogg', 'audio/webm'}


    if media_file.content_type in image_types:


        media_type = 'image'


    elif media_file.content_type in audio_types:


        media_type = 'audio'


    else:


        return JsonResponse({'success': False, 'error': 'فقط عکس و فایل صوتی مجاز است.'}, status=400)


    if media_file.size > 20 * 1024 * 1024:


        return JsonResponse({'success': False, 'error': 'حجم فایل نباید بیشتر از ۲۰ مگابایت باشد.'}, status=400)


    media = BlogMedia.objects.create(


        uploader=request.user,


        file=media_file,


        media_type=media_type,


    )


    return JsonResponse({


        'success': True,


        'url': media.file.url,


        'media_type': media.media_type,


        'name': os.path.basename(media.file.name),


    })


@user_passes_test(lambda u: u.is_staff)


@login_required


def delete_blog_post(request, slug):


    post = get_object_or_404(BlogPost, slug=slug)


    if request.method == 'POST':


        post.delete()


        messages.success(request, 'مقاله با موفقیت حذف شد.')


        return redirect('blog_list')


    return render(request, 'confirm_delete_blog.html', {'post': post})


@login_required


@require_http_methods(["POST"])


def upload_file_temp(request):


    if 'file' not in request.FILES:


        return JsonResponse({'success': False, 'error': 'فایلی ارسال نشده است'}, status=400)


    file = request.FILES['file']


    temp_path = os.path.join(settings.MEDIA_ROOT, 'temp')


    if not os.path.exists(temp_path):


        os.makedirs(temp_path)


    ext = file.name.split('.')[-1]


    filename = f"{uuid.uuid4().hex}.{ext}"


    filepath = os.path.join(temp_path, filename)


    with open(filepath, 'wb+') as destination:


        for chunk in file.chunks():


            destination.write(chunk)


    return JsonResponse({'success': True, 'filename': filename})


@login_required


def create_post_with_file(request):


    if request.method == 'POST':


        content = request.POST.get('content')


        temp_filename = request.POST.get('temp_filename')


        parent_id = request.POST.get('parent_id')

        community = Community.objects.filter(
            id=request.POST.get('community'),
            is_active=True,
            memberships__user=request.user
        ).first()


        post = Post(author=request.user, content=content, community=community)


        if temp_filename:


            temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', temp_filename)


            if os.path.exists(temp_path):


                final_path = os.path.join(settings.MEDIA_ROOT, 'posts', temp_filename)


                if not os.path.exists(os.path.dirname(final_path)):


                    os.makedirs(os.path.dirname(final_path))


                os.rename(temp_path, final_path)


                ext = os.path.splitext(temp_filename)[1].lower()


                if ext in ['.mp4', '.mov', '.webm']:


                    mtype = 'video'


                elif ext in ['.mp3', '.wav', '.ogg']:


                    mtype = 'audio'


                else:


                    mtype = 'image'


                post.save()


                pm = PostMedia(post=post, media_type=mtype, order=0, is_active=True)


                pm.file.name = os.path.join('posts', temp_filename)


                pm.save()


        else:


            post.save()


        if parent_id:


            try:


                post.parent = Post.objects.get(id=parent_id)


            except Post.DoesNotExist:


                pass


        post.save()


        sync_post_hashtags(post)


        notify_mentions(request.user, post.content, post=post)


        if post.parent:


            notify_user(


                post.parent.author,


                request.user,


                'reply',


                f'{request.user.username} به پست شما پاسخ داد',


                post.content[:160],


                post=post


            )


        if request.headers.get('x-requested-with') == 'XMLHttpRequest':


            return JsonResponse({'success': True, 'post_id': post.id})


        else:


            return redirect('home')


    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def load_more_posts(request):


    page_number = request.GET.get('page', 1)


    posts = Post.objects.exclude(is_pinned=True).order_by('-created_at')


    paginator = Paginator(posts, 5)


    page_obj = paginator.get_page(page_number)


    posts_html = ""


    for post in page_obj:


        posts_html += render_to_string('post_card.html', {'post': post, 'user': request.user})


    return JsonResponse({


        'posts_html': posts_html,


        'has_next': page_obj.has_next()


    })


@login_required


def check_new_posts(request):


    last_post_id = request.GET.get('last_post_id', 0)


    new_posts = Post.objects.filter(id__gt=last_post_id).exclude(is_pinned=True).order_by('-created_at')


    posts_html = ""


    for post in new_posts:


        posts_html += render_to_string('post_card.html', {'post': post, 'user': request.user})


    return JsonResponse({


        'posts_html': posts_html,


        'count': new_posts.count()


    })


@login_required


def create_post_ajax(request):


    if request.method == 'POST':


        form = PostForm(request.POST, request.FILES, user=request.user)


        if form.is_valid():


            post = form.save(commit=False)


            post.author = request.user


            def render_post_response(saved_post, duplicate=False):

                post_html = render_to_string('post_card.html', {'post': saved_post, 'user': request.user})

                data = {'success': True, 'post_id': saved_post.id, 'post_html': post_html}

                if duplicate:

                    data['duplicate'] = True

                return JsonResponse(data)


            parent_id = request.POST.get('parent_id')


            if parent_id:


                try:


                    parent_post = Post.objects.get(id=parent_id)


                    post.parent = parent_post


                except Post.DoesNotExist:


                    pass


            temp_filename = request.POST.get('temp_filename')

            submission_token = request.POST.get('submission_token', '').strip()

            if submission_token:

                try:

                    post.submission_token = uuid.UUID(submission_token)

                except ValueError:

                    post.submission_token = None


            if post.submission_token:

                existing_post = Post.objects.filter(
                    author=request.user,
                    submission_token=post.submission_token
                ).first()

                if existing_post:

                    return render_post_response(existing_post, duplicate=True)


            duplicate_query = Post.objects.filter(


                author=request.user,


                content=post.content,


                parent=post.parent,


                community=post.community,


                created_at__gte=timezone.now() - timezone.timedelta(seconds=5)


            )


            if temp_filename:


                duplicate_query = duplicate_query.filter(media__file__endswith=temp_filename)


            recent_duplicate = duplicate_query.order_by('-created_at').first()


            if recent_duplicate:

                return render_post_response(recent_duplicate, duplicate=True)


            try:

                post.save()

            except IntegrityError:

                if post.submission_token:

                    existing_post = Post.objects.filter(
                        author=request.user,
                        submission_token=post.submission_token
                    ).first()

                    if existing_post:

                        return render_post_response(existing_post, duplicate=True)

                raise


            if temp_filename:


                temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', temp_filename)


                if os.path.exists(temp_path):


                    final_path = os.path.join(settings.MEDIA_ROOT, 'posts', temp_filename)


                    if not os.path.exists(os.path.dirname(final_path)):


                        os.makedirs(os.path.dirname(final_path))


                    os.rename(temp_path, final_path)


                    ext = os.path.splitext(temp_filename)[1].lower()


                    if ext in ['.mp4', '.mov', '.webm']:


                        mtype = 'video'


                    elif ext in ['.mp3', '.wav', '.ogg']:


                        mtype = 'audio'


                    else:


                        mtype = 'image'


                    pm = PostMedia(post=post, media_type=mtype, order=0, is_active=True)


                    pm.file.name = os.path.join('posts', temp_filename)


                    pm.save()


            else:


                files = request.FILES.getlist('media') or request.FILES.getlist('image')


                for idx, f in enumerate(files):


                    ctype = getattr(f, 'content_type', '') or f.name.lower()


                    if 'video' in ctype:


                        mtype = 'video'


                    elif 'audio' in ctype:


                        mtype = 'audio'


                    else:


                        mtype = 'image'


                    PostMedia.objects.create(post=post, file=f, media_type=mtype, order=idx, is_active=True)


            sync_post_hashtags(post)


            notify_mentions(request.user, post.content, post=post)


            if post.parent:


                notify_user(


                    post.parent.author,


                    request.user,


                    'reply',


                    f'{request.user.username} به پست شما پاسخ داد',


                    post.content[:160],


                    post=post


                )


            return render_post_response(post)


        else:


            return JsonResponse({'success': False, 'errors': form.errors}, status=400)


    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def handle_streaming_error(request, message):


    if request.headers.get('x-requested-with') == 'XMLHttpRequest':


        def error_gen():


            yield message


        return StreamingHttpResponse(error_gen(), content_type='text/plain')


    else:


        return funmig_ai_redirect(request)


@login_required


def create_ticket(request):


    if request.method == 'POST':


        subject = request.POST.get('subject')


        message = request.POST.get('message')


        if subject and message:


            Ticket.objects.create(user=request.user, subject=subject, message=message)


            messages.success(request, 'تیکت شما با موفقیت ارسال شد.')


            return redirect('ticket_list')


        else:


            messages.error(request, 'لطفاً همه فیلدها را پر کنید.')


    return render(request, 'create_ticket.html')


@login_required


def ticket_list(request):


    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')


    return render(request, 'ticket_list.html', {'tickets': tickets})


@login_required


def ticket_detail(request, ticket_id):


    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)


    replies = ticket.replies.all().order_by('created_at')


    if request.method == 'POST':


        message = request.POST.get('message')


        if message:


            TicketReply.objects.create(ticket=ticket, user=request.user, message=message, is_admin=False)


            messages.success(request, 'پاسخ شما ارسال شد.')


            return redirect('ticket_detail', ticket_id=ticket.id)


    return render(request, 'ticket_detail.html', {'ticket': ticket, 'replies': replies})


@user_passes_test(lambda u: u.is_staff)


@login_required


def admin_ticket_list(request):


    tickets = Ticket.objects.all().order_by('-created_at')


    return render(request, 'admin_ticket_list.html', {'tickets': tickets})


@user_passes_test(lambda u: u.is_staff)


@login_required


def admin_ticket_detail(request, ticket_id):


    ticket = get_object_or_404(Ticket, id=ticket_id)


    replies = ticket.replies.all().order_by('created_at')


    if request.method == 'POST':


        action = request.POST.get('action')


        if action == 'reply':


            message = request.POST.get('message')


            if message:


                TicketReply.objects.create(ticket=ticket, user=request.user, message=message, is_admin=True)


                messages.success(request, 'پاسخ ادمین ارسال شد.')


                return redirect('admin_ticket_detail', ticket_id=ticket.id)


        elif action == 'close':


            ticket.status = 'closed'


            ticket.save()


            messages.success(request, 'تیکت بسته شد.')


            return redirect('admin_ticket_detail', ticket_id=ticket.id)


        elif action == 'reopen':


            ticket.status = 'open'


            ticket.save()


            messages.success(request, 'تیکت مجدداً باز شد.')


            return redirect('admin_ticket_detail', ticket_id=ticket.id)


    return render(request, 'admin_ticket_detail.html', {'ticket': ticket, 'replies': replies})


@user_passes_test(lambda u: u.is_staff)


@login_required


def delete_ticket(request, ticket_id):


    ticket = get_object_or_404(Ticket, id=ticket_id)


    if request.method == 'POST':


        ticket.delete()


        messages.success(request, 'تیکت حذف شد.')


        return redirect('admin_ticket_list')


    return render(request, 'confirm_delete_ticket.html', {'ticket': ticket})


@login_required


def save_user_info(request):
    return funmig_ai_redirect(request, 'account')

@login_required


def get_user_tokens(request):
    return funmig_ai_redirect(request, 'account')

def load_more_posts(request):


    page_number = request.GET.get('page', 1)


    posts_list = Post.objects.exclude(is_pinned=True).order_by('-created_at')


    paginator = Paginator(posts_list, 10)


    page_obj = paginator.get_page(page_number)


    posts_html = ""


    for post in page_obj:


        posts_html += render_to_string('post_card.html', {'post': post, 'user': request.user})


    return JsonResponse({


        'posts_html': posts_html,


        'has_next': page_obj.has_next(),


        'current_page': page_obj.number,


        'total_pages': paginator.num_pages


    })


def about(request):


    stats = {
        'active_users_count': User.objects.filter(is_active=True).count(),
        'posts_count': Post.objects.count(),
        'messages_count': UserChatMessage.objects.count(),
        'seo': build_seo(
            request,
            title='درباره فان میگ',
            description='با فان میگ، امکانات شبکه اجتماعی، چت، بلاگ و ترندهای آن آشنا شوید.',
        ),
        'seo_json_ld': organization_schema(),
    }


    return render(request, 'about.html', stats)


@login_required


def notifications_center(request):


    notifications = SiteNotification.objects.filter(recipient=request.user).select_related(


        'actor', 'post', 'comment'


    )


    unread_count = notifications.filter(is_read=False).count()


    if request.method == 'POST':


        action = request.POST.get('action')


        if action == 'mark_all_read':


            notifications.filter(is_read=False).update(is_read=True)


            return redirect('notifications_center')


        if action == 'clear_read':


            notifications.filter(is_read=True).delete()


            return redirect('notifications_center')


    paginator = Paginator(notifications, 20)


    page_obj = paginator.get_page(request.GET.get('page'))


    return render(request, 'notifications_center.html', {


        'notifications': page_obj,


        'page_obj': page_obj,


        'unread_count': unread_count,


    })


@login_required


def mark_notification_read(request, notification_id):


    notification = get_object_or_404(SiteNotification, id=notification_id, recipient=request.user)


    notification.is_read = True


    notification.save(update_fields=['is_read'])


    return redirect(notification.url or 'notifications_center')


@login_required


def explore(request):


    following_ids = set(request.user.following.values_list('following_id', flat=True))


    user_interests = request.user.userprofile.interests or ''


    interest_terms = [term.strip() for term in re.split(r'[,،؛]+', user_interests) if term.strip()]


    post_query = Q(parent=None)


    for term in interest_terms:


        post_query |= Q(content__icontains=term)


    suggested_posts = Post.objects.filter(post_query).exclude(author=request.user).annotate(


        likes_count=Count('like'),


        comments_count=Count('comments'),


        saves_count=Count('saved_by'),


    ).order_by('-likes_count', '-comments_count', '-created_at')[:12]


    suggested_users = User.objects.exclude(id=request.user.id).exclude(id__in=following_ids).annotate(


        followers_count=Count('followers'),


        posts_count=Count('post'),


        latest_post=Max('post__created_at'),


    ).order_by('-followers_count', '-latest_post')[:10]


    trending_tags = Hashtag.objects.filter(post_count__gt=0).order_by('-post_count', '-updated_at')[:15]


    recent_posts = Post.objects.filter(parent=None).order_by('-created_at')[:8]


    return render(request, 'explore.html', {


        'suggested_posts': suggested_posts,


        'suggested_users': suggested_users,


        'trending_tags': trending_tags,


        'recent_posts': recent_posts,
        'seo': build_seo(
            request,
            title='اکسپلور فان میگ',
            description='پست ها، کاربران و هشتگ های پیشنهادی فان میگ را کشف کنید.',
            robots='noindex,follow',
        ),


    })


@login_required


def hashtag_detail(request, tag_name):


    hashtag = get_object_or_404(Hashtag, name__iexact=tag_name.lower())


    posts_list = Post.objects.filter(post_hashtags__hashtag=hashtag).select_related('author').order_by('-created_at')


    paginator = Paginator(posts_list, 10)


    page_obj = paginator.get_page(request.GET.get('page'))


    return render(request, 'hashtag_detail.html', {


        'hashtag': hashtag,


        'posts': page_obj,


        'page_obj': page_obj,
        'seo': build_seo(
            request,
            title=f'#{hashtag.name}',
            description=f'پست های مرتبط با هشتگ #{hashtag.name} در فان میگ.',
            robots='noindex,follow',
        ),


    })


@login_required


def trending(request):


    tags = Hashtag.objects.filter(post_count__gt=0).order_by('-post_count', '-updated_at')[:50]


    posts = Post.objects.filter(parent=None).annotate(


        likes_count=Count('like'),


        comments_count=Count('comments'),


        saves_count=Count('saved_by'),


    ).order_by('-likes_count', '-comments_count', '-saves_count', '-created_at')[:20]


    return render(request, 'trending.html', {


        'tags': tags,


        'posts': posts,
        'seo': build_seo(
            request,
            title='ترندهای فان میگ',
            description='هشتگ ها و پست های محبوب و پرتعامل فان میگ را دنبال کنید.',
            robots='noindex,follow',
        ),


    })


@login_required

def community_list(request):


    query = (request.GET.get('q') or '').strip()

    communities = Community.objects.filter(is_active=True).annotate(
        member_count=Count('memberships', distinct=True),
        posts_count=Count('posts', distinct=True)
    )


    if query:

        communities = communities.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )


    joined_ids = set(
        CommunityMembership.objects.filter(user=request.user).values_list(
            'community_id', flat=True
        )
    )


    return render(request, 'communities/list.html', {
        'communities': communities,
        'joined_ids': joined_ids,
        'query': query,
        'seo': build_seo(
            request,
            title='انجمن های فان میگ',
            description='انجمن های فعال فان میگ را پیدا کنید و به گفتگوهای مورد علاقه تان بپیوندید.',
            robots='noindex,follow',
        ),
    })


@login_required

def community_create(request):


    if request.method == 'POST':

        form = CommunityForm(request.POST, request.FILES)

        if form.is_valid():

            community = form.save(commit=False)

            community.owner = request.user

            community.save()

            CommunityMembership.objects.create(
                community=community,
                user=request.user,
                role=CommunityMembership.ROLE_MODERATOR
            )

            messages.success(request, 'انجمن با موفقیت ساخته شد.')

            return redirect('community_detail', slug=community.slug)

    else:

        form = CommunityForm()


    return render(request, 'communities/create.html', {'form': form})


@login_required

def community_detail(request, slug):


    community = get_object_or_404(Community, slug=slug, is_active=True)

    membership = CommunityMembership.objects.filter(
        community=community,
        user=request.user
    ).first()


    if request.method == 'POST':

        if not membership:

            messages.error(request, 'برای انتشار پست ابتدا عضو انجمن شوید.')

            return redirect('community_detail', slug=community.slug)


        form = PostForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():

            post = form.save(commit=False)

            post.author = request.user

            post.community = community

            post.save()


            files = request.FILES.getlist('media') or request.FILES.getlist('image')

            for idx, uploaded_file in enumerate(files):

                content_type = getattr(uploaded_file, 'content_type', '') or uploaded_file.name.lower()

                if 'video' in content_type:

                    media_type = 'video'

                elif 'audio' in content_type:

                    media_type = 'audio'

                else:

                    media_type = 'image'

                PostMedia.objects.create(
                    post=post,
                    file=uploaded_file,
                    media_type=media_type,
                    order=idx,
                    is_active=True
                )


            sync_post_hashtags(post)

            notify_mentions(request.user, post.content, post=post)

            messages.success(request, 'پست شما در انجمن منتشر شد.')

            return redirect('community_detail', slug=community.slug)

    else:

        form = PostForm(user=request.user, initial={'community': community})


    posts = community.posts.filter(parent__isnull=True).select_related(
        'author', 'author__userprofile', 'community'
    ).order_by('-is_pinned', '-created_at')

    page_obj = Paginator(posts, 10).get_page(request.GET.get('page'))


    return render(request, 'communities/detail.html', {
        'community': community,
        'membership': membership,
        'form': form,
        'posts': page_obj,
        'member_count': community.memberships.count(),
        'recent_members': community.members.select_related('userprofile')[:8],
        'seo': build_seo(
            request,
            title=community.name,
            description=community.description,
            image=community.cover.url if community.cover else None,
            robots='noindex,follow',
        ),
    })


@login_required

@require_POST

def community_join(request, slug):


    community = get_object_or_404(Community, slug=slug, is_active=True)

    CommunityMembership.objects.get_or_create(
        community=community,
        user=request.user
    )

    messages.success(request, f'عضو انجمن {community.name} شدید.')

    return redirect('community_detail', slug=community.slug)


@login_required

@require_POST

def community_leave(request, slug):


    community = get_object_or_404(Community, slug=slug, is_active=True)

    if community.owner_id == request.user.id:

        messages.error(request, 'سازنده انجمن نمی‌تواند از انجمن خارج شود.')

    else:

        CommunityMembership.objects.filter(
            community=community,
            user=request.user
        ).delete()

        messages.success(request, f'از انجمن {community.name} خارج شدید.')

    return redirect('community_detail', slug=community.slug)


@user_passes_test(lambda u: u.is_staff)

def manage_banner(request):


    if request.method == 'POST':


        action = request.POST.get('action')


        if action == 'create':


            Banner.objects.create(


                title=request.POST.get('title'),


                description=request.POST.get('description'),


                link=request.POST.get('link'),


                image=request.FILES.get('image'),


                placement=request.POST.get('placement') or 'site_top',


                background_color=request.POST.get('background_color'),


                text_color=request.POST.get('text_color'),


                is_active=request.POST.get('is_active') == 'on',


                is_dismissible=request.POST.get('is_dismissible') == 'on',


                starts_at=parse_admin_datetime(request.POST.get('starts_at')),


                ends_at=parse_admin_datetime(request.POST.get('ends_at')),


                created_by=request.user


            )


            return JsonResponse({'success': True, 'message': 'تبلیغ جدید اضافه شد'})


        elif action == 'update':


            banner_id = request.POST.get('banner_id')


            banner = get_object_or_404(Banner, id=banner_id)


            banner.title = request.POST.get('title')


            banner.description = request.POST.get('description')


            banner.link = request.POST.get('link')


            if request.FILES.get('image'):


                banner.image = request.FILES.get('image')


            banner.placement = request.POST.get('placement') or 'site_top'


            banner.background_color = request.POST.get('background_color')


            banner.text_color = request.POST.get('text_color')


            banner.is_active = request.POST.get('is_active') in ['true', 'on']


            banner.is_dismissible = request.POST.get('is_dismissible') in ['true', 'on']


            banner.starts_at = parse_admin_datetime(request.POST.get('starts_at'))


            banner.ends_at = parse_admin_datetime(request.POST.get('ends_at'))


            banner.save()


            return JsonResponse({'success': True, 'message': 'تبلیغ ویرایش شد'})


        elif action == 'delete':


            banner_id = request.POST.get('banner_id')


            banner = get_object_or_404(Banner, id=banner_id)


            banner.delete()


            return JsonResponse({'success': True, 'message': 'بنر حذف شد'})


    banners = Banner.objects.all()


    return render(request, 'admin/manage_banner.html', {'banners': banners})


def get_active_banner(request):


    dismiss_id = request.GET.get('dismiss')


    if dismiss_id:


        request.session['dismissed_banner_id'] = dismiss_id


        return JsonResponse({'success': True})


    dismissed_id = request.session.get('dismissed_banner_id')


    now = timezone.now()


    active_banners = Banner.objects.filter(
        is_active=True,
        placement='site_top'
    ).filter(
        Q(starts_at__isnull=True) | Q(starts_at__lte=now),
        Q(ends_at__isnull=True) | Q(ends_at__gte=now)
    ).order_by('-created_at')


    if dismissed_id:


        active_banners = active_banners.exclude(id=dismissed_id)


    if active_banners.exists():


        banners_data = []


        for b in active_banners:


            banners_data.append({


                'id': b.id,


                'title': b.title,


                'description': b.description,


                'link': b.link,


                'image': b.image.url if b.image else '',


                'background_color': b.background_color,


                'text_color': b.text_color,


                'is_dismissible': b.is_dismissible


            })


        return JsonResponse({'exists': True, 'banners': banners_data})


    return JsonResponse({'exists': False})


@user_passes_test(lambda u: u.is_staff)

def manage_announcements(request):


    if request.method == 'POST':


        action = request.POST.get('action')


        if action == 'create':


            Announcement.objects.create(
                title=request.POST.get('title'),
                message=request.POST.get('message'),
                announcement_type=request.POST.get('announcement_type') or Announcement.TYPE_INFO,
                link=request.POST.get('link') or None,
                link_label=request.POST.get('link_label') or 'جزئیات',
                is_active=request.POST.get('is_active') == 'on',
                is_dismissible=request.POST.get('is_dismissible') == 'on',
                starts_at=parse_admin_datetime(request.POST.get('starts_at')),
                ends_at=parse_admin_datetime(request.POST.get('ends_at')),
                created_by=request.user
            )


            return JsonResponse({'success': True, 'message': 'اعلامیه جدید اضافه شد'})


        if action == 'delete':


            announcement_id = request.POST.get('announcement_id')


            announcement = get_object_or_404(Announcement, id=announcement_id)


            announcement.delete()


            return JsonResponse({'success': True, 'message': 'اعلامیه حذف شد'})


        if action == 'toggle':


            announcement_id = request.POST.get('announcement_id')


            announcement = get_object_or_404(Announcement, id=announcement_id)


            announcement.is_active = not announcement.is_active


            announcement.save(update_fields=['is_active', 'updated_at'])


            return JsonResponse({'success': True, 'message': 'وضعیت اعلامیه تغییر کرد'})


    announcements = Announcement.objects.all()


    return render(request, 'admin/manage_announcements.html', {'announcements': announcements})


def get_active_announcement(request):


    dismiss_id = request.GET.get('dismiss')


    if dismiss_id:


        request.session['dismissed_announcement_id'] = dismiss_id


        return JsonResponse({'success': True})


    dismissed_id = request.session.get('dismissed_announcement_id')


    now = timezone.now()


    announcements = Announcement.objects.filter(is_active=True).filter(
        Q(starts_at__isnull=True) | Q(starts_at__lte=now),
        Q(ends_at__isnull=True) | Q(ends_at__gte=now)
    ).order_by('-created_at')


    if dismissed_id:


        announcements = announcements.exclude(id=dismissed_id)


    announcement = announcements.first()


    if not announcement:


        return JsonResponse({'exists': False})


    return JsonResponse({
        'exists': True,
        'announcement': {
            'id': announcement.id,
            'title': announcement.title,
            'message': announcement.message,
            'announcement_type': announcement.announcement_type,
            'link': announcement.link,
            'link_label': announcement.link_label,
            'is_dismissible': announcement.is_dismissible,
        }
    })


@user_passes_test(lambda u: u.is_staff)


def edit_blog_post(request, slug):


    post = get_object_or_404(BlogPost, slug=slug)


    if request.method == 'POST':


        form = BlogPostForm(request.POST, request.FILES, instance=post)


        if form.is_valid():


            post = form.save(commit=False)

            post.status = 'published'

            post.save()


            messages.success(request, 'مقاله با موفقیت ویرایش شد!')


            return redirect('blog_detail', slug=post.slug)


    else:


        form = BlogPostForm(instance=post)


    return render(request, 'blog_edit.html', {'form': form, 'post': post, 'page_title': 'ویرایش مقاله'})


@login_required


@require_http_methods(["POST"])


def follow_user(request, username):


    try:


        user_to_follow = User.objects.get(username=username)


        if user_to_follow == request.user:


            return JsonResponse({


                'success': False,


                'error': 'نمی‌توانید خودتان را فالو کنید'


            }, status=400)


        follow, created = Follow.objects.get_or_create(


            follower=request.user,


            following=user_to_follow


        )


        if created:


            notify_user(


                user_to_follow,


                request.user,


                'follow',


                f'{request.user.username} شما را فالو کرد',


                url=reverse('profile', args=[request.user.username])


            )


            return JsonResponse({


                'success': True,


                'action': 'followed',


                'followers_count': user_to_follow.followers.count()


            })


        else:


            return JsonResponse({


                'success': False,


                'error': 'شما قبلاً این کاربر را فالو کرده‌اید'


            }, status=400)


    except User.DoesNotExist:


        return JsonResponse({


            'success': False,


            'error': 'کاربر یافت نشد'


        }, status=404)


@login_required


@require_http_methods(["POST"])


def unfollow_user(request, username):


    try:


        user_to_unfollow = User.objects.get(username=username)


        follow = Follow.objects.filter(


            follower=request.user,


            following=user_to_unfollow


        ).first()


        if follow:


            follow.delete()


            return JsonResponse({


                'success': True,


                'action': 'unfollowed',


                'followers_count': user_to_unfollow.followers.count()


            })


        else:


            return JsonResponse({


                'success': False,


                'error': 'شما این کاربر را فالو نکرده‌اید'


            }, status=400)


    except User.DoesNotExist:


        return JsonResponse({


            'success': False,


            'error': 'کاربر یافت نشد'


        }, status=404)


@login_required


def followers_list(request, username):


    user = get_object_or_404(User, username=username)


    followers = user.followers.all()


    paginator = Paginator(followers, 20)


    page_number = request.GET.get('page')


    page_obj = paginator.get_page(page_number)


    return render(request, 'followers_list.html', {


        'profile_user': user,


        'followers': page_obj,


        'page_obj': page_obj,


        'type': 'followers'


    })


@login_required


def following_list(request, username):


    user = get_object_or_404(User, username=username)


    following = user.following.all()


    paginator = Paginator(following, 20)


    page_number = request.GET.get('page')


    page_obj = paginator.get_page(page_number)


    return render(request, 'followers_list.html', {


        'profile_user': user,


        'following': page_obj,


        'page_obj': page_obj,


        'type': 'following'


    })


@login_required


def search(request):


    query = request.GET.get('q', '').strip()


    search_type = request.GET.get('type', 'posts')  


    users_results = []


    posts_results = []


    if query:


        if query.startswith('#'):


            real_query = query[1:]


            search_type = 'posts'


            posts_results = Post.objects.filter(


                Q(content__icontains=real_query) |


                Q(content__icontains=f'#{real_query}') |


                Q(post_hashtags__hashtag__name__iexact=real_query.lower())


            ).order_by('-created_at')[:50]


        elif search_type == 'users':


            users_results = User.objects.filter(


                Q(username__icontains=query) |


                Q(first_name__icontains=query) |


                Q(last_name__icontains=query)


            ).exclude(id=request.user.id).distinct()[:20]


        else:


            posts_results = Post.objects.filter(


                Q(content__icontains=query)


            ).order_by('-created_at')[:50]


    return render(request, 'search.html', {


        'query': query,


        'users_results': users_results,


        'posts_results': posts_results,


        'search_type': search_type


    })


@login_required


@require_POST


def subscribe_push(request):


    try:


        data = json.loads(request.body)


        subscription_data = data.get('subscription', {})


        if not subscription_data:


            return JsonResponse({'error': 'No subscription data'}, status=400)


        PushSubscription.objects.filter(user=request.user).delete()


        PushSubscription.objects.create(


            user=request.user,


            subscription_data=subscription_data


        )


        return JsonResponse({'success': True})


    except Exception as e:


        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt


@require_POST


def unsubscribe_push(request):


    if request.user.is_authenticated:


        PushSubscription.objects.filter(user=request.user).delete()


        return JsonResponse({'success': True})


    return JsonResponse({'error': 'Unauthorized'}, status=401)


def install(request):


    return render(request, 'install.html', {
        'seo': build_seo(
            request,
            title='نصب اپلیکیشن فان میگ',
            description='اپلیکیشن فان میگ را نصب کنید و سریع تر به شبکه اجتماعی، چت و بلاگ دسترسی داشته باشید.',
        )
    })


def download_android_apk(request):


    apk_paths = [
        os.path.join(settings.STATIC_ROOT, 'FUNMIG.apk'),
        os.path.join(settings.BASE_DIR, 'static', 'FUNMIG.apk'),
    ]


    for apk_path in apk_paths:

        if os.path.exists(apk_path):

            return FileResponse(
                open(apk_path, 'rb'),
                as_attachment=True,
                filename='FUNMIG.apk',
                content_type='application/vnd.android.package-archive',
            )


    raise Http404('Android application file was not found.')
