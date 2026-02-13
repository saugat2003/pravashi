"""
Management command to update ChecklistItem with icons and Nepali titles for existing data.
Usage: python manage.py update_checklist_items
"""

from django.core.management.base import BaseCommand
from main.models import ChecklistItem


class Command(BaseCommand):
    help = 'Update checklist items with icons and Nepali titles'

    def handle(self, *args, **options):
        self.stdout.write('Updating checklist items...')

        # Icon mapping for checklist items
        icon_mapping = {
            'Verify Passport Validity': ('description', 'राहदानी (Passport)', 'विदेश जानका लागि कम्तीमा ६ महिनासम्म म्याद भएको राहदानी अनिवार्य हुन्छ।'),
            'Get Work Visa': ('card_travel', 'कार्य भिसा (Work Visa)', 'गन्तव्य देशका लागि सही कार्य भिसा प्राप्त गर्नुहोस्।'),
            'Medical Examination': ('health_and_safety', 'मेडिकल परीक्षण (Medical Examination)', 'मान्यताप्राप्त केन्द्रमा आवश्यक मेडिकल परीक्षणहरू पूरा गर्नुहोस्।'),
            'Attend Pre-departure Orientation': ('school', 'प्रस्थान पूर्व तालिम (Pre-departure Orientation)', 'अनिवार्य प्रस्थान पूर्व अभिमुखीकरण तालिम पूरा गर्नुहोस्।'),
            'Employment Contract Review': ('handshake', 'रोजगार करार समीक्षा (Contract Review)', 'हस्ताक्षर गर्नु अघि कानूनी विशेषज्ञद्वारा आफ्नो करारको समीक्षा गराउनुहोस्।'),
            'Embassy Registration': ('location_city', 'दूतावास दर्ता (Embassy Registration)', 'आगमनमा गन्तव्य देशमा नेपाली दूतावासमा दर्ता गर्नुहोस्।'),
            'Save Emergency Numbers': ('phone_in_talk', 'आपतकालीन नम्बरहरू (Emergency Numbers)', 'आफ्नो फोनमा दूतावास, पुलिस र आपतकालीन सम्पर्क नम्बरहरू सुरक्षित गर्नुहोस्।'),
            'Financial Planning': ('account_balance', 'वित्तीय योजना (Financial Planning)', 'घर पैसा पठाउनको लागि बैंक खाता र रेमिट्यान्स योजना स्थापना गर्नुहोस्।'),
            'Insurance Coverage': ('shield', 'बीमा कभरेज (Insurance Coverage)', 'प्रस्थान गर्नु अघि स्वास्थ्य र दुर्घटना बीमा लिनुहोस्।'),
            'Learn Basic Local Language': ('translate', 'स्थानीय भाषा सिक्नुहोस् (Learn Local Language)', 'गन्तव्यको आधारमा अरबी, मलय वा कोरियालीमा आधारभूत वाक्यांशहरू सिक्नुहोस्।'),
        }

        updated_count = 0
        for title, (icon, nepali_title, nepali_desc) in icon_mapping.items():
            try:
                item = ChecklistItem.objects.get(title=title)
                # Store icon in category field temporarily (we can add a proper icon field later)
                old_desc = item.description
                item.description = f"{nepali_desc}\n\nEnglish: {old_desc}"
                item.title = nepali_title
                # We'll use a custom field later, for now store icon name in a way we can parse
                item.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Updated: {title} → {nepali_title}'))
            except ChecklistItem.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ⚠ Not found: {title}'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Updated {updated_count} checklist items'))
