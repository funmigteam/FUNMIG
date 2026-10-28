

import django.db.models.deletion


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0001_initial'),


    ]


    operations = [


        migrations.AddField(


            model_name='comment',


            name='parent',


            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='core.comment', verbose_name='پاسخ به'),


        ),


        migrations.AddField(


            model_name='post',


            name='image',


            field=models.ImageField(blank=True, null=True, upload_to='posts/', verbose_name='تصویر پست'),


        ),


    ]


