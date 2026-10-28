from django.db import migrations, models


def update_phone(apps, schema_editor):
    TeamPortfolio = apps.get_model("core", "TeamPortfolio")
    TeamPortfolio.objects.using(schema_editor.connection.alias).filter(
        phone="+989981502665"
    ).update(phone="09993397299")


def restore_phone(apps, schema_editor):
    TeamPortfolio = apps.get_model("core", "TeamPortfolio")
    TeamPortfolio.objects.using(schema_editor.connection.alias).filter(
        phone="09993397299"
    ).update(phone="+989981502665")


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0052_remove_userprofile_has_trial_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teamportfolio",
            name="phone",
            field=models.CharField(
                default="09993397299", max_length=40, verbose_name="شماره تماس"
            ),
        ),
        migrations.RunPython(update_phone, restore_phone),
    ]
