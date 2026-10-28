from django import forms


from html import escape

from html.parser import HTMLParser

import re


from .models import Post, Comment, UserProfile, BlogPost, ProfileTag, Community


class BlogContentSanitizer(HTMLParser):


    allowed_tags = {
        'p', 'br', 'strong', 'b', 'em', 'i', 'u', 'ul', 'ol', 'li',
        'h2', 'h3', 'h4', 'blockquote', 'a', 'img', 'audio', 'source',
        'span', 'figure', 'figcaption', 'hr'
    }

    void_tags = {'br', 'img', 'source', 'hr'}

    allowed_attrs = {
        'a': {'href', 'target', 'rel'},
        'img': {'src', 'alt', 'title'},
        'audio': {'src', 'controls'},
        'source': {'src', 'type'},
        'span': {'style'},
        'blockquote': {'class'},
        'figure': {'class'},
    }

    allowed_classes = {'blog-callout', 'blog-media', 'blog-audio'}


    def __init__(self):

        super().__init__(convert_charrefs=True)

        self.parts = []

        self.open_tags = []

        self.skip_depth = 0


    def handle_starttag(self, tag, attrs):

        if tag in {'script', 'style'}:

            self.skip_depth += 1

            return

        if self.skip_depth:

            return

        if tag not in self.allowed_tags:

            return

        clean_attrs = self.clean_attrs(tag, attrs)

        attr_text = ''.join(f' {name}="{escape(value, quote=True)}"' for name, value in clean_attrs)

        self.parts.append(f'<{tag}{attr_text}>')

        if tag not in self.void_tags:

            self.open_tags.append(tag)


    def handle_endtag(self, tag):

        if tag in {'script', 'style'} and self.skip_depth:

            self.skip_depth -= 1

            return

        if self.skip_depth:

            return

        if tag not in self.allowed_tags or tag in self.void_tags:

            return

        if tag in self.open_tags:

            while self.open_tags:

                open_tag = self.open_tags.pop()

                self.parts.append(f'</{open_tag}>')

                if open_tag == tag:

                    break


    def handle_data(self, data):

        if self.skip_depth:

            return

        self.parts.append(escape(data))


    def handle_entityref(self, name):

        if self.skip_depth:

            return

        self.parts.append(f'&{name};')


    def handle_charref(self, name):

        if self.skip_depth:

            return

        self.parts.append(f'&#{name};')


    def clean_attrs(self, tag, attrs):

        clean = []

        allowed = self.allowed_attrs.get(tag, set())

        for name, value in attrs:

            if name not in allowed:

                continue

            value = value or ''

            if name in {'href', 'src'} and not self.is_safe_url(value):

                continue

            if name == 'style':

                value = self.clean_style(value)

                if not value:

                    continue

            if name == 'class':

                classes = [item for item in value.split() if item in self.allowed_classes]

                if not classes:

                    continue

                value = ' '.join(classes)

            if tag == 'audio' and name == 'controls':

                value = 'controls'

            clean.append((name, value))

        if tag == 'a':

            clean = [(name, value) for name, value in clean if name not in {'target', 'rel'}]

            clean.extend([('target', '_blank'), ('rel', 'noopener noreferrer')])

        if tag == 'audio' and not any(name == 'controls' for name, _ in clean):

            clean.append(('controls', 'controls'))

        return clean


    def clean_style(self, value):

        safe_rules = []

        for rule in value.split(';'):

            if ':' not in rule:

                continue

            prop, raw = [part.strip().lower() for part in rule.split(':', 1)]

            if prop not in {'color', 'background-color'}:

                continue

            if re.fullmatch(r'#[0-9a-f]{3}([0-9a-f]{3})?', raw) or re.fullmatch(r'rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)', raw):

                safe_rules.append(f'{prop}: {raw}')

        return '; '.join(safe_rules)


    def is_safe_url(self, value):

        return value.startswith(('/', 'http://', 'https://')) and not value.lower().startswith(('javascript:', 'data:'))


    def get_html(self):

        while self.open_tags:

            self.parts.append(f'</{self.open_tags.pop()}>')

        return ''.join(self.parts)


def sanitize_blog_content(content):

    content = content or ''

    content = re.sub(
        r"''\s*([^']{1,500}?)\s*''",
        r'<blockquote class="blog-callout">\1</blockquote>',
        content,
        flags=re.DOTALL,
    )

    sanitizer = BlogContentSanitizer()

    sanitizer.feed(content)

    return sanitizer.get_html().strip()


class MultiFileInput(forms.ClearableFileInput):


    allow_multiple_selected = True


