from django.db import migrations, models


def create_default_ai_settings(apps, schema_editor):

    AISettings = apps.get_model('core', 'AISettings')

    AISettings.objects.get_or_create(pk=1, defaults={'is_free_for_all': False})


class Migration(migrations.Migration):


    dependencies = [
        ('core', '0040_post_submission_token'),
    ]


    operations = [
        migrations.CreateModel(
            name='AISettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_free_for_all', models.BooleanField(default=False, verbose_name='هوش مصنوعی برای همه رایگان باشد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین تغییر')),
            ],
            options={
                'verbose_name': 'تنظیمات هوش مصنوعی',
                'verbose_name_plural': 'تنظیمات هوش مصنوعی',
            },
        ),
        migrations.RunPython(create_default_ai_settings, migrations.RunPython.noop),
    ]

