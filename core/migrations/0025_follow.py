

import django.db.models.deletion


import django.utils.timezone


from django.conf import settings


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0024_chatsession_chatmessage'),


        migrations.swappable_dependency(settings.AUTH_USER_MODEL),


    ]


    operations = [


        migrations.CreateModel(


            name='Follow',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),


                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='دنبال\u200cکننده')),


                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL, verbose_name='دنبال\u200cشونده')),


            ],


            options={


                'verbose_name': 'فالو',


                'verbose_name_plural': 'فالوها',


                'ordering': ['-created_at'],


                'unique_together': {('follower', 'following')},


            },


        ),


    ]


