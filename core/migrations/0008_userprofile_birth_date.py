

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0007_remove_userprofile_birth_date'),


    ]


    operations = [


        migrations.AddField(


            model_name='userprofile',


            name='birth_date',


            field=models.DateField(blank=True, null=True, verbose_name='تاریخ تولد'),


        ),


    ]


