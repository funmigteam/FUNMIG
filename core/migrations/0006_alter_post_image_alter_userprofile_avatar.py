

import core.models


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0005_post_is_pinned'),


    ]


    operations = [


        migrations.AlterField(


            model_name='post',


            name='image',


            field=models.ImageField(blank=True, null=True, upload_to=core.models.PathAndRename('posts/'), verbose_name='تصویر پست'),


        ),


        migrations.AlterField(


            model_name='userprofile',


            name='avatar',


            field=models.ImageField(blank=True, null=True, upload_to=core.models.PathAndRename('avatars/'), verbose_name='تصویر پروفایل'),


        ),


    ]


