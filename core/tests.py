from io import BytesIO
import os
import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase, override_settings
from PIL import Image

from django.urls import reverse
import json
import re

from .models import Community, CommunityMembership, Post, UserProfile


class PortfolioLocalizationTests(TestCase):
    def test_persian_and_english_pages_have_independent_seo(self):
        fa = self.client.get('/', secure=True, HTTP_HOST='funmig.com')
        en = self.client.get('/en/', secure=True, HTTP_HOST='funmig.com')

        self.assertEqual(fa.status_code, 200)
        self.assertEqual(en.status_code, 200)
        self.assertContains(fa, '<html lang="fa" dir="rtl">')
        self.assertContains(en, '<html lang="en" dir="ltr">')
        self.assertContains(en, 'FUNMIG | Custom Web Development, AI and Product Design')
        self.assertContains(en, 'hreflang="fa-IR"')
        self.assertContains(en, 'hreflang="en"')

        match = re.search(r'<script type="application/ld\+json">(.*?)</script>', en.content.decode(), re.S)
        document = json.loads(match.group(1))
        self.assertIn('FAQPage', [node.get('@type') for node in document['@graph']])

    def test_saved_english_language_redirects_root(self):
        self.client.cookies['funmig_portfolio_language'] = 'en'
        response = self.client.get('/', secure=True, HTTP_HOST='funmig.com')
        self.assertRedirects(response, '/en/', fetch_redirect_response=False)

    def test_ai_discovery_files_are_public(self):
        robots = self.client.get('/robots.txt', secure=True, HTTP_HOST='funmig.com')
        llms = self.client.get('/llms.txt', secure=True, HTTP_HOST='funmig.com')
        self.assertContains(robots, 'OAI-SearchBot')
        self.assertContains(robots, 'Google-Extended')
        self.assertContains(llms, 'English version: https://funmig.com/en/')


class CommunityTests(TestCase):


    def setUp(self):

        self.owner = User.objects.create_user(username='owner', password='pass12345')

        self.member = User.objects.create_user(username='member', password='pass12345')

        UserProfile.objects.create(user=self.owner)

        UserProfile.objects.create(user=self.member)

        self.community = Community.objects.create(
            name='تکنولوژی',
            slug='technology',
            description='گفتگو درباره فناوری',
            owner=self.owner
        )

        CommunityMembership.objects.create(
            community=self.community,
            user=self.owner,
            role=CommunityMembership.ROLE_MODERATOR
        )


    def test_creator_becomes_moderator(self):

        self.client.force_login(self.member)

        response = self.client.post(reverse('community_create'), {
            'name': 'بازی',
            'slug': 'gaming',
            'description': 'انجمن بازی',
            'rules': '',
            'color': '#8b5cf6',
        })


        community = Community.objects.get(slug='gaming')

        membership = CommunityMembership.objects.get(
            community=community,
            user=self.member
        )

        self.assertRedirects(response, reverse('community_detail', args=['gaming']))

        self.assertEqual(community.owner, self.member)

        self.assertEqual(membership.role, CommunityMembership.ROLE_MODERATOR)


    def test_user_can_join_and_publish_in_community(self):

        self.client.force_login(self.member)

        self.client.post(reverse('community_join', args=[self.community.slug]))


        response = self.client.post(
            reverse('community_detail', args=[self.community.slug]),
            {'content': 'اولین پست انجمن'}
        )


        post = Post.objects.get(content='اولین پست انجمن')

        self.assertRedirects(
            response,
            reverse('community_detail', args=[self.community.slug])
        )

        self.assertEqual(post.community, self.community)

        self.assertEqual(post.author, self.member)


    def test_non_member_cannot_publish_in_community(self):

        self.client.force_login(self.member)


        response = self.client.post(
            reverse('community_detail', args=[self.community.slug]),
            {'content': 'پست غیرمجاز'}
        )


        self.assertRedirects(
            response,
            reverse('community_detail', args=[self.community.slug])
        )

        self.assertFalse(Post.objects.filter(content='پست غیرمجاز').exists())


    def test_owner_cannot_leave_community(self):

        self.client.force_login(self.owner)


        self.client.post(reverse('community_leave', args=[self.community.slug]))


        self.assertTrue(
            CommunityMembership.objects.filter(
                community=self.community,
                user=self.owner
            ).exists()
        )


