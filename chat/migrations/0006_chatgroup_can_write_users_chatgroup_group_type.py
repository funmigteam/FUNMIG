

from django.conf import settings


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('chat', '0005_chatmessage_is_video_message'),


        migrations.swappable_dependency(settings.AUTH_USER_MODEL),


    ]


    operations = [


        migrations.AddField(


            model_name='chatgroup',


            name='can_write_users',


            field=models.ManyToManyField(blank=True, related_name='writable_channels', to=settings.AUTH_USER_MODEL, verbose_name='کاربران قادر به نوشتن'),


        ),


        migrations.AddField(


            model_name='chatgroup',


            name='group_type',


            field=models.CharField(choices=[('group', 'گروه'), ('channel', 'چنل')], default='group', max_length=10, verbose_name='نوع گروه'),


        ),


    ]


