import json

import re

from html import escape

from urllib.parse import urljoin


from django.conf import settings

from django.templatetags.static import static

from django.urls import reverse

from django.utils.html import strip_tags


SITE_NAME = 'FUNMIG'

DEFAULT_TITLE = 'FUNMIG | شبکه اجتماعی سرگرمی، بلاگ و چت'

DEFAULT_DESCRIPTION = (
    'فان میگ فضایی برای اشتراک گذاری پست، دنبال کردن ترندها، خواندن مقاله های تازه '
    'و گفت وگو با دوستان است.'
)


def plain_text(value, limit=160):

    text = strip_tags(value or '')

    text = re.sub(r'\s+', ' ', text).strip()

    if len(text) <= limit:

        return text

    return text[:limit - 1].rstrip() + '…'


def site_url():

    return getattr(settings, 'SITE_URL', 'https://social.funmig.com').rstrip('/')


def absolute_url(path_or_url):

    if not path_or_url:

        return ''

    if str(path_or_url).startswith(('http://', 'https://')):

        return str(path_or_url)

    return urljoin(site_url() + '/', str(path_or_url).lstrip('/'))


def default_image_url():

    return absolute_url(static('logo.png'))


def build_seo(
    request=None,
    title=None,
    description=None,
    path=None,
    image=None,
    type='website',
    robots='index,follow',
    keywords=None,
    published_time=None,
    modified_time=None,
):

    canonical_path = path

    if canonical_path is None and request is not None:

        canonical_path = request.path


    page_title = title or DEFAULT_TITLE

    if page_title != DEFAULT_TITLE and SITE_NAME not in page_title:

        page_title = f'{page_title} | {SITE_NAME}'


    return {
        'title': page_title,
        'description': plain_text(description or DEFAULT_DESCRIPTION),
        'canonical_url': absolute_url(canonical_path) if canonical_path else site_url(),
        'image': absolute_url(image) if image else default_image_url(),
        'type': type,
        'robots': robots,
        'keywords': keywords or '',
        'published_time': published_time,
        'modified_time': modified_time,
    }


def website_schema():

    return json.dumps({
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        'name': SITE_NAME,
        'url': site_url(),
        'potentialAction': {
            '@type': 'SearchAction',
            'target': f'{site_url()}{reverse("search")}?q={{search_term_string}}',
            'query-input': 'required name=search_term_string',
        },
    }, ensure_ascii=False)


def organization_schema():

    return json.dumps({
        '@context': 'https://schema.org',
        '@type': 'Organization',
        'name': SITE_NAME,
        'url': site_url(),
        'logo': default_image_url(),
    }, ensure_ascii=False)


