

import django.db.models.deletion


from django.conf import settings


from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [


        ('core', '0026_pushsubscription'),


        migrations.swappable_dependency(settings.AUTH_USER_MODEL),


    ]


    operations = [


        migrations.CreateModel(


            name='PaymentRequest',


            fields=[


                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),


                ('plan_type', models.CharField(max_length=20, verbose_name='نوع پلن')),


                ('amount', models.PositiveIntegerField(verbose_name='مبلغ (تومان)')),


                ('token_count', models.PositiveIntegerField(verbose_name='تعداد توکن')),


                ('validity_days', models.PositiveIntegerField(verbose_name='تعداد روز اعتبار')),


                ('receipt_image', models.ImageField(upload_to='receipts/%Y/%m/%d/', verbose_name='فیش واریزی')),


                ('status', models.CharField(choices=[('pending', 'در انتظار بررسی'), ('approved', 'تایید شده'), ('rejected', 'رد شده')], default='pending', max_length=20, verbose_name='وضعیت')),


                ('admin_note', models.TextField(blank=True, null=True, verbose_name='توضیحات ادمین')),


                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درخواست')),


                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),


                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),


            ],


            options={


                'verbose_name': 'درخواست پرداخت',


                'verbose_name_plural': 'درخواست\u200cهای پرداخت',


                'ordering': ['-created_at'],


            },


        ),


    ]


