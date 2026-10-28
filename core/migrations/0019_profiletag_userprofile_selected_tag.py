

import django.db.models.deletion


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0018_userprofile_token_expiry_userprofile_tokens_balance'),


    ]


    operations = [


        migrations.CreateModel(


            name='ProfileTag',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('name', models.CharField(max_length=50, verbose_name='نام تگ')),


                ('color', models.CharField(default='#007bff', max_length=7, verbose_name='رنگ متن')),


                ('background_color', models.CharField(default='#e7f1ff', max_length=7, verbose_name='رنگ پس\u200cزمینه')),


                ('icon', models.CharField(blank=True, max_length=20, verbose_name='آیکون (emoji)')),


                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),


                ('order', models.PositiveIntegerField(default=0, verbose_name='ترتیب')),


            ],


            options={


                'verbose_name': 'تگ پروفایل',


                'verbose_name_plural': 'تگ\u200cهای پروفایل',


                'ordering': ['order', 'name'],


            },


        ),


        migrations.AddField(


            model_name='userprofile',


            name='selected_tag',


            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.profiletag', verbose_name='تگ انتخابی'),


        ),


    ]


