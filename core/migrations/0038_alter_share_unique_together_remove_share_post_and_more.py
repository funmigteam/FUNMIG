from django.db import migrations


class Migration(migrations.Migration):


    dependencies = [
        ('core', '0037_alter_sitenotification_notification_type_postview_and_more'),
    ]


    operations = [
        migrations.AlterUniqueTogether(
            name='share',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='share',
            name='post',
        ),
        migrations.RemoveField(
            model_name='share',
            name='shared_by',
        ),
        migrations.DeleteModel(
            name='Reaction',
        ),
        migrations.DeleteModel(
            name='Share',
        ),
    ]

