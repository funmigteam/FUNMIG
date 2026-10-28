

import django.db.models.deletion


import django.utils.timezone


from django.conf import settings


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0023_banner'),


        migrations.swappable_dependency(settings.AUTH_USER_MODEL),


    ]


    operations = [


        migrations.CreateModel(


            name='ChatSession',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('title', models.CharField(default='چت جدید', max_length=100, verbose_name='عنوان چت')),


                ('model_key', models.CharField(max_length=50, verbose_name='مدل هوش مصنوعی')),


                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),


                ('updated_at', models.DateTimeField(auto_now=True)),


                ('is_archived', models.BooleanField(default=False, verbose_name='آرشیو شده')),


                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_sessions', to=settings.AUTH_USER_MODEL)),


            ],


            options={


                'verbose_name': 'سشن چت',


                'verbose_name_plural': 'سشن\u200cهای چت',


                'ordering': ['-updated_at'],


            },


        ),


        migrations.CreateModel(


            name='ChatMessage',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('role', models.CharField(choices=[('user', 'کاربر'), ('assistant', 'هوش مصنوعی')], max_length=20)),


                ('content', models.TextField()),


                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),


                ('tokens_used', models.IntegerField(default=0, verbose_name='توکن مصرفی')),


                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='core.chatsession')),


            ],


            options={


                'verbose_name': 'پیام چت',


                'verbose_name_plural': 'پیام\u200cهای چت',


                'ordering': ['created_at'],


            },


        ),


    ]


