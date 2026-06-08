"""Add appointment_date and change slot to ForeignKey with active-booking uniqueness."""
from django.db import migrations, models
import django.db.models.deletion


def forwards_set_appointment_date(apps, schema_editor):
    """Copy the concrete date from the linked slot row."""
    Appointment = apps.get_model('appointments', 'Appointment')
    AvailableSlot = apps.get_model('slots', 'AvailableSlot')

    for appointment in Appointment.objects.all():
        slot = AvailableSlot.objects.filter(pk=appointment.slot_id).first()
        if slot and slot.date:
            appointment.appointment_date = slot.date
        else:
            from datetime import date
            appointment.appointment_date = date.today()
        appointment.save(update_fields=['appointment_date'])


def backwards_clear_appointment_date(apps, schema_editor):
    """Clear appointment_date on reverse."""
    Appointment = apps.get_model('appointments', 'Appointment')
    Appointment.objects.update(appointment_date=None)


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
        ('slots', '0002_weekly_slots'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='appointment_date',
            field=models.DateField(null=True),
        ),
        migrations.RunPython(forwards_set_appointment_date, backwards_clear_appointment_date),
        migrations.AlterField(
            model_name='appointment',
            name='slot',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='appointments',
                to='slots.availableslot',
            ),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_date',
            field=models.DateField(),
        ),
        migrations.AddConstraint(
            model_name='appointment',
            constraint=models.UniqueConstraint(
                condition=models.Q(('status__in', ['PENDING', 'CONFIRMED'])),
                fields=('slot', 'appointment_date'),
                name='unique_active_booking_per_slot_date',
            ),
        ),
        migrations.AlterModelOptions(
            name='appointment',
            options={
                'ordering': ['-appointment_date', '-slot__start_time'],
                'verbose_name': 'Appointment',
                'verbose_name_plural': 'Appointments',
            },
        ),
    ]
