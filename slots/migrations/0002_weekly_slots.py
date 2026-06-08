"""Add weekday and is_deleted; derive weekday from existing date field."""
from django.db import migrations, models


def forwards_set_weekday(apps, schema_editor):
    """Populate weekday from the legacy date column."""
    AvailableSlot = apps.get_model('slots', 'AvailableSlot')
    for slot in AvailableSlot.objects.all():
        if slot.date is not None:
            slot.weekday = slot.date.weekday()
            slot.save(update_fields=['weekday'])


def backwards_clear_weekday(apps, schema_editor):
    """Clear weekday on reverse."""
    AvailableSlot = apps.get_model('slots', 'AvailableSlot')
    AvailableSlot.objects.update(weekday=None)


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='availableslot',
            name='weekday',
            field=models.IntegerField(
                choices=[
                    (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
                    (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday'),
                ],
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='availableslot',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(forwards_set_weekday, backwards_clear_weekday),
    ]
