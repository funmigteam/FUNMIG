

from django.db import migrations


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0006_alter_post_image_alter_userprofile_avatar'),


    ]


    operations = [


        migrations.RemoveField(


            model_name='userprofile',


            name='birth_date',


        ),


    ]


