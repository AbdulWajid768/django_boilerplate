"""Management command to seed the default weekly AvailableSlot patterns."""
from django.core.management.base import BaseCommand

from slots.default_slots import DEFAULT_SLOTS
from slots.models import AvailableSlot


class Command(BaseCommand):
    """Create or restore the project's default weekly consultation slots."""

    help = 'Create the default weekly consultation slot patterns.'

    def add_arguments(self, parser):
        """Register optional flags for clearing existing slots."""
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing slots before seeding defaults.',
        )

    def handle(self, *args, **options):
        """Seed default slots, optionally clearing existing rows first."""
        if options['clear']:
            deleted_count, _ = AvailableSlot.all_objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Removed {deleted_count} existing slot(s).'))

        created_count = 0
        restored_count = 0

        for weekday, start_time, end_time, slot_type in DEFAULT_SLOTS:
            slot, created = AvailableSlot.all_objects.get_or_create(
                weekday=weekday,
                start_time=start_time,
                slot_type=slot_type,
                defaults={
                    'end_time': end_time,
                    'is_disabled': False,
                    'is_deleted': False,
                },
            )
            if created:
                created_count += 1
                continue

            updates = {}
            if slot.end_time != end_time:
                updates['end_time'] = end_time
            if slot.is_disabled:
                updates['is_disabled'] = False
            if slot.is_deleted:
                updates['is_deleted'] = False
                restored_count += 1
            if updates:
                for field, value in updates.items():
                    setattr(slot, field, value)
                slot.save(update_fields=[*updates.keys(), 'updated_at'])

        self.stdout.write(
            self.style.SUCCESS(
                f'Default slots ready: {created_count} created, {restored_count} restored.'
            )
        )
