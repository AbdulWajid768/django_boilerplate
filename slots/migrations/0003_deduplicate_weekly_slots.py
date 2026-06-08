"""Deduplicate weekly slot patterns after appointment_date is populated."""
from django.db import migrations


def forwards_deduplicate_slots(apps, schema_editor):
    """Merge duplicate weekly patterns and re-point appointments to the canonical row."""
    AvailableSlot = apps.get_model('slots', 'AvailableSlot')
    Appointment = apps.get_model('appointments', 'Appointment')

    canonical = {}
    for slot in AvailableSlot.objects.order_by('created_at'):
        key = (slot.weekday, slot.start_time, slot.end_time, slot.slot_type)
        if key not in canonical:
            canonical[key] = slot.id
            continue
        Appointment.objects.filter(slot_id=slot.id).update(slot_id=canonical[key])
        slot.delete()


def backwards_noop(apps, schema_editor):
    """No reverse for deduplication."""
    pass


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('slots', '0002_weekly_slots'),
        ('appointments', '0002_appointment_date_and_slot_fk'),
    ]

    operations = [
        migrations.RunPython(forwards_deduplicate_slots, backwards_noop),
    ]
