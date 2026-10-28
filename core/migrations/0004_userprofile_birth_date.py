

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0003_post_parent'),


    ]


    operations = [


        migrations.AddField(


            model_name='userprofile',


            name='birth_date',


            field=models.DateField(blank=True, null=True, verbose_name='تاریخ تولد'),


        ),


    ]


