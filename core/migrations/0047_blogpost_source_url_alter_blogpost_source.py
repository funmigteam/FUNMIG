

from django.db import migrations, models

from django.db.models import Q


def copy_url_sources(apps, schema_editor):

    BlogPost = apps.get_model('core', 'BlogPost')

    url_sources = BlogPost.objects.filter(source_url='').filter(
        Q(source__startswith='http://') | Q(source__startswith='https://')
    )

    for post in url_sources:

        post.source_url = post.source

        post.save(update_fields=['source_url'])


class Migration(migrations.Migration):


    dependencies = [
        ('core', '0046_blogpost_source_alter_blogpost_status'),
    ]


    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='source_url',
            field=models.URLField(blank=True, max_length=500, verbose_name='لینک منبع'),
        ),
        migrations.RunPython(copy_url_sources, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='blogpost',
            name='source',
            field=models.CharField(blank=True, max_length=255, verbose_name='نام منبع'),
        ),
    ]

