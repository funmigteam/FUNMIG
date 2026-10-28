                                               

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_delete_aisettings_remove_chatsession_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='has_trial',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='subscription_expiry',
        ),
    ]
