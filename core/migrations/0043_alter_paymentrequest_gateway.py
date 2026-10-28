from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [
        ('core', '0042_paymentrequest_client_reference_number_and_more'),
    ]


    operations = [
        migrations.AlterField(
            model_name='paymentrequest',
            name='gateway',
            field=models.CharField(blank=True, default='manual', max_length=20, null=True, verbose_name='درگاه پرداخت'),
        ),
    ]

