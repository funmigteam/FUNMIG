

import core.models

import django.db.models.deletion

from django.conf import settings

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [
        ('core', '0047_blogpost_source_url_alter_blogpost_source'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]


    operations = [
        migrations.CreateModel(
            name='BlogMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=core.models.PathAndRename('blog_media/'), verbose_name='فایل')),
                ('media_type', models.CharField(choices=[('image', 'تصویر'), ('audio', 'صوت')], max_length=10, verbose_name='نوع رسانه')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('uploader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='آپلودکننده')),
            ],
            options={
                'verbose_name': 'رسانه وبلاگ',
                'verbose_name_plural': 'رسانه\u200cهای وبلاگ',
                'ordering': ['-created_at'],
            },
        ),
    ]

