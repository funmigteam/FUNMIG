

import django.db.models.deletion


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0020_remove_userprofile_selected_tag'),


    ]


    operations = [


        migrations.AddField(


            model_name='userprofile',


            name='selected_tag',


            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.profiletag', verbose_name='تگ انتخابی'),


        ),


    ]


