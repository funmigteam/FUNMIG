

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('chat', '0002_chatmessage_parent'),


    ]


    operations = [


        migrations.AddField(


            model_name='chatgroup',


            name='is_private',


            field=models.BooleanField(default=False, verbose_name='چت خصوصی'),


        ),


    ]


