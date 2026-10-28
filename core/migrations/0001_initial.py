

import django.db.models.deletion


import django.utils.timezone


from django.conf import settings


from django.db import migrations, models


class Migration(migrations.Migration):


    initial = True


    dependencies = [


        migrations.swappable_dependency(settings.AUTH_USER_MODEL),


    ]


    operations = [


        migrations.CreateModel(


            name='Post',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('content', models.TextField(verbose_name='محتوا')),


                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),


                ('updated_at', models.DateTimeField(auto_now=True)),


                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),


            ],


        ),


        migrations.CreateModel(


            name='Comment',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('text', models.TextField(verbose_name='متن کامنت')),


                ('created_at', models.DateTimeField(auto_now_add=True)),


                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),


                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.post')),


            ],


        ),


        migrations.CreateModel(


            name='UserProfile',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('bio', models.TextField(blank=True, null=True, verbose_name='بیوگرافی')),


                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='تصویر پروفایل')),


                ('background_color', models.CharField(default='#ffffff', max_length=7, verbose_name='رنگ پس\u200cزمینه')),


                ('text_color', models.CharField(default='#000000', max_length=7, verbose_name='رنگ متن')),


                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),


            ],


        ),


        migrations.CreateModel(


            name='Like',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('created_at', models.DateTimeField(auto_now_add=True)),


                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),


                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.post')),


            ],


            options={


                'unique_together': {('post', 'user')},


            },


        ),


    ]


