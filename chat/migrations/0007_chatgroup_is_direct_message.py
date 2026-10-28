from django.db import migrations, models


def mark_existing_direct_messages(apps, schema_editor):

    ChatGroup = apps.get_model('chat', 'ChatGroup')


    for group in ChatGroup.objects.filter(is_private=True).prefetch_related('members'):

        usernames = list(group.members.values_list('username', flat=True))

        if len(usernames) != 2:

            continue


        expected_names = {
            f'Private {usernames[0]}-{usernames[1]}',
            f'Private {usernames[1]}-{usernames[0]}',
        }

        if group.name in expected_names:

            group.is_direct_message = True

            group.save(update_fields=['is_direct_message'])


class Migration(migrations.Migration):


    dependencies = [
        ('chat', '0006_chatgroup_can_write_users_chatgroup_group_type'),
    ]


    operations = [
        migrations.AddField(
            model_name='chatgroup',
            name='is_direct_message',
            field=models.BooleanField(default=False, verbose_name='چت مستقیم'),
        ),
        migrations.RunPython(mark_existing_direct_messages, migrations.RunPython.noop),
    ]

