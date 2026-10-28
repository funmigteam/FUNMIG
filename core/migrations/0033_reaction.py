

import django.db.models.deletion


from django.conf import settings


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0032_remove_draftpost_author_remove_draftpost_tags_and_more'),


        migrations.swappable_dependency(settings.AUTH_USER_MODEL),


    ]


    operations = [


        migrations.CreateModel(


            name='Reaction',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('emoji', models.CharField(choices=[('👍', 'like'), ('❤️', 'love'), ('😂', 'haha'), ('😢', 'sad'), ('😮', 'wow'), ('🔥', 'fire'), ('😍', 'heart_eyes'), ('💯', 'hundred')], max_length=4)),


                ('created_at', models.DateTimeField(auto_now_add=True)),


                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='core.post')),


                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),


            ],


            options={


                'unique_together': {('post', 'user')},


            },


        ),


    ]


