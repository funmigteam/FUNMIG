

import core.models


import django.db.models.deletion


from django.conf import settings


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0010_remove_post_file_remove_post_file_type_post_image'),


        migrations.swappable_dependency(settings.AUTH_USER_MODEL),


    ]


    operations = [


        migrations.CreateModel(


            name='BlogPost',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('title', models.CharField(max_length=200, verbose_name='عنوان مقاله')),


                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='اسلاگ')),


                ('content', models.TextField(verbose_name='محتوای مقاله')),


                ('image', models.ImageField(blank=True, null=True, upload_to=core.models.PathAndRename('blog_images/'), verbose_name='تصویر مقاله')),


                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),


                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),


                ('status', models.CharField(choices=[('draft', 'پیش\u200cنویس'), ('published', 'منتشر شده')], default='draft', max_length=10, verbose_name='وضعیت')),


                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),


            ],


            options={


                'verbose_name': 'مقاله وبلاگ',


                'verbose_name_plural': 'مقالات وبلاگ',


                'ordering': ['-created_at'],


            },


        ),


    ]


