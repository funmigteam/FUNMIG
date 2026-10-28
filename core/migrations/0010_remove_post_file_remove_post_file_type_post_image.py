

import core.models


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0009_remove_post_image_post_file_post_file_type'),


    ]


    operations = [


        migrations.RemoveField(


            model_name='post',


            name='file',


        ),


        migrations.RemoveField(


            model_name='post',


            name='file_type',


        ),


        migrations.AddField(


            model_name='post',


            name='image',


            field=models.ImageField(blank=True, null=True, upload_to=core.models.PathAndRename('posts/'), verbose_name='تصویر پست'),


        ),


    ]


