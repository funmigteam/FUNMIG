

import django.db.models.deletion


from django.conf import settings


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0013_userprofile_phone_number_delete_subscriptionrequest'),


        migrations.swappable_dependency(settings.AUTH_USER_MODEL),


    ]


    operations = [


        migrations.CreateModel(


            name='Ticket',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('subject', models.CharField(max_length=200, verbose_name='موضوع')),


                ('message', models.TextField(verbose_name='پیام')),


                ('status', models.CharField(choices=[('open', 'باز'), ('closed', 'بسته')], default='open', max_length=10, verbose_name='وضعیت')),


                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),


                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),


                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),


            ],


            options={


                'verbose_name': 'تیکت',


                'verbose_name_plural': 'تیکت\u200cها',


                'ordering': ['-created_at'],


            },


        ),


        migrations.CreateModel(


            name='TicketReply',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('message', models.TextField(verbose_name='پیام')),


                ('is_admin', models.BooleanField(default=False, verbose_name='پاسخ ادمین')),


                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')),


                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='core.ticket', verbose_name='تیکت')),


                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),


            ],


            options={


                'verbose_name': 'پاسخ تیکت',


                'verbose_name_plural': 'پاسخ\u200cهای تیکت',


                'ordering': ['created_at'],


            },


        ),


    ]


