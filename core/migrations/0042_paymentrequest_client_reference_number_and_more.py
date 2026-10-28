from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [
        ('core', '0041_aisettings'),
    ]


    operations = [
        migrations.AddField(
            model_name='paymentrequest',
            name='client_reference_number',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True, verbose_name='شماره پیگیری داخلی'),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='gateway',
            field=models.CharField(default='manual', max_length=20, verbose_name='درگاه پرداخت'),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='gateway_purchase_id',
            field=models.CharField(blank=True, db_index=True, max_length=128, null=True, verbose_name='شناسه خرید درگاه'),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='gateway_status',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='وضعیت درگاه'),
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='paid_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='زمان پرداخت'),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='receipt_image',
            field=models.ImageField(blank=True, null=True, upload_to='receipts/%Y/%m/%d/', verbose_name='فیش واریزی'),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'در انتظار بررسی'), ('gateway_pending', 'در انتظار پرداخت درگاه'), ('approved', 'تایید شده'), ('rejected', 'رد شده'), ('failed', 'ناموفق')], default='pending', max_length=20, verbose_name='وضعیت'),
        ),
    ]

