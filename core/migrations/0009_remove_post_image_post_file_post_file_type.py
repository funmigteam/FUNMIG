

import core.models


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0008_userprofile_birth_date'),


    ]


    operations = [


        migrations.RemoveField(


            model_name='post',


            name='image',


        ),


        migrations.AddField(


            model_name='post',


            name='file',


            field=models.FileField(blank=True, null=True, upload_to=core.models.PathAndRename('posts/'), verbose_name='فایل پست'),


        ),


        migrations.AddField(


            model_name='post',


            name='file_type',


            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='نوع فایل'),


        ),


    ]


