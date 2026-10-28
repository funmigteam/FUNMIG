

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0021_userprofile_selected_tag'),


    ]


    operations = [


        migrations.AddField(


            model_name='profiletag',


            name='is_admin_only',


            field=models.BooleanField(default=False, verbose_name='فقط برای ادمین'),


        ),


    ]


