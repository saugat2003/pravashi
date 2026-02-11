"""
Management command to seed the database with realistic data for Pradesh Setu.
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
    help = 'Seed the database with sample data for Pradesh Setu demo'

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
                'current_country': 'Qatar',
                'current_city': 'Doha',
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
            {'name': 'Nepali Embassy Qatar', 'relationship': 'Embassy', 'phone': '+974-44422880'},
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
            employer_name='Al Rayyan Construction Co.',
            defaults={
                'file': 'contracts/al_rayyan_contract.pdf',
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
                'explanation_ne': 'यो धाराले भन्छ कि रोजगारदाताले तपाईंको राहदानी राख्नेछ। यो कतारको कानून अनुसार अवैध हो।',
                'recommendation': 'NEVER surrender your passport. This is illegal under Qatari labor law.',
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
                'name': 'Embassy of Nepal in Qatar',
                'country': 'Qatar',
                'city': 'Doha',
                'phone': '+974-44422880',
                'address': 'West Bay, Diplomatic Area, Doha',
                'labor_attache': 'Mr. Mohan Khanal',
                'office_hours': 'Sun–Thu 09:00–17:00',
            },
            {
                'name': 'Embassy of Nepal in UAE',
                'country': 'UAE',
                'city': 'Abu Dhabi',
                'phone': '+971-2-6327603',
                'address': 'Embassy Area, Abu Dhabi',
                'labor_attache': 'Mr. Binod Sharma',
                'office_hours': 'Sun–Thu 09:00–16:00',
            },
            {
                'name': 'Embassy of Nepal in Saudi Arabia',
                'country': 'Saudi Arabia',
                'city': 'Riyadh',
                'phone': '+966-1-4632804',
                'address': 'Diplomatic Quarter, Riyadh',
                'labor_attache': 'Ms. Anita Poudel',
                'office_hours': 'Sun–Thu 08:00–15:00',
            },
            {
                'name': 'Embassy of Nepal in Kuwait',
                'country': 'Kuwait',
                'city': 'Kuwait City',
                'phone': '+965-22561003',
                'address': 'Mishref, Kuwait City',
                'labor_attache': 'Mr. Suman Bajracharya',
                'office_hours': 'Sun–Thu 08:30–15:30',
            },
            {
                'name': 'Embassy of Nepal in Malaysia',
                'country': 'Malaysia',
                'city': 'Kuala Lumpur',
                'phone': '+60-3-20203573',
                'address': 'Jalan Taman Duta, Kuala Lumpur',
                'labor_attache': 'Mr. Deepak Gurung',
                'office_hours': 'Mon–Fri 09:00–17:00',
            },
            {
                'name': 'Consulate General of Nepal in South Korea',
                'country': 'South Korea',
                'city': 'Seoul',
                'phone': '+82-2-37891017',
                'address': 'Hangangno, Yongsan-gu, Seoul',
                'labor_attache': 'Ms. Renuka Tamang',
                'office_hours': 'Mon–Fri 09:00–17:00',
            },
        ]
        for e in embassies_data:
            Embassy.objects.get_or_create(name=e['name'], defaults=e)
        self.stdout.write(self.style.SUCCESS('  ✓ Embassies (6)'))

        # ── Communities ────────────────────────────────
        communities_data = [
            {
                'name': 'Nepali Workers Welfare Society – Qatar',
                'city': 'Doha',
                'country': 'Qatar',
                'community_type': 'welfare',
                'contact_person': 'Bishnu Adhikari',
                'phone': '+974-55123456',
                'operating_hours': 'Fri 10:00–18:00',
            },
            {
                'name': 'NRNA Qatar Chapter',
                'city': 'Doha',
                'country': 'Qatar',
                'community_type': 'nrna',
                'contact_person': 'Kamala Rai',
                'phone': '+974-55234567',
                'operating_hours': 'Fri–Sat 10:00–16:00',
            },
            {
                'name': 'Prabasi Nepali Samuha – UAE',
                'city': 'Dubai',
                'country': 'UAE',
                'community_type': 'community',
                'contact_person': 'Suresh Magar',
                'phone': '+971-551234567',
                'operating_hours': 'Fri 11:00–17:00',
            },
            {
                'name': 'Migrant Workers Legal Aid – Malaysia',
                'city': 'Kuala Lumpur',
                'country': 'Malaysia',
                'community_type': 'legal',
                'contact_person': 'Tika Bhattarai',
                'phone': '+60-112345678',
                'operating_hours': 'Mon–Fri 09:00–17:00',
            },
            {
                'name': 'Nepal Community Center – Riyadh',
                'city': 'Riyadh',
                'country': 'Saudi Arabia',
                'community_type': 'community',
                'contact_person': 'Ganesh Pandey',
                'phone': '+966-551234567',
                'operating_hours': 'Fri 14:00–20:00',
            },
        ]
        for c in communities_data:
            Community.objects.get_or_create(name=c['name'], defaults=c)
        self.stdout.write(self.style.SUCCESS('  ✓ Communities (5)'))

        # ── Checklist Items ────────────────────────────
        checklist_data = [
            {'title': 'Verify Passport Validity', 'description': 'Ensure passport is valid for at least 6 months beyond travel date.', 'category': 'documents', 'order': 1},
            {'title': 'Get Work Visa', 'description': 'Apply for and obtain the correct work visa for your destination country.', 'category': 'documents', 'order': 2},
            {'title': 'Medical Examination', 'description': 'Complete required medical tests at an approved center.', 'category': 'health', 'order': 3},
            {'title': 'Attend Pre-departure Orientation', 'description': 'Complete the mandatory pre-departure orientation training.', 'category': 'training', 'order': 4},
            {'title': 'Employment Contract Review', 'description': 'Have your contract reviewed by a legal expert before signing.', 'category': 'legal', 'order': 5},
            {'title': 'Embassy Registration', 'description': 'Register with the Nepali embassy in your destination country on arrival.', 'category': 'safety', 'order': 6},
            {'title': 'Save Emergency Numbers', 'description': 'Save embassy, police, and emergency contact numbers in your phone.', 'category': 'safety', 'order': 7},
            {'title': 'Financial Planning', 'description': 'Set up a bank account and remittance plan for sending money home.', 'category': 'finance', 'order': 8},
            {'title': 'Insurance Coverage', 'description': 'Get health and accident insurance before departure.', 'category': 'health', 'order': 9},
            {'title': 'Learn Basic Local Language', 'description': 'Learn basic phrases in Arabic, Malay, or Korean depending on destination.', 'category': 'training', 'order': 10},
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
        self.stdout.write(self.style.SUCCESS('  ✓ Checklist items (10) with progress'))

        # ── Notifications ──────────────────────────────
        notifications_data = [
            {'title': 'Daily Check-in Reminder', 'description': 'Don\'t forget to check in today to let your family know you\'re safe.', 'category': 'reminder', 'is_read': False},
            {'title': 'Contract Analysis Complete', 'description': 'Your contract "al_rayyan_contract.pdf" has been analyzed. 3 risky clauses found.', 'category': 'contract', 'is_read': False},
            {'title': 'New Community Event', 'description': 'Nepali Workers Welfare Society is hosting a gathering this Friday.', 'category': 'community', 'is_read': True},
            {'title': 'Document Verified', 'description': 'Your passport document has been verified successfully.', 'category': 'document', 'is_read': True},
            {'title': 'Safety Alert – Extreme Heat', 'description': 'Temperature expected to exceed 45°C tomorrow. Stay hydrated and avoid outdoor work between 11AM–3PM.', 'category': 'safety', 'is_read': False},
        ]
        for n in notifications_data:
            Notification.objects.get_or_create(
                user=worker,
                title=n['title'],
                defaults={
                    'description': n['description'],
                    'category': n['category'],
                    'is_read': n['is_read'],
                },
            )
        self.stdout.write(self.style.SUCCESS('  ✓ Notifications (5)'))

        # ── Activity Logs ──────────────────────────────
        logs_data = [
            {'event_type': 'check_in', 'description': 'Checked in – Safe'},
            {'event_type': 'document', 'description': 'Uploaded passport document'},
            {'event_type': 'contract', 'description': 'Contract "al_rayyan_contract.pdf" analyzed'},
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
