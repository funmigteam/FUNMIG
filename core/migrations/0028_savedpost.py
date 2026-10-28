from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0027_paymentrequest'),


    ]


    operations = [


        migrations.CreateModel(


            name='SavedPost',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('created_at', models.DateTimeField(auto_now_add=True)),


                ('post', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='saved_by', to='core.post')),


                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='saved_posts', to='auth.user')),


            ],


            options={


                'ordering': ['-created_at'],


                'verbose_name': 'پست ذخیره‌شده',


                'verbose_name_plural': 'پست‌های ذخیره‌شده',


                'unique_together': (('user', 'post'),),


            },


        ),


    ]


