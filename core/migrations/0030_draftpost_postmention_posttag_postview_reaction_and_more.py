

import core.models


import django.db.models.deletion


from django.conf import settings


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0029_blogpost_category_blogpost_description_blogpost_tags'),


        migrations.swappable_dependency(settings.AUTH_USER_MODEL),


    ]


    operations = [


        migrations.CreateModel(


            name='DraftPost',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('content', models.TextField(verbose_name='محتوا')),


                ('image', models.ImageField(blank=True, null=True, upload_to=core.models.PathAndRename('posts/'), verbose_name='تصویر')),


                ('created_at', models.DateTimeField(auto_now_add=True)),


                ('updated_at', models.DateTimeField(auto_now=True)),


            ],


            options={


                'verbose_name': 'پست پیش\u200cنویس',


                'verbose_name_plural': 'پست\u200cهای پیش\u200cنویس',


                'ordering': ['-updated_at'],


            },


        ),


        migrations.CreateModel(


            name='PostMention',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('created_at', models.DateTimeField(auto_now_add=True)),


            ],


            options={


                'verbose_name': 'اشاره به کاربر',


                'verbose_name_plural': 'اشارات',


            },


        ),


        migrations.CreateModel(


            name='PostTag',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('name', models.CharField(max_length=100, unique=True, verbose_name='نام تگ')),


                ('slug', models.SlugField(allow_unicode=True, unique=True)),


                ('created_at', models.DateTimeField(auto_now_add=True)),


                ('post_count', models.PositiveIntegerField(default=0, verbose_name='تعداد پست\u200cها')),


            ],


            options={


                'verbose_name': 'برچسب پست',


                'verbose_name_plural': 'برچسب\u200cهای پست',


                'ordering': ['-post_count'],


            },


        ),


        migrations.CreateModel(


            name='PostView',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('viewed_at', models.DateTimeField(auto_now_add=True)),


                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),


            ],


            options={


                'verbose_name': 'نمایش پست',


                'verbose_name_plural': 'نمایش\u200cهای پست',


                'ordering': ['-viewed_at'],


            },


        ),


        migrations.CreateModel(


            name='Reaction',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('emoji', models.CharField(choices=[('👍', '👍 خوب'), ('❤️', '❤️ دوست دارم'), ('😂', '😂 خنده دار'), ('😢', '😢 غم\u200cانگیز'), ('😮', '😮 شگفت\u200cانگیز'), ('🔥', '🔥 داغ'), ('😍', '😍 عاشق'), ('💯', '💯 عالی')], max_length=5)),


                ('created_at', models.DateTimeField(auto_now_add=True)),


            ],


            options={


                'verbose_name': 'واکنش',


                'verbose_name_plural': 'واکنش\u200cها',


            },


        ),


        migrations.CreateModel(


            name='Share',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('share_content', models.TextField(blank=True, null=True, verbose_name='متن اضافی هنگام اشتراک')),


                ('created_at', models.DateTimeField(auto_now_add=True)),


            ],


            options={


                'verbose_name': 'اشتراک پست',


                'verbose_name_plural': 'اشتراک\u200cهای پست',


                'ordering': ['-created_at'],


            },


        ),


        migrations.AlterModelOptions(


            name='post',


            options={'ordering': ['-created_at'], 'verbose_name': 'پست', 'verbose_name_plural': 'پست\u200cها'},


        ),


        migrations.AddIndex(


            model_name='post',


            index=models.Index(fields=['-created_at'], name='core_post_created_84f629_idx'),


        ),


        migrations.AddIndex(


            model_name='post',


            index=models.Index(fields=['author', '-created_at'], name='core_post_author__dc61ce_idx'),


        ),


        migrations.AddField(


            model_name='draftpost',


            name='author',


            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='draft_posts', to=settings.AUTH_USER_MODEL),


        ),


        migrations.AddField(


            model_name='postmention',


            name='mentioned_user',


            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentioned_in_posts', to=settings.AUTH_USER_MODEL, verbose_name='کاربر اشاره\u200cشده'),


        ),


        migrations.AddField(


            model_name='postmention',


            name='post',


            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentions', to='core.post'),


        ),


        migrations.AddField(


            model_name='draftpost',


            name='tags',


            field=models.ManyToManyField(blank=True, to='core.posttag', verbose_name='برچسب\u200cها'),


        ),


        migrations.AddField(


            model_name='postview',


            name='post',


            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='core.post'),


        ),


        migrations.AddField(


            model_name='postview',


            name='user',


            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),


        ),


        migrations.AddField(


            model_name='reaction',


            name='post',


            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='core.post'),


        ),


        migrations.AddField(


            model_name='reaction',


            name='user',


            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),


        ),


        migrations.AddField(


            model_name='share',


            name='post',


            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='core.post'),


        ),


        migrations.AddField(


            model_name='share',


            name='shared_by',


            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),


        ),


        migrations.AlterUniqueTogether(


            name='postmention',


            unique_together={('post', 'mentioned_user')},


        ),


        migrations.AlterUniqueTogether(


            name='reaction',


            unique_together={('post', 'user', 'emoji')},


        ),


        migrations.AlterUniqueTogether(


            name='share',


            unique_together={('post', 'shared_by')},


        ),


    ]


