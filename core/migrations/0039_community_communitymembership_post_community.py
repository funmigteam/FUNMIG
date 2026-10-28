import django.db.models.deletion

from django.conf import settings

from django.db import migrations, models


import core.models


class Migration(migrations.Migration):


    dependencies = [
        ('core', '0038_alter_share_unique_together_remove_share_post_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]


    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='نام انجمن')),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='نشانی انجمن')),
                ('description', models.TextField(max_length=500, verbose_name='معرفی انجمن')),
                ('rules', models.TextField(blank=True, verbose_name='قوانین انجمن')),
                ('cover', models.ImageField(blank=True, null=True, upload_to=core.models.PathAndRename('communities/'), verbose_name='تصویر انجمن')),
                ('color', models.CharField(default='#8b5cf6', max_length=7, verbose_name='رنگ انجمن')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_communities', to=settings.AUTH_USER_MODEL, verbose_name='سازنده')),
            ],
            options={
                'verbose_name': 'انجمن',
                'verbose_name_plural': 'انجمن‌ها',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CommunityMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('member', 'عضو'), ('moderator', 'مدیر')], default='member', max_length=12)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='core.community', verbose_name='انجمن')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community_memberships', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'عضویت انجمن',
                'verbose_name_plural': 'عضویت‌های انجمن',
                'ordering': ['-joined_at'],
                'unique_together': {('community', 'user')},
            },
        ),
        migrations.AddField(
            model_name='community',
            name='members',
            field=models.ManyToManyField(related_name='communities', through='core.CommunityMembership', to=settings.AUTH_USER_MODEL, verbose_name='اعضا'),
        ),
        migrations.AddField(
            model_name='post',
            name='community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='core.community', verbose_name='انجمن'),
        ),
    ]

