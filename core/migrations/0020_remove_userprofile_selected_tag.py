

from django.db import migrations


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0019_profiletag_userprofile_selected_tag'),


    ]


    operations = [


        migrations.RemoveField(


            model_name='userprofile',


            name='selected_tag',


        ),


    ]