class PostReplyTests(TestCase):


    def setUp(self):

        self.author = User.objects.create_user(username='author', password='pass12345')

        self.replier = User.objects.create_user(username='replier', password='pass12345')

        UserProfile.objects.create(user=self.author)

        UserProfile.objects.create(user=self.replier)

        self.post = Post.objects.create(author=self.author, content='Original post')


    def test_ajax_reply_can_target_another_reply(self):

        first_reply = Post.objects.create(
            author=self.replier,
            content='First reply',
            parent=self.post
        )

        self.client.force_login(self.author)


        response = self.client.post(
            reverse('create_post_ajax'),
            {'content': 'Nested reply', 'parent_id': first_reply.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )


        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.json()['success'])

        nested_reply = Post.objects.get(content='Nested reply')

        self.assertEqual(nested_reply.parent, first_reply)

        self.assertContains(response, 'First reply')


class PostSubmissionTokenTests(TestCase):


    def setUp(self):

        self.user = User.objects.create_user(username='poster', password='pass12345')

        UserProfile.objects.create(user=self.user)


    def test_duplicate_submission_token_returns_existing_post(self):

        self.client.force_login(self.user)

        token = '11111111-1111-4111-8111-111111111111'


        first = self.client.post(
            reverse('create_post_ajax'),
            {'content': 'Slow network post', 'submission_token': token},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        second = self.client.post(
            reverse('create_post_ajax'),
            {'content': 'Slow network post', 'submission_token': token},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )


        self.assertEqual(first.status_code, 200)

        self.assertEqual(second.status_code, 200)

        self.assertTrue(second.json()['duplicate'])

        self.assertEqual(first.json()['post_id'], second.json()['post_id'])

        self.assertEqual(Post.objects.filter(content='Slow network post').count(), 1)


class ImageOptimizationTests(TestCase):
    def setUp(self):
        self.media = tempfile.mkdtemp()
        self.override = override_settings(MEDIA_ROOT=self.media)
        self.override.enable()
        self.user = User.objects.create_user('photo', 'photo@example.com', 'pass12345X')

    def tearDown(self):
        self.override.disable()
        shutil.rmtree(self.media, ignore_errors=True)

    def _upload(self, name, mode, size, fmt):
        buffer = BytesIO()
        Image.frombytes(mode, size, os.urandom(size[0] * size[1] * len(mode))).save(buffer, fmt)
        return SimpleUploadedFile(name, buffer.getvalue())

    def test_large_photo_post_is_resized_on_upload(self):
        post = Post.objects.create(author=self.user, content='x', image=self._upload('big.jpg', 'RGB', (3000, 2000), 'JPEG'))
        post.refresh_from_db()
        with Image.open(post.image.path) as image:
            self.assertEqual(max(image.size), 1600)

    def test_opaque_png_becomes_jpeg_and_field_is_updated(self):
        post = Post.objects.create(author=self.user, content='x', image=self._upload('shot.png', 'RGB', (2400, 1400), 'PNG'))
        post.refresh_from_db()
        self.assertTrue(post.image.name.endswith('.jpg'))
        with Image.open(post.image.path) as image:
            self.assertEqual(image.format, 'JPEG')

    def test_transparent_png_stays_png(self):
        post = Post.objects.create(author=self.user, content='x', image=self._upload('logo.png', 'RGBA', (2000, 2000), 'PNG'))
        post.refresh_from_db()
        self.assertTrue(post.image.name.endswith('.png'))

    def test_small_image_is_left_untouched(self):
        upload = self._upload('tiny.jpg', 'RGB', (40, 40), 'JPEG')
        size = upload.size
        post = Post.objects.create(author=self.user, content='x', image=upload)
        self.assertEqual(os.path.getsize(post.image.path), size)
