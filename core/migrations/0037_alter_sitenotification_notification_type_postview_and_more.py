import django.db.models.deletion

from django.conf import settings

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [
        ('core', '0036_hashtag_posthashtag_sitenotification'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]


    operations = [
        migrations.AlterField(
            model_name='sitenotification',
            name='notification_type',
            field=models.CharField(choices=[('like', 'لایک'), ('comment', 'کامنت'), ('reply', 'پاسخ'), ('follow', 'فالو'), ('save', 'ذخیره'), ('share', 'اشتراک'), ('mention', 'منشن'), ('payment', 'پرداخت'), ('system', 'سیستم')], default='system', max_length=20),
        ),
        migrations.CreateModel(
            name='PostView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('viewed_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='core.post')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-viewed_at'],
                'indexes': [models.Index(fields=['post', '-viewed_at'], name='core_postvi_post_id_bd7682_idx'), models.Index(fields=['user', '-viewed_at'], name='core_postvi_user_id_ce35ee_idx'), models.Index(fields=['ip_address', '-viewed_at'], name='core_postvi_ip_addr_8e32d4_idx')],
            },
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emoji', models.CharField(choices=[('👍', 'پسندیدم'), ('❤️', 'دوست دارم'), ('😂', 'خنده\u200cدار'), ('😢', 'غم\u200cانگیز'), ('😮', 'شگفت\u200cانگیز'), ('🔥', 'داغ'), ('😍', 'عالی'), ('💯', 'بی\u200cنقص')], max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='core.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('post', 'user', 'emoji')},
            },
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('share_content', models.TextField(blank=True, null=True, verbose_name='متن اضافه هنگام اشتراک')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='core.post')),
                ('shared_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('post', 'shared_by')},
            },
        ),
    ]

