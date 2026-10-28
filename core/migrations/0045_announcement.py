

import django.db.models.deletion

from django.conf import settings

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [
        ('core', '0044_banner_created_by_banner_ends_at_banner_image_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]


    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='عنوان اعلامیه')),
                ('message', models.TextField(verbose_name='متن اعلامیه')),
                ('announcement_type', models.CharField(choices=[('info', 'اطلاعیه'), ('update', 'آپدیت'), ('warning', 'مهم')], default='info', max_length=20, verbose_name='نوع اعلامیه')),
                ('link', models.CharField(blank=True, max_length=255, null=True, verbose_name='لینک (اختیاری)')),
                ('link_label', models.CharField(default='جزئیات', max_length=40, verbose_name='متن دکمه')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال/غیرفعال')),
                ('is_dismissible', models.BooleanField(default=True, verbose_name='قابلیت بستن توسط کاربر')),
                ('starts_at', models.DateTimeField(blank=True, null=True, verbose_name='شروع نمایش')),
                ('ends_at', models.DateTimeField(blank=True, null=True, verbose_name='پایان نمایش')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='ایجادکننده')),
            ],
            options={
                'verbose_name': 'اعلامیه',
                'verbose_name_plural': 'اعلامیه\u200cها',
                'ordering': ['-created_at'],
            },
        ),
    ]

