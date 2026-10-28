

import django.db.models.deletion


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0002_comment_parent_post_image'),


    ]


    operations = [


        migrations.AddField(


            model_name='post',


            name='parent',


            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='core.post', verbose_name='ریپلای به'),


        ),


    ]


