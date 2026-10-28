

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0012_userprofile_has_trial_and_more'),


    ]


    operations = [


        migrations.AddField(


            model_name='userprofile',


            name='phone_number',


            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='شماره موبایل'),


        ),


        migrations.DeleteModel(


            name='SubscriptionRequest',


        ),


    ]


