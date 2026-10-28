from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [
        ('core', '0039_community_communitymembership_post_community'),
    ]


    operations = [
        migrations.AddField(
            model_name='post',
            name='submission_token',
            field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        ),
    ]

