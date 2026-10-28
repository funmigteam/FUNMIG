

import core.models


import django.db.models.deletion


from django.conf import settings


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0011_blogpost'),


        migrations.swappable_dependency(settings.AUTH_USER_MODEL),


    ]


    operations = [


        migrations.AddField(


            model_name='userprofile',


            name='has_trial',


            field=models.BooleanField(default=False, verbose_name='آیا تست رایگان استفاده شده؟'),


        ),


        migrations.AddField(


            model_name='userprofile',


            name='subscription_expiry',


            field=models.DateTimeField(blank=True, null=True, verbose_name='تاریخ انقضای اشتراک'),


        ),


        migrations.AlterField(


            model_name='post',


            name='content',


            field=models.TextField(blank=True, verbose_name='محتوا'),


        ),


        migrations.CreateModel(


            name='SubscriptionRequest',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('receipt_image', models.ImageField(upload_to=core.models.PathAndRename('receipts/'), verbose_name='تصویر رسید واریزی')),


                ('status', models.CharField(choices=[('pending', 'در انتظار تایید'), ('approved', 'تایید شده'), ('rejected', 'رد شده')], default='pending', max_length=10, verbose_name='وضعیت')),


                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درخواست')),


                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),


            ],


        ),


    ]


