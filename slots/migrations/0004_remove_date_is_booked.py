"""Remove legacy date/is_booked columns and enforce weekly uniqueness."""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0003_deduplicate_weekly_slots'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='availableslot',
            name='unique_slot_per_date_time_type',
        ),
        migrations.RemoveField(
            model_name='availableslot',
            name='date',
        ),
        migrations.RemoveField(
            model_name='availableslot',
            name='is_booked',
        ),
        migrations.AlterField(
            model_name='availableslot',
            name='weekday',
            field=models.IntegerField(
                choices=[
                    (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
                    (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday'),
                ],
            ),
        ),
        migrations.AddConstraint(
            model_name='availableslot',
            constraint=models.UniqueConstraint(
                fields=('weekday', 'start_time', 'slot_type'),
                name='unique_slot_per_weekday_time_type',
            ),
        ),
        migrations.AlterModelOptions(
            name='availableslot',
            options={
                'ordering': ['weekday', 'start_time'],
                'verbose_name': 'Available slot',
                'verbose_name_plural': 'Available slots',
            },
        ),
    ]
