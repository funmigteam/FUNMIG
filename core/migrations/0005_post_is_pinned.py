

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0004_userprofile_birth_date'),


    ]


    operations = [


        migrations.AddField(


            model_name='post',


            name='is_pinned',


            field=models.BooleanField(default=False, verbose_name='پین شده'),


        ),


    ]