def portfolio_schema(portfolio, language='fa'):

    is_english = language == 'en'
    portfolio_url = 'https://funmig.com/en/' if is_english else 'https://funmig.com/'
    logo_url = 'https://funmig.com/static/logo.png'
    services = ([
        'Custom website and responsive web design',
        'Web application and API development',
        'Social platform and marketplace development',
        'Admin dashboard and business tool development',
        'Artificial intelligence integration and automation',
        'UX/UI design, PWA and technical SEO',
        'Secure deployment, monitoring and technical support',
    ] if is_english else [
        'طراحی سایت اختصاصی و ریسپانسیو',
        'برنامه نویسی وب و توسعه وب اپلیکیشن',
        'طراحی و توسعه شبکه اجتماعی',
        'ساخت پنل مدیریت و داشبورد اختصاصی',
        'طراحی رابط و تجربه کاربری',
        'پیاده سازی PWA و اپلیکیشن تحت وب',
        'استقرار، امنیت و پشتیبانی فنی سایت',
    ])
    faq = ([
        ('What does FUNMIG build?', 'FUNMIG builds custom websites, web applications, social platforms, marketplaces, admin dashboards, PWAs and AI-enabled business tools.'),
        ('Does FUNMIG provide AI integration?', 'Yes. FUNMIG integrates AI models into real workflows including assistants, chatbots, content tools and automation.'),
        ('Are FUNMIG websites optimized for search and mobile?', 'Yes. Responsive design, accessibility, semantic HTML, structured data, sitemaps, performance and technical SEO are included from the beginning.'),
    ] if is_english else [
        ('فان میگ چه محصولاتی می سازد؟', 'فان میگ سایت اختصاصی، وب اپلیکیشن، شبکه اجتماعی، مارکت پلیس، پنل مدیریت، PWA و ابزارهای مجهز به هوش مصنوعی طراحی و توسعه می دهد.'),
        ('آیا فان میگ خدمات یکپارچه سازی هوش مصنوعی ارائه می دهد؟', 'بله. مدل های هوش مصنوعی برای دستیار، چت بات، تولید محتوا و اتوماسیون به فرایندهای واقعی متصل می شوند.'),
        ('آیا سایت ها برای موبایل و موتور جست وجو بهینه هستند؟', 'بله. طراحی ریسپانسیو، دسترس پذیری، HTML معنایی، داده ساختاریافته، سایت مپ، سرعت و سئوی فنی از ابتدا در نظر گرفته می شوند.'),
    ])

    graph = [
        {
            '@type': 'WebSite',
            '@id': f'{portfolio_url}#website',
            'url': portfolio_url,
            'name': 'FUNMIG',
            'alternateName': ['فان میگ', 'تیم برنامه نویسی فان میگ'],
            'inLanguage': 'en' if is_english else 'fa-IR',
            'publisher': {'@id': f'{portfolio_url}#organization'},
        },
        {
            '@type': ['Organization', 'ProfessionalService'],
            '@id': f'{portfolio_url}#organization',
            'name': 'FUNMIG Product and Web Development Team' if is_english else 'تیم طراحی و برنامه نویسی فان میگ',
            'alternateName': 'FUNMIG Web Development Team',
            'url': portfolio_url,
            'logo': {
                '@type': 'ImageObject',
                'url': logo_url,
            },
            'image': logo_url,
            'description': 'FUNMIG is a product-focused team delivering custom web development, social platforms, AI integrations, UX design and reliable infrastructure.' if is_english else plain_text(portfolio.intro, limit=300),
            'email': portfolio.email,
            'telephone': portfolio.phone,
            'address': {
                '@type': 'PostalAddress',
                'streetAddress': 'Emamat 18, No. 126' if is_english else portfolio.address,
                'addressLocality': 'Mashhad' if is_english else 'مشهد',
                'addressCountry': 'IR',
            },
            'areaServed': {'@type': 'Country', 'name': 'Iran' if is_english else 'ایران'},
            'knowsAbout': services,
            'sameAs': [
                'https://social.funmig.com/',
                portfolio.telegram_url,
            ],
            'contactPoint': {
                '@type': 'ContactPoint',
                'telephone': portfolio.phone,
                'email': portfolio.email,
                'contactType': 'sales and technical support',
                'availableLanguage': ['Persian', 'English'],
                'areaServed': 'IR',
            },
        },
        {
            '@type': 'Service',
            '@id': f'{portfolio_url}#web-development',
            'name': 'Custom Web Development and Product Design' if is_english else 'طراحی سایت و برنامه نویسی وب اختصاصی',
            'description': 'Custom websites, web applications, social platforms, AI integrations, admin dashboards, PWAs and secure infrastructure.' if is_english else 'طراحی و توسعه سایت، وب اپلیکیشن، شبکه اجتماعی، پنل مدیریت، PWA و زیرساخت امن و سریع برای کسب و کارها.',
            'provider': {'@id': f'{portfolio_url}#organization'},
            'areaServed': {'@type': 'Country', 'name': 'Iran' if is_english else 'ایران'},
            'serviceType': services,
            'url': portfolio_url,
        },
        {
            '@type': 'WebPage',
            '@id': f'{portfolio_url}#webpage',
            'url': portfolio_url,
            'name': 'FUNMIG | Custom Web Development, AI and Product Design' if is_english else 'طراحی سایت و برنامه نویسی وب | تیم توسعه FUNMIG',
            'description': 'FUNMIG designs and develops custom websites, social platforms, AI integrations, web applications and admin dashboards.' if is_english else 'طراحی سایت اختصاصی، برنامه نویسی وب، ساخت شبکه اجتماعی، وب اپلیکیشن و پنل مدیریت توسط تیم فان میگ.',
            'isPartOf': {'@id': f'{portfolio_url}#website'},
            'about': {'@id': f'{portfolio_url}#organization'},
            'mainEntity': {'@id': f'{portfolio_url}#web-development'},
            'inLanguage': 'en' if is_english else 'fa-IR',
            'dateModified': portfolio.updated_at.isoformat(),
        },
        {
            '@type': 'FAQPage',
            '@id': f'{portfolio_url}#faq',
            'inLanguage': 'en' if is_english else 'fa-IR',
            'mainEntity': [
                {'@type': 'Question', 'name': question, 'acceptedAnswer': {'@type': 'Answer', 'text': answer}}
                for question, answer in faq
            ],
        },
    ]

    return json.dumps({
        '@context': 'https://schema.org',
        '@graph': graph,
    }, ensure_ascii=False)


def article_schema(post):

    image = absolute_url(post.image.url) if getattr(post, 'image', None) else default_image_url()

    return json.dumps({
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': post.title,
        'description': plain_text(post.excerpt),
        'image': image,
        'datePublished': post.created_at.isoformat(),
        'dateModified': post.updated_at.isoformat(),
        'author': {
            '@type': 'Person',
            'name': post.author.get_full_name() or post.author.username,
        },
        'publisher': {
            '@type': 'Organization',
            'name': SITE_NAME,
            'logo': {
                '@type': 'ImageObject',
                'url': default_image_url(),
            },
        },
        'mainEntityOfPage': absolute_url(post.get_absolute_url()),
    }, ensure_ascii=False)


def sitemap_url(location, lastmod=None, changefreq='weekly', priority='0.7'):

    item = [
        '<url>',
        f'<loc>{escape(absolute_url(location))}</loc>',
    ]

    if lastmod:

        item.append(f'<lastmod>{lastmod.date().isoformat()}</lastmod>')

    item.extend([
        f'<changefreq>{changefreq}</changefreq>',
        f'<priority>{priority}</priority>',
        '</url>',
    ])

    return '\n'.join(item)

