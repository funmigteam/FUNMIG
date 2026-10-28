

import django.db.models.deletion


from django.conf import settings


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('chat', '0003_chatgroup_is_private'),


        migrations.swappable_dependency(settings.AUTH_USER_MODEL),


    ]


    operations = [


        migrations.CreateModel(


            name='Notification',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('is_read', models.BooleanField(default=False, verbose_name='خوانده شده')),


                ('created_at', models.DateTimeField(auto_now_add=True)),


                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chatgroup', verbose_name='گروه مربوطه')),


                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chatmessage', verbose_name='پیام مربوطه')),


                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL, verbose_name='گیرنده')),


            ],


        ),


    ]


