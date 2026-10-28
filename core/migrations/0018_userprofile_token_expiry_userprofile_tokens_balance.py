

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0017_userprofile_interests_userprofile_personality_traits'),


    ]


    operations = [


        migrations.AddField(


            model_name='userprofile',


            name='token_expiry',


            field=models.DateTimeField(blank=True, null=True, verbose_name='تاریخ انقضای توکن\u200cها'),


        ),


        migrations.AddField(


            model_name='userprofile',


            name='tokens_balance',


            field=models.PositiveIntegerField(default=0, verbose_name='موجودی توکن'),


        ),


    ]