class PostForm(forms.ModelForm):


    media = forms.FileField(


        required=False,


        widget=MultiFileInput(attrs={'multiple': True, 'accept': 'image/*,video/*,audio/*'})


    )


    class Meta:


        model = Post


        fields = ['content', 'community']


        widgets = {


            'content': forms.Textarea(attrs={


                'class': 'form-control',


                'rows': 3,


                'placeholder': 'چه خبر؟',


                'style': 'direction: rtl; text-align: right;'


            }),
            'community': forms.Select(attrs={
                'class': 'form-control',
                'style': 'direction: rtl; text-align: right;'
            }),


        }


    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        self.fields['community'].required = False

        self.fields['community'].empty_label = 'بدون انجمن (فید عمومی)'

        if user and user.is_authenticated:

            self.fields['community'].queryset = Community.objects.filter(
                is_active=True,
                memberships__user=user
            ).distinct()

        else:

            self.fields['community'].queryset = Community.objects.none()


    def clean_content(self):


        content = self.cleaned_data.get('content')


        return content.strip()


    def clean_image(self):


        return None


    def clean_media(self):


        files = self.files.getlist('media') if hasattr(self, 'files') else []


        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.webm', '.mp3', '.wav', '.ogg']


        for f in files:


            ext = '.' + f.name.lower().split('.')[-1]


            if ext not in valid_extensions:


                raise forms.ValidationError("فرمت فایل نامعتبر است. فقط عکس، ویدیو و موزیک مجاز هستند.")


        return files


class CommentForm(forms.ModelForm):


    class Meta:


        model = Comment


        fields = ['text']


        widgets = {


            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نظر خود را بنویسید...'}),


        }


class CommunityForm(forms.ModelForm):


    class Meta:

        model = Community

        fields = ['name', 'slug', 'description', 'rules', 'cover', 'color']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً تکنولوژی'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'technology'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'موضوع و هدف انجمن را معرفی کنید'}),
            'rules': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'قوانین اختصاصی انجمن (اختیاری)'}),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):


    birth_date = forms.DateField(


        required=False,


        widget=forms.DateInput(attrs={'type': 'date'}),


        input_formats=['%Y-%m-%d']


    )


    selected_tag = forms.ModelChoiceField(


        queryset=ProfileTag.objects.none(),


        required=False,


        empty_label="بدون تگ",


        widget=forms.Select(attrs={'class': 'form-control'})


    )


    class Meta:


        model = UserProfile


        fields = ['bio', 'avatar', 'background_color', 'text_color', 'birth_date', 'phone_number', 'selected_tag']


        widgets = {


            'bio': forms.Textarea(attrs={'rows': 3}),


            'background_color': forms.TextInput(attrs={'type': 'color'}),


            'text_color': forms.TextInput(attrs={'type': 'color'}),


        }


    def __init__(self, *args, **kwargs):


        user = kwargs.pop('user', None)


        super().__init__(*args, **kwargs)


        if user:


            if user.is_staff:


                self.fields['selected_tag'].queryset = ProfileTag.objects.filter(is_active=True)


            else:


                self.fields['selected_tag'].queryset = ProfileTag.objects.filter(


                    is_active=True,


                    is_admin_only=False


                )


    def clean_avatar(self):


        avatar = self.cleaned_data.get('avatar')


        if not avatar:


            return avatar


        if hasattr(avatar, 'content_type'):


            if not avatar.content_type in ['image/png', 'image/jpeg', 'image/jpg', 'image/gif']:


                raise forms.ValidationError("فقط فرمت‌های PNG، JPG و JPEG مجاز هستند.")


        return avatar


class BlogPostForm(forms.ModelForm):


    content = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control blog-rich-textarea',
        'rows': 12,
        'placeholder': 'متن اصلی مقاله...',
    }))


    class Meta:


        model = BlogPost


        fields = ['title', 'slug', 'description', 'tags', 'source', 'source_url', 'content', 'image']


        widgets = {


            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان مقاله'}),


            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسلاگ (انگلیسی)'}),


            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'خلاصه‌ای کوتاه برای صفحه اصلی...'}),


            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'برچسب‌ها با کاما جدا شوند'}),


            'source': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام منبع، مثلاً BBC یا سایت رسمی'}),


            'source_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'لینک منبع، اختیاری'}),


        }


    def clean_content(self):


        content = self.cleaned_data.get('content')


        clean_content = sanitize_blog_content(content)


        if not re.sub(r'<[^>]+>', '', clean_content).strip() and '<img' not in clean_content and '<audio' not in clean_content:


            raise forms.ValidationError('محتوای مقاله نمی‌تواند خالی باشد.')


        return clean_content

