

import django.db.models.deletion


from django.conf import settings


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0035_postmedia'),


        migrations.swappable_dependency(settings.AUTH_USER_MODEL),


    ]


    operations = [


        migrations.CreateModel(


            name='Hashtag',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('name', models.CharField(db_index=True, max_length=80, unique=True, verbose_name='نام هشتگ')),


                ('post_count', models.PositiveIntegerField(default=0, verbose_name='تعداد پست')),


                ('created_at', models.DateTimeField(auto_now_add=True)),


                ('updated_at', models.DateTimeField(auto_now=True)),


            ],


            options={


                'verbose_name': 'هشتگ',


                'verbose_name_plural': 'هشتگ\u200cها',


                'ordering': ['-post_count', 'name'],


            },


        ),


        migrations.CreateModel(


            name='PostHashtag',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('created_at', models.DateTimeField(auto_now_add=True)),


                ('hashtag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_links', to='core.hashtag')),


                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_hashtags', to='core.post')),


            ],


            options={


                'verbose_name': 'هشتگ پست',


                'verbose_name_plural': 'هشتگ\u200cهای پست',


                'indexes': [models.Index(fields=['post', 'hashtag'], name='core_postha_post_id_845ae5_idx'), models.Index(fields=['hashtag', 'created_at'], name='core_postha_hashtag_70d909_idx')],


                'unique_together': {('post', 'hashtag')},


            },


        ),


        migrations.CreateModel(


            name='SiteNotification',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('notification_type', models.CharField(choices=[('like', 'لایک'), ('comment', 'کامنت'), ('reply', 'پاسخ'), ('follow', 'فالو'), ('save', 'ذخیره'), ('mention', 'منشن'), ('payment', 'پرداخت'), ('system', 'سیستم')], default='system', max_length=20)),


                ('title', models.CharField(max_length=120)),


                ('message', models.TextField(blank=True)),


                ('url', models.CharField(blank=True, max_length=255)),


                ('is_read', models.BooleanField(default=False)),


                ('created_at', models.DateTimeField(auto_now_add=True)),


                ('actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_site_notifications', to=settings.AUTH_USER_MODEL)),


                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='core.comment')),


                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='core.post')),


                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='site_notifications', to=settings.AUTH_USER_MODEL)),


            ],


            options={


                'verbose_name': 'نوتیفیکیشن سایت',


                'verbose_name_plural': 'نوتیفیکیشن\u200cهای سایت',


                'ordering': ['-created_at'],


                'indexes': [models.Index(fields=['recipient', 'is_read', '-created_at'], name='core_siteno_recipie_f3feeb_idx'), models.Index(fields=['notification_type', '-created_at'], name='core_siteno_notific_25dc78_idx')],


            },


        ),


    ]


