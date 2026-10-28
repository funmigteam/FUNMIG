

import core.models

import django.db.models.deletion

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [
        ('core', '0049_teamportfolio'),
    ]


    operations = [
        migrations.CreateModel(
            name='TeamPortfolioProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140, verbose_name='عنوان پروژه')),
                ('description', models.TextField(blank=True, verbose_name='توضیح پروژه')),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.models.PathAndRename('team_projects/'), verbose_name='عکس پروژه')),
                ('project_url', models.URLField(blank=True, max_length=500, verbose_name='لینک پروژه (اختیاری)')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_cards', to='core.teamportfolio', verbose_name='پروفایلو')),
            ],
            options={
                'verbose_name': 'پروژه پروفایلوی تیم',
                'verbose_name_plural': 'پروژه های پروفایلوی تیم',
                'ordering': ['order', '-created_at'],
            },
        ),
    ]

