

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('chat', '0004_notification'),


    ]


    operations = [


        migrations.AddField(


            model_name='chatmessage',


            name='is_video_message',


            field=models.BooleanField(default=False, verbose_name='آیا ویدیو مسیج است؟'),


        ),


    ]


