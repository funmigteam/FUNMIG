

import core.models


import django.db.models.deletion


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0030_draftpost_postmention_posttag_postview_reaction_and_more'),


    ]


    operations = [


        migrations.CreateModel(


            name='PostMedia',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('file', models.FileField(upload_to=core.models.PathAndRename('posts/'), verbose_name='فایل')),


                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video'), ('audio', 'Audio'), ('file', 'File')], default='image', max_length=10)),


                ('order', models.PositiveIntegerField(default=0)),


                ('created_at', models.DateTimeField(auto_now_add=True)),


                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='core.post')),


            ],


            options={


                'verbose_name': 'رسانه پست',


                'verbose_name_plural': 'رسانه\u200cهای پست',


                'ordering': ['order', '-created_at'],


            },


        ),


    ]


