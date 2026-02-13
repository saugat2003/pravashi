"""
Management command to seed the database with realistic data for Pravash.
Usage: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from main.models import (
    User, EmergencyContact, Document, ContractAnalysis, FlaggedClause,
    SafetyCheckIn, SOSEvent, Embassy, Community, ChecklistItem,
    UserChecklistProgress, Notification, ActivityLog,
)


class Command(BaseCommand):
    help = 'Seed the database with sample data for Pravash demo'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # ── Users ──────────────────────────────────────
        worker, _ = User.objects.get_or_create(
            username='ram',
            defaults={
                'first_name': 'Ram',
                'last_name': 'Thapa',
                'email': 'ram@example.com',
                'phone': '+977-9841234567',
                'profile_type': 'worker',
                'current_country': 'Malaysia',
                'current_city': 'Kuala Lumpur',
                'language_preference': 'ne',
                'location_sharing': True,
                'checkin_reminders': True,
            },
        )
        worker.set_password('worker123')
        worker.save()

        family, _ = User.objects.get_or_create(
            username='sita',
            defaults={
                'first_name': 'Sita',
                'last_name': 'Thapa',
                'email': 'sita@example.com',
                'phone': '+977-9849876543',
                'profile_type': 'family',
                'language_preference': 'ne',
                'monitored_worker': worker,
            },
        )
        family.set_password('family123')
        family.save()

        self.stdout.write(self.style.SUCCESS(
            '  ✓ Users: ram/worker123 (worker), sita/family123 (family)'
        ))

        # ── Emergency Contacts ─────────────────────────
        contacts_data = [
            {'name': 'Sita Thapa', 'relationship': 'Wife', 'phone': '+977-9849876543'},
            {'name': 'Krishna Thapa', 'relationship': 'Brother', 'phone': '+977-9812345678'},
            {'name': 'Nepal Embassy Malaysia', 'relationship': 'Embassy', 'phone': '+60-3-20203573'},
        ]
        for c in contacts_data:
            EmergencyContact.objects.get_or_create(user=worker, phone=c['phone'], defaults=c)
        self.stdout.write(self.style.SUCCESS('  ✓ Emergency contacts'))

        # ── Documents ──────────────────────────────────
        docs_data = [
            {'doc_type': 'passport', 'file': 'documents/passport.pdf', 'verification_status': 'verified'},
            {'doc_type': 'work_visa', 'file': 'documents/work_visa.pdf', 'verification_status': 'verified'},
            {'doc_type': 'employment_contract', 'file': 'documents/employment_contract.pdf', 'verification_status': 'pending'},
            {'doc_type': 'insurance', 'file': 'documents/insurance.pdf', 'verification_status': 'pending'},
        ]
        for d in docs_data:
            doc_type = d.pop('doc_type')
            Document.objects.get_or_create(user=worker, doc_type=doc_type, defaults=d)
        self.stdout.write(self.style.SUCCESS('  ✓ Documents'))

        # ── Contract Analysis ──────────────────────────
        analysis, _ = ContractAnalysis.objects.get_or_create(
            user=worker,
            employer_name='Sunway Construction Sdn Bhd',
            defaults={
                'file': 'contracts/sunway_contract.pdf',
                'risk_score': 72,
                'risk_level': 'high',
                'ai_recommendation': (
                    'This contract contains several concerning clauses regarding '
                    'overtime pay, passport confiscation, and contract termination. '
                    'We strongly recommend consulting with a legal advisor before signing.'
                ),
                'ai_recommendation_ne': (
                    'यो करारमा ओभरटाइम भुक्तानी, राहदानी जफत, र करार समाप्तिका बारेमा '
                    'चिन्ताजनक धाराहरू छन्। हस्ताक्षर गर्नु अघि कानूनी सल्लाहकारसँग '
                    'परामर्श गर्न सिफारिस गरिन्छ।'
                ),
            },
        )

        clauses_data = [
            {
                'clause_reference': 'Clause 8.3',
                'title': 'Passport Retention by Employer',
                'severity': 'illegal',
                'original_text': 'The employee shall surrender their passport to the employer for safekeeping during the employment period.',
                'explanation_ne': 'यो धाराले भन्छ कि रोजगारदाताले तपाईंको राहदानी राख्नेछ। यो मलेसियाको कानून अनुसार अवैध हो।',
                'recommendation': 'NEVER surrender your passport. This is illegal under Malaysian labor law.',
            },
            {
                'clause_reference': 'Clause 12.1',
                'title': 'Unlimited Overtime Without Pay',
                'severity': 'high_risk',
                'original_text': 'The employee agrees to work additional hours as required by the employer without additional compensation.',
                'explanation_ne': 'यो धाराले भन्छ कि तपाईंले थप तलब बिना ओभरटाइम काम गर्नुपर्छ। यो उच्च जोखिमपूर्ण छ।',
                'recommendation': 'Overtime must be compensated. Request revision to include overtime pay rate.',
            },
            {
                'clause_reference': 'Clause 15.4',
                'title': 'Penalty for Early Termination',
                'severity': 'warning',
                'original_text': 'If the employee terminates the contract before 2 years, a penalty of 3 months salary shall be deducted.',
                'explanation_ne': 'यदि तपाईंले २ वर्ष अघि नै काम छोड्नुभयो भने ३ महिनाको तलब काटिनेछ।',
                'recommendation': 'Negotiate the penalty clause to a maximum of 1 month salary.',
            },
        ]
        for c in clauses_data:
            FlaggedClause.objects.get_or_create(analysis=analysis, clause_reference=c['clause_reference'], defaults=c)
        self.stdout.write(self.style.SUCCESS('  ✓ Contract analysis & flagged clauses'))

        # ── Safety Check-ins ───────────────────────────
        now = timezone.now()
        for i in range(5):
            dt = now - timedelta(days=i)
            if not SafetyCheckIn.objects.filter(user=worker, checked_in_at__date=dt.date()).exists():
                SafetyCheckIn.objects.create(
                    user=worker,
                    status='safe',
                    checked_in_at=dt.replace(hour=8, minute=0),
                )
        self.stdout.write(self.style.SUCCESS('  ✓ Safety check-ins (last 5 days)'))

        # ── Embassies ──────────────────────────────────
        embassies_data = [
            {
                'name': 'Embassy of Nepal in Malaysia',
                'country': 'Malaysia',
                'city': 'Kuala Lumpur',
                'phone': '+60-3-20203573',
                'address': 'No. 36, Jalan Taman Duta, Off Jalan Duta, 50480 Kuala Lumpur',
                'labor_attache': 'Mr. Deepak Gurung',
                'office_hours': 'Mon–Fri 09:00–17:00',
                'latitude': 3.1750,
                'longitude': 101.6780,
            },
            {
                'name': 'Nepal Honorary Consulate – Penang',
                'country': 'Malaysia',
                'city': 'Penang',
                'phone': '+60-4-2625373',
                'address': 'Wisma Yeap Chor Ee, 1 Gat Lebuh China, 10100 George Town, Penang',
                'labor_attache': 'Mr. Ramesh Shrestha',
                'office_hours': 'Mon–Fri 09:00–16:00',
                'latitude': 5.4141,
                'longitude': 100.3288,
            },
            {
                'name': 'Nepal Honorary Consulate – Johor Bahru',
                'country': 'Malaysia',
                'city': 'Johor Bahru',
                'phone': '+60-7-2233456',
                'address': 'Jalan Yahya Awal, 80100 Johor Bahru, Johor',
                'labor_attache': 'Ms. Anita Poudel',
                'office_hours': 'Mon–Fri 09:00–16:00',
                'latitude': 1.4655,
                'longitude': 103.7578,
            },
            {
                'name': 'Malaysian Immigration Department (HQ)',
                'country': 'Malaysia',
                'city': 'Putrajaya',
                'phone': '+60-3-88801000',
                'address': 'No. 15, Persiaran Perdana, Presint 2, 62550 Putrajaya',
                'labor_attache': '',
                'office_hours': 'Mon–Fri 08:00–17:00',
                'latitude': 2.9264,
                'longitude': 101.6964,
            },
            {
                'name': 'Ministry of Human Resources Malaysia',
                'country': 'Malaysia',
                'city': 'Putrajaya',
                'phone': '+60-3-88865000',
                'address': 'Aras 6-9, Blok D3, Parcel D, Pusat Pentadbiran Kerajaan Persekutuan, 62530 Putrajaya',
                'labor_attache': '',
                'office_hours': 'Mon–Fri 08:00–17:00',
                'latitude': 2.9320,
                'longitude': 101.6932,
            },
            {
                'name': 'Tenaganita Migrant Worker Resource Centre',
                'country': 'Malaysia',
                'city': 'Kuala Lumpur',
                'phone': '+60-3-26917564',
                'address': '29, Jalan Titiwangsa 1, 54000 Kuala Lumpur',
                'labor_attache': '',
                'office_hours': 'Mon–Fri 09:00–17:00',
                'latitude': 3.1800,
                'longitude': 101.7060,
            },
        ]
        for e in embassies_data:
            Embassy.objects.get_or_create(name=e['name'], defaults=e)
        self.stdout.write(self.style.SUCCESS('  ✓ Embassies & key offices (6)'))

        # ── Communities ────────────────────────────────
        communities_data = [
            {
                'name': 'NRNA Malaysia Chapter',
                'city': 'Kuala Lumpur',
                'country': 'Malaysia',
                'community_type': 'nrna',
                'contact_person': 'Kamala Rai',
                'phone': '+60-112345678',
                'operating_hours': 'Sat–Sun 10:00–16:00',
                'latitude': 3.1520,
                'longitude': 101.7110,
            },
            {
                'name': 'Nepali Workers Welfare Society – KL',
                'city': 'Kuala Lumpur',
                'country': 'Malaysia',
                'community_type': 'welfare',
                'contact_person': 'Bishnu Adhikari',
                'phone': '+60-123456789',
                'operating_hours': 'Mon–Fri 09:00–17:00',
                'latitude': 3.1390,
                'longitude': 101.6869,
            },
            {
                'name': 'Migrant Workers Legal Aid – Malaysia',
                'city': 'Kuala Lumpur',
                'country': 'Malaysia',
                'community_type': 'legal',
                'contact_person': 'Tika Bhattarai',
                'phone': '+60-132345678',
                'operating_hours': 'Mon–Fri 09:00–17:00',
                'latitude': 3.1570,
                'longitude': 101.7120,
            },
            {
                'name': 'Prabasi Nepali Samuha – Penang',
                'city': 'Penang',
                'country': 'Malaysia',
                'community_type': 'community',
                'contact_person': 'Suresh Magar',
                'phone': '+60-145678901',
                'operating_hours': 'Sat 10:00–16:00',
                'latitude': 5.4141,
                'longitude': 100.3288,
            },
            {
                'name': 'Nepal Community Center – Johor Bahru',
                'city': 'Johor Bahru',
                'country': 'Malaysia',
                'community_type': 'community',
                'contact_person': 'Ganesh Pandey',
                'phone': '+60-167890123',
                'operating_hours': 'Sat–Sun 10:00–18:00',
                'latitude': 1.4655,
                'longitude': 103.7578,
            },
            {
                'name': 'Tenaganita Migrant Support Centre',
                'city': 'Kuala Lumpur',
                'country': 'Malaysia',
                'community_type': 'welfare',
                'contact_person': 'Aegile Fernandez',
                'phone': '+60-3-26917564',
                'operating_hours': 'Mon–Fri 09:00–17:00',
                'latitude': 3.1800,
                'longitude': 101.7060,
            },
        ]
        for c in communities_data:
            Community.objects.get_or_create(name=c['name'], defaults=c)
        self.stdout.write(self.style.SUCCESS('  ✓ Communities (6)'))

        # ── Checklist Items ────────────────────────────
        checklist_data = [
            {'title': 'राहदानी (Passport)', 'description': 'विदेश जानका लागि कम्तीमा ६ महिनासम्म म्याद भएको राहदानी अनिवार्य हुन्छ। राहदानीमा स्पष्ट फोटो र व्यक्तिगत विवरण मिलेको हुनुपर्छ।', 'category': 'documents', 'icon': 'description', 'order': 1},
            {'title': 'रोजगार प्रस्ताव पत्र (Job Offer Letter)', 'description': 'विदेशी रोजगारदाताबाट प्राप्त आधिकारिक पत्र हो जसमा कामको पद, तलब, काम गर्ने स्थान र अन्य सर्तहरू उल्लेख गरिएको हुन्छ।', 'category': 'documents', 'icon': 'mail_outline', 'order': 2},
            {'title': 'रोजगार सम्झौता (Employment Contract)', 'description': 'कामदार र रोजगारदाताबीच भएको कानुनी सम्झौता हो। यसमा कामको अवधि, तलब, सुविधा, काम गर्ने समय लगायतका विवरणहरू हुन्छन्।', 'category': 'legal', 'icon': 'handshake', 'order': 3},
            {'title': 'पासपोर्ट साइज फोटो', 'description': 'हालै खिचिएको फोटो आवश्यक पर्छ। फोटो प्रायः सेतो पृष्ठभूमिमा र दूतावासको मापदण्ड अनुसार हुनुपर्छ।', 'category': 'documents', 'icon': 'photo_camera', 'order': 4},
            {'title': 'मेडिकल परीक्षण रिपोर्ट (Medical Report)', 'description': 'मान्यताप्राप्त मेडिकल सेन्टरबाट गरिएको स्वास्थ्य परीक्षणको रिपोर्ट हो। संक्रामक रोग नभएको प्रमाणित हुनुपर्छ।', 'category': 'health', 'icon': 'health_and_safety', 'order': 5},
            {'title': 'प्रहरी चारित्रिक प्रमाणपत्र (Police Clearance)', 'description': 'नेपाल प्रहरीबाट जारी गरिने प्रमाणपत्र हो जसले व्यक्तिको आपराधिक रेकर्ड नभएको प्रमाणित गर्छ।', 'category': 'legal', 'icon': 'gavel', 'order': 6},
            {'title': 'शैक्षिक प्रमाणपत्र (Educational Certificates)', 'description': 'आवश्यक परेमा शैक्षिक योग्यता प्रमाणित गर्ने प्रमाणपत्रहरू (जस्तै SEE, +2, Diploma आदि) पेश गर्नुपर्छ।', 'category': 'documents', 'icon': 'school', 'order': 7},
            {'title': 'सीप वा तालिम प्रमाणपत्र (Skill Certificate)', 'description': 'विशेष सीप सम्बन्धी कामका लागि तालिम वा अनुभव प्रमाणित गर्ने कागजात आवश्यक पर्न सक्छ।', 'category': 'training', 'icon': 'card_membership', 'order': 8},
            {'title': 'भिसा आवेदन फाराम (Visa Application Form)', 'description': 'सम्बन्धित देशको दूतावास वा रोजगारदातामार्फत भर्ने आधिकारिक फाराम हो।', 'category': 'documents', 'icon': 'receipt', 'order': 9},
            {'title': 'श्रम स्वीकृति (Labour Approval)', 'description': 'नेपाल सरकारको वैदेशिक रोजगार विभागबाट प्राप्त स्वीकृति हो, जुन वैदेशिक रोजगारीका लागि अनिवार्य हुन्छ।', 'category': 'legal', 'icon': 'verified', 'order': 10},
            {'title': 'स्वास्थ्य बीमा (Health Insurance)', 'description': 'केही देशहरूमा अनिवार्य स्वास्थ्य बीमा कागजात आवश्यक हुन्छ, जसले विदेश बसाइँ अवधिमा स्वास्थ्य उपचार कभर गर्छ।', 'category': 'health', 'icon': 'medical_services', 'order': 11},
        ]
        for item_data in checklist_data:
            item, _ = ChecklistItem.objects.get_or_create(title=item_data['title'], defaults=item_data)
            UserChecklistProgress.objects.get_or_create(
                user=worker,
                item=item,
                defaults={
                    'status': 'completed' if item_data['order'] <= 4 else ('active' if item_data['order'] == 5 else 'pending'),
                    'completed_at': timezone.now() if item_data['order'] <= 4 else None,
                },
            )
        self.stdout.write(self.style.SUCCESS('  ✓ Checklist items (11) with progress'))

        # ── Notifications ──────────────────────────────
        # Clear existing notifications for clean seeding
        Notification.objects.filter(user=worker).delete()
        
        notifications_data = [
            {'title': 'Daily Check-in Reminder', 'description': 'Don\'t forget to check in today to let your family know you\'re safe.', 'category': 'reminder', 'is_read': False},
            {'title': 'Contract Analysis Complete', 'description': 'Your contract "sunway_contract.pdf" has been analyzed. 3 risky clauses found.', 'category': 'contract', 'is_read': False},
            {'title': 'New Community Event', 'description': 'Nepali Workers Welfare Society – KL is hosting a gathering this Saturday.', 'category': 'community', 'is_read': True},
            {'title': 'Document Verified', 'description': 'Your passport document has been verified successfully.', 'category': 'document', 'is_read': True},
            {'title': 'Safety Alert – Heat Advisory', 'description': 'Temperature expected to exceed 37°C tomorrow in KL. Stay hydrated and take breaks in shade between 12PM–3PM.', 'category': 'safety', 'is_read': False},
        ]
        for n in notifications_data:
            Notification.objects.create(
                user=worker,
                title=n['title'],
                description=n['description'],
                category=n['category'],
                is_read=n['is_read'],
            )
        self.stdout.write(self.style.SUCCESS('  ✓ Notifications (5)'))

        # ── Activity Logs ──────────────────────────────
        logs_data = [
            {'event_type': 'check_in', 'description': 'Checked in – Safe'},
            {'event_type': 'document', 'description': 'Uploaded passport document'},
            {'event_type': 'contract', 'description': 'Contract "sunway_contract.pdf" analyzed'},
            {'event_type': 'profile', 'description': 'Updated profile settings'},
        ]
        for log in logs_data:
            ActivityLog.objects.get_or_create(
                user=worker,
                description=log['description'],
                defaults={'event_type': log['event_type']},
            )
        self.stdout.write(self.style.SUCCESS('  ✓ Activity logs'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('═' * 50))
        self.stdout.write(self.style.SUCCESS('  Database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('  Demo accounts:'))
        self.stdout.write(self.style.SUCCESS('    Worker: ram / worker123'))
        self.stdout.write(self.style.SUCCESS('    Family: sita / family123'))
        self.stdout.write(self.style.SUCCESS('    Admin:  admin / admin123'))
        self.stdout.write(self.style.SUCCESS('═' * 50))
