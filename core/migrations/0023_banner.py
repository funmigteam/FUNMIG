

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0022_profiletag_is_admin_only'),


    ]


    operations = [


        migrations.CreateModel(


            name='Banner',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('title', models.CharField(max_length=100, verbose_name='عنوان بنر')),


                ('description', models.TextField(verbose_name='متن بنر')),


                ('link', models.CharField(blank=True, max_length=255, null=True, verbose_name='لینک (اختیاری)')),


                ('background_color', models.CharField(default='#6366f1', max_length=7, verbose_name='رنگ پس\u200cزمینه')),


                ('text_color', models.CharField(default='#ffffff', max_length=7, verbose_name='رنگ متن')),


                ('is_active', models.BooleanField(default=True, verbose_name='فعال/غیرفعال')),


                ('is_dismissible', models.BooleanField(default=True, verbose_name='قابلیت بستن توسط کاربر')),


                ('created_at', models.DateTimeField(auto_now_add=True)),


            ],


            options={


                'verbose_name': 'بنر',


                'verbose_name_plural': 'بنرها',


                'ordering': ['-created_at'],


            },


        ),


    ]


