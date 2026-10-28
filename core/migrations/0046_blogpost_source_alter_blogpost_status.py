

from django.db import migrations, models


def publish_existing_drafts(apps, schema_editor):

    BlogPost = apps.get_model('core', 'BlogPost')

    BlogPost.objects.filter(status='draft').update(status='published')


class Migration(migrations.Migration):


    dependencies = [
        ('core', '0045_announcement'),
    ]


    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='source',
            field=models.CharField(blank=True, max_length=255, verbose_name='منبع'),
        ),
        migrations.RunPython(publish_existing_drafts, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='blogpost',
            name='status',
            field=models.CharField(choices=[('published', 'منتشر شده')], default='published', max_length=10, verbose_name='وضعیت'),
        ),
    ]

