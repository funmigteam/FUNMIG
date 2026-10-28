

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0016_delete_userpersona'),


    ]


    operations = [


        migrations.AddField(


            model_name='userprofile',


            name='interests',


            field=models.TextField(blank=True, null=True, verbose_name='علاقه\u200cمندی\u200cها'),


        ),


        migrations.AddField(


            model_name='userprofile',


            name='personality_traits',


            field=models.TextField(blank=True, null=True, verbose_name='صفات شخصیتی'),


        ),


    ]


