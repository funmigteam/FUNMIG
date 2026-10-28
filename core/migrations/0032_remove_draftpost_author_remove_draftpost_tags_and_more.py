

from django.db import migrations


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0031_postmedia'),


    ]


    operations = [


        migrations.RemoveField(


            model_name='draftpost',


            name='author',


        ),


        migrations.RemoveField(


            model_name='draftpost',


            name='tags',


        ),


        migrations.RemoveField(


            model_name='postmedia',


            name='post',


        ),


        migrations.AlterUniqueTogether(


            name='postmention',


            unique_together=None,


        ),


        migrations.RemoveField(


            model_name='postmention',


            name='mentioned_user',


        ),


        migrations.RemoveField(


            model_name='postmention',


            name='post',


        ),


        migrations.RemoveField(


            model_name='postview',


            name='post',


        ),


        migrations.RemoveField(


            model_name='postview',


            name='user',


        ),


        migrations.AlterUniqueTogether(


            name='reaction',


            unique_together=None,


        ),


        migrations.RemoveField(


            model_name='reaction',


            name='post',


        ),


        migrations.RemoveField(


            model_name='reaction',


            name='user',


        ),


        migrations.AlterUniqueTogether(


            name='share',


            unique_together=None,


        ),


        migrations.RemoveField(


            model_name='share',


            name='post',


        ),


        migrations.RemoveField(


            model_name='share',


            name='shared_by',


        ),


        migrations.AlterModelOptions(


            name='post',


            options={},


        ),


        migrations.RemoveIndex(


            model_name='post',


            name='core_post_created_84f629_idx',


        ),


        migrations.RemoveIndex(


            model_name='post',


            name='core_post_author__dc61ce_idx',


        ),


        migrations.DeleteModel(


            name='DraftPost',


        ),


        migrations.DeleteModel(


            name='PostTag',


        ),


        migrations.DeleteModel(


            name='PostMedia',


        ),


        migrations.DeleteModel(


            name='PostMention',


        ),


        migrations.DeleteModel(


            name='PostView',


        ),


        migrations.DeleteModel(


            name='Reaction',


        ),


        migrations.DeleteModel(


            name='Share',


        ),


    ]


