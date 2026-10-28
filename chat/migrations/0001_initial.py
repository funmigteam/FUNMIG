

import django.db.models.deletion


from django.conf import settings


from django.db import migrations, models


class Migration(migrations.Migration):


    initial = True


    dependencies = [


        migrations.swappable_dependency(settings.AUTH_USER_MODEL),


    ]


    operations = [


        migrations.CreateModel(


            name='ChatGroup',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('name', models.CharField(max_length=100, verbose_name='نام گروه')),


                ('created_at', models.DateTimeField(auto_now_add=True)),


                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_groups', to=settings.AUTH_USER_MODEL, verbose_name='سازنده')),


                ('members', models.ManyToManyField(related_name='chat_groups', to=settings.AUTH_USER_MODEL, verbose_name='اعضا')),


            ],


        ),


        migrations.CreateModel(


            name='ChatMessage',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('content', models.TextField(blank=True, null=True, verbose_name='متن پیام')),


                ('file', models.FileField(blank=True, null=True, upload_to='chat_files/', verbose_name='فایل پیوست')),


                ('file_type', models.CharField(blank=True, max_length=20, null=True, verbose_name='نوع فایل')),


                ('created_at', models.DateTimeField(auto_now_add=True)),


                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='فرستنده')),


                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chatgroup', verbose_name='گروه')),


            ],


        ),


        migrations.CreateModel(


            name='GroupInvite',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('token', models.CharField(max_length=64, unique=True, verbose_name='توکن دعوت')),


                ('created_at', models.DateTimeField(auto_now_add=True)),


                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_invites', to=settings.AUTH_USER_MODEL, verbose_name='فرستنده دعوت')),


                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invites', to='chat.chatgroup', verbose_name='گروه')),


            ],


        ),


    ]


