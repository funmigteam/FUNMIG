

import core.models

import django.db.models.deletion

from django.conf import settings

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [
        ('core', '0043_alter_paymentrequest_gateway'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]


    operations = [
        migrations.AddField(
            model_name='banner',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='ایجادکننده'),
        ),
        migrations.AddField(
            model_name='banner',
            name='ends_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='پایان نمایش'),
        ),
        migrations.AddField(
            model_name='banner',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=core.models.PathAndRename('ads/'), verbose_name='تصویر تبلیغ'),
        ),
        migrations.AddField(
            model_name='banner',
            name='placement',
            field=models.CharField(default='site_top', max_length=50, verbose_name='جایگاه نمایش'),
        ),
        migrations.AddField(
            model_name='banner',
            name='starts_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='شروع نمایش'),
        ),
        migrations.AddField(
            model_name='banner',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

