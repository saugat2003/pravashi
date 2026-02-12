from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, FileResponse, Http404, HttpResponseForbidden
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
import json

from .models import (
    User, EmergencyContact, Document, ContractAnalysis, FlaggedClause,
    SafetyCheckIn, SOSEvent, Embassy, EmbassyBookmark, Community,
    ChecklistItem, UserChecklistProgress, Notification, ActivityLog,
)
from .forms import (
    RegisterForm, ProfileUpdateForm, EmergencyContactForm,
    DocumentUploadForm, ContractUploadForm, SafetyCheckInForm, SOSEventForm,
)


# ─── Helpers ─────────────────────────────────

def _unread_count(user):
    """Return count of unread notifications for nav badge."""
    if user.is_authenticated:
        return user.notifications.filter(is_read=False).count()
    return 0


def _log_activity(user, event_type, description=''):
    """Create an activity log entry (visible to family)."""
    ActivityLog.objects.create(user=user, event_type=event_type, description=description)


# ─── Auth ────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('main:home')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'main/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Initialize checklist progress for new users
            for item in ChecklistItem.objects.all():
                UserChecklistProgress.objects.get_or_create(user=user, item=item)
            Notification.objects.create(
                user=user,
                category='general',
                title='Welcome to Pradesh Setu!',
                description='Your account has been created. Start by uploading your documents.',
            )
            return redirect('main:home')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main:onboarding_welcome')


# ─── Onboarding ─────────────────────────────

def onboarding_welcome(request):
    return render(request, 'main/onboarding_welcome.html')


def onboarding_key_features(request):
    return render(request, 'main/onboarding_key_features.html')


def onboarding_profile_selection(request):
    return render(request, 'main/onboarding_profile_selection.html')


# ─── Home Dashboard ─────────────────────────

@login_required(login_url='main:login')
def home(request):
    user = request.user

    # Nearest embassy based on user's current country
    nearest_embassy = Embassy.objects.filter(
        country__icontains=user.current_country
    ).first() if user.current_country else Embassy.objects.first()

    # Documents status
    total_doc_types = 4  # passport, visa, contract, citizenship
    uploaded_docs = user.documents.count()
    verified_docs = user.documents.filter(verification_status='verified').count()
    docs_up_to_date = verified_docs >= total_doc_types

    # Recent contract analysis
    latest_analysis = user.contract_analyses.first()

    # Today's check-in status
    today = timezone.now().date()
    last_checkin = user.safety_checkins.order_by('-checked_in_at').first()
    checked_in_today = last_checkin and last_checkin.checked_in_at.date() == today

    context = {
        'user': user,
        'nearest_embassy': nearest_embassy,
        'unread_count': _unread_count(user),
        'docs_up_to_date': docs_up_to_date,
        'uploaded_docs': uploaded_docs,
        'total_doc_types': total_doc_types,
        'latest_analysis': latest_analysis,
        'checked_in_today': checked_in_today,
        'last_checkin': last_checkin,
    }
    return render(request, 'main/home.html', context)


# ─── Worker Profile & Settings ───────────────

@login_required(login_url='main:login')
def worker_profile_settings(request):
    user = request.user

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_profile':
            form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated.')
                return redirect('main:worker_profile_settings')

        elif action == 'toggle_location_sharing':
            user.location_sharing = not user.location_sharing
            user.save(update_fields=['location_sharing'])
            # If the request is AJAX return JSON, otherwise redirect back
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'location_sharing': user.location_sharing})
            return redirect('main:worker_profile_settings')

        elif action == 'toggle_dark_mode':
            user.dark_mode = not user.dark_mode
            user.save(update_fields=['dark_mode'])
            # If the request is AJAX return JSON, otherwise redirect back
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'dark_mode': user.dark_mode})
            return redirect('main:worker_profile_settings')

        elif action == 'toggle_checkin_reminders':
            user.checkin_reminders = not user.checkin_reminders
            user.save(update_fields=['checkin_reminders'])
            # If the request is AJAX return JSON, otherwise redirect back
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'checkin_reminders': user.checkin_reminders})
            return redirect('main:worker_profile_settings')

        elif action == 'change_language':
            lang = request.POST.get('language', 'en')
            user.language_preference = lang
            user.save(update_fields=['language_preference'])
            return redirect('main:worker_profile_settings')

    # Documents summary
    passport = user.documents.filter(doc_type='passport').first()
    visa = user.documents.filter(doc_type='work_visa').first()
    contract = user.documents.filter(doc_type='employment_contract').first()

    context = {
        'user': user,
        'passport': passport,
        'visa': visa,
        'contract': contract,
        'unread_count': _unread_count(user),
        'emergency_contacts': user.emergency_contacts.all(),
        # Country-level emergency contacts (police, fire, ambulance, embassy)
        # Default to Dubai emergency numbers (hardcoded per request)
        'country_contacts': {
            'police': '999',
            'fire': '997',
            'ambulance': '998',
            'embassy': None,
        },
    }
    # Try to populate country-level emergency numbers from Embassy model and a small lookup
    if user.current_country:
        # prefer embassy contact info when available
        embassy = Embassy.objects.filter(country__icontains=user.current_country).first()
        if embassy:
            context['country_contacts']['embassy'] = embassy.emergency_hotline or embassy.phone

        # Simple fallback mapping for common countries (extend as needed)
        fallback = {
            'nepal': {'police': '100', 'fire': '101', 'ambulance': '102'},
            'qatar': {'police': '999', 'fire': '999', 'ambulance': '999'},
            'india': {'police': '100', 'fire': '101', 'ambulance': '102'},
            'uae': {'police': '999', 'fire': '998', 'ambulance': '998'},
        }
        key = user.current_country.strip().lower()
        for country_key, numbers in fallback.items():
            if country_key in key:
                context['country_contacts'].update(numbers)
                break
    return render(request, 'main/worker_profile_settings.html', context)


# ─── Document Vault ──────────────────────────

@login_required(login_url='main:login')
def secure_document_vault(request):
    user = request.user

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = user
            doc.save()
            _log_activity(user, 'document', f'{doc.get_doc_type_display()} uploaded')
            Notification.objects.create(
                user=user, category='document',
                title='Document Uploaded',
                description=f'Your {doc.get_doc_type_display()} was securely stored.',
            )
            messages.success(request, f'{doc.get_doc_type_display()} uploaded successfully.')
            return redirect('main:secure_document_vault')
    else:
        form = DocumentUploadForm()

    uploaded_docs = user.documents.all()
    # Determine which types are still pending
    uploaded_types = set(uploaded_docs.values_list('doc_type', flat=True))
    all_types = [
        ('passport', 'Passport'),
        ('work_visa', 'Work Visa'),
        ('employment_contract', 'Employment Contract'),
        ('citizenship', 'Citizenship Certificate'),
        ('insurance', 'Insurance Policy'),
        ('other', 'Other'),
    ]
    pending_types = [{'value': t, 'label': label} for t, label in all_types if t not in uploaded_types]
    doc_total = len(all_types)

    context = {
        'uploaded_docs': uploaded_docs,
        'pending_types': pending_types,
        'doc_total': doc_total,
        'form': form,
        'unread_count': _unread_count(user),
    }
    return render(request, 'main/secure_document_vault.html', context)


# Download a stored document (owner-only)
@login_required(login_url='main:login')
def document_download(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    if doc.user != request.user:
        return HttpResponseForbidden()
    try:
        f = doc.file.open('rb')
        filename = doc.file.name.split('/')[-1]
        return FileResponse(f, as_attachment=True, filename=filename)
    except Exception:
        raise Http404('File not found')


# Remove a stored document (owner-only, POST only)
@login_required(login_url='main:login')
def document_delete(request, pk):
    doc = get_object_or_404(Document, pk=pk, user=request.user)
    if request.method != 'POST':
        return HttpResponseForbidden()
    # remove file from storage then delete record
    try:
        doc.file.delete(save=False)
    except Exception:
        pass
    doc.delete()
    messages.success(request, 'Document removed.')
    _log_activity(request.user, 'document', f'{doc.get_doc_type_display()} deleted')
    return redirect('main:secure_document_vault')


@login_required(login_url='main:login')
def document_upload_ajax(request):
    """Accepts a multipart/form-data POST and returns JSON for dynamic UI updates."""
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'POST required'}, status=405)

    form = DocumentUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

    doc = form.save(commit=False)
    doc.user = request.user
    doc.save()

    _log_activity(request.user, 'document', f'{doc.get_doc_type_display()} uploaded')
    Notification.objects.create(
        user=request.user, category='document',
        title='Document Uploaded',
        description=f'Your {doc.get_doc_type_display()} was securely stored.',
    )

    data = {
        'id': doc.pk,
        'doc_type': doc.doc_type,
        'doc_label': doc.get_doc_type_display(),
        'uploaded_at': doc.uploaded_at.strftime('%d %b %Y'),
        'verification_status': doc.verification_status,
        'download_url': reverse('main:document_download', args=[doc.pk]),
        'delete_url': reverse('main:document_delete', args=[doc.pk]),
    }

    return JsonResponse({'ok': True, 'doc': data})


# ─── Contract Analysis ───────────────────────

@login_required(login_url='main:login')
def contract_analysis_upload(request):
    user = request.user

    if request.method == 'POST':
        form = ContractUploadForm(request.POST, request.FILES)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.user = user
            # Simulate AI analysis (in production, call AI service here)
            import random
            analysis.risk_score = random.randint(15, 95)
            if analysis.risk_score >= 70:
                analysis.risk_level = 'high'
            elif analysis.risk_score >= 40:
                analysis.risk_level = 'medium'
            else:
                analysis.risk_level = 'low'
            analysis.ai_recommendation = (
                'Do not sign this contract.' if analysis.risk_score >= 70
                else 'Review flagged clauses carefully.' if analysis.risk_score >= 40
                else 'This contract appears safe.'
            )
            analysis.ai_recommendation_ne = (
                'यो सम्झौतामा हस्ताक्षर नगर्नुहोस्।' if analysis.risk_score >= 70
                else 'चिन्हित धाराहरू ध्यानपूर्वक समीक्षा गर्नुहोस्।' if analysis.risk_score >= 40
                else 'यो सम्झौता सुरक्षित देखिन्छ।'
            )
            analysis.save()

            # Create sample flagged clauses (simulated AI output)
            if analysis.risk_score >= 40:
                FlaggedClause.objects.create(
                    analysis=analysis,
                    clause_reference='Clause 7.1',
                    title='Passport Retention',
                    severity='illegal',
                    original_text='The employee agrees to surrender their passport to the employer upon arrival for safekeeping purposes.',
                    explanation_ne='रोजगारदाताले तपाइँको राहदानी राख्नु गैरकानूनी हो। यसले तपाइँको स्वतन्त्रतामा बाधा पुर्‍याउँछ।',
                    recommendation='Never surrender your passport. This is illegal under international law.',
                )
            if analysis.risk_score >= 60:
                FlaggedClause.objects.create(
                    analysis=analysis,
                    clause_reference='Clause 4.2',
                    title='Undefined Overtime Pay',
                    severity='warning',
                    original_text='Any additional hours will be compensated at the discretion of the employer.',
                    explanation_ne='ओभरटाइम दर तोकिएको छैन। रोजगारदाताको तजबिजमा भन्नुको अर्थ भुक्तानी नपाउन पनि सकिन्छ।',
                    recommendation='Ensure overtime rate is clearly defined in writing.',
                )

            _log_activity(user, 'contract', f'Contract analyzed: {analysis.employer_name}')
            Notification.objects.create(
                user=user, category='contract',
                title='Contract Analysis Complete',
                description=f'{analysis.flagged_clauses.count()} clauses flagged for review.',
            )
            return redirect('main:contract_risk_report', pk=analysis.pk)
    else:
        form = ContractUploadForm()

    recent_analyses = user.contract_analyses.all()[:5]

    context = {
        'form': form,
        'recent_analyses': recent_analyses,
        'unread_count': _unread_count(user),
    }
    return render(request, 'main/contract_analysis_upload.html', context)


@login_required(login_url='main:login')
def contract_risk_report(request, pk=None):
    if pk:
        analysis = get_object_or_404(ContractAnalysis, pk=pk, user=request.user)
    else:
        analysis = request.user.contract_analyses.first()
        if not analysis:
            return redirect('main:contract_analysis_upload')

    clauses = analysis.flagged_clauses.all()

    context = {
        'analysis': analysis,
        'clauses': clauses,
        'unread_count': _unread_count(request.user),
    }
    return render(request, 'main/contract_risk_report.html', context)


@login_required(login_url='main:login')
def detailed_ai_clause_analysis(request, pk=None):
    if pk:
        analysis = get_object_or_404(ContractAnalysis, pk=pk, user=request.user)
    else:
        analysis = request.user.contract_analyses.first()
        if not analysis:
            return redirect('main:contract_analysis_upload')

    clauses = analysis.flagged_clauses.all()

    context = {
        'analysis': analysis,
        'clauses': clauses,
        'unread_count': _unread_count(request.user),
    }
    return render(request, 'main/detailed_ai_clause_analysis.html', context)


# ─── Daily Safety Check-In ───────────────────

@login_required(login_url='main:login')
def daily_safety_check_in(request):
    user = request.user

    if request.method == 'POST':
        status = request.POST.get('status', 'safe')
        checkin = SafetyCheckIn.objects.create(user=user, status=status)
        _log_activity(user, 'check_in', f'Marked as {checkin.get_status_display()}')

        if status == 'need_help':
            return redirect('main:emergency_sos_activation')

        messages.success(request, 'Check-in recorded. Stay safe!')
        return redirect('main:daily_safety_check_in')

    # Recent check-ins
    checkins = user.safety_checkins.all()[:10]

    # 7-day calendar data
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())  # Monday
    week_days = []
    for i in range(7):
        day = week_start + timedelta(days=i)
        checked = user.safety_checkins.filter(checked_in_at__date=day).exists()
        week_days.append({'date': day, 'day': day.day, 'label': day.strftime('%a'), 'checked_in': checked, 'is_today': day == today})

    context = {
        'checkins': checkins,
        'week_days': week_days,
        'unread_count': _unread_count(user),
    }
    return render(request, 'main/daily_safety_check_in.html', context)


# ─── Emergency SOS ───────────────────────────

@login_required(login_url='main:login')
def emergency_sos_activation(request):
    user = request.user

    if request.method == 'POST':
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        signal = request.POST.get('signal_strength', '')
        battery = request.POST.get('battery_level')

        sos = SOSEvent.objects.create(
            user=user,
            latitude=float(lat) if lat else None,
            longitude=float(lon) if lon else None,
            signal_strength=signal,
            battery_level=int(battery) if battery else None,
            status='active',
        )
        _log_activity(user, 'sos', 'Emergency SOS activated')
        Notification.objects.create(
            user=user, category='safety',
            title='SOS Alert Sent',
            description='Your emergency alert has been dispatched to contacts and embassy.',
        )
        # Also notify family members
        for family in user.family_members.all():
            Notification.objects.create(
                user=family, category='safety',
                title=f'SOS Alert from {user.get_full_name() or user.username}',
                description='An emergency SOS has been activated. Check the family dashboard.',
            )
        return JsonResponse({'status': 'active', 'sos_id': sos.pk})

    context = {
        'user': user,
        'unread_count': _unread_count(user),
        'user_lat': user.latitude if user.latitude else 27.7172,
        'user_lon': user.longitude if user.longitude else 85.3240,
    }
    return render(request, 'main/emergency_sos_activation.html', context)


@login_required(login_url='main:login')
def sos_countdown_timer(request):
    return render(request, 'main/sos_countdown_timer.html', {
        'unread_count': _unread_count(request.user),
    })


# ─── Family Safety Dashboard ─────────────────

@login_required(login_url='main:login')
def family_safety_dashboard(request):
    user = request.user

    # Get the worker being monitored
    worker = user.monitored_worker
    if not worker and user.profile_type == 'worker':
        # If the user is a worker, show their own data
        worker = user

    last_checkin = worker.safety_checkins.first() if worker else None
    activity_logs = worker.activity_logs.all()[:10] if worker else []
    is_safe = last_checkin.status == 'safe' if last_checkin else True

    # Get worker's location for map
    worker_lat = worker.latitude if worker and worker.latitude else 25.2854  # Default to Doha, Qatar
    worker_lon = worker.longitude if worker and worker.longitude else 51.5310

    context = {
        'worker': worker,
        'last_checkin': last_checkin,
        'activity_logs': activity_logs,
        'is_safe': is_safe,
        'worker_lat': worker_lat,
        'worker_lon': worker_lon,
        'unread_count': _unread_count(user),
    }
    return render(request, 'main/family_safety_dashboard.html', context)


# ─── Embassy Contact Directory ────────────────

@login_required(login_url='main:login')
def embassy_contact_directory(request):
    user = request.user
    query = request.GET.get('q', '')

    # Filter embassies by current country (unless searching)
    embassies = Embassy.objects.all()
    if user.current_country and not query:
        embassies = embassies.filter(country__icontains=user.current_country)
    elif query:
        embassies = embassies.filter(
            Q(country__icontains=query) | Q(city__icontains=query) | Q(name__icontains=query)
        )

    # User's bookmarked embassy IDs
    bookmarked_ids = set(
        user.bookmarked_embassies.values_list('embassy_id', flat=True)
    )

    # Handle bookmark toggle
    if request.method == 'POST':
        embassy_id = request.POST.get('embassy_id')
        embassy = get_object_or_404(Embassy, pk=embassy_id)
        bookmark, created = EmbassyBookmark.objects.get_or_create(user=user, embassy=embassy)
        if not created:
            bookmark.delete()
        return redirect('main:embassy_contact_directory')

    # Detect nearest embassy
    current_country_embassy = Embassy.objects.filter(
        country__icontains=user.current_country
    ).first() if user.current_country else None

    # Get user's current location for map centering
    user_lat = user.latitude if user.latitude else 27.7172  # Default to Kathmandu
    user_lon = user.longitude if user.longitude else 85.3240

    # Prepare embassy markers for map (only current country)
    embassy_markers = []
    for embassy in embassies:
        if embassy.latitude and embassy.longitude:
            embassy_markers.append({
                'name': embassy.name,
                'lat': embassy.latitude,
                'lon': embassy.longitude,
                'city': embassy.city,
                'country': embassy.country,
                'phone': embassy.phone,
                'address': embassy.address,
            })

    # Get nearby communities for the map (current country only)
    communities = Community.objects.all()
    if user.current_country:
        communities = communities.filter(country__icontains=user.current_country)
    
    community_markers = []
    for community in communities[:20]:  # Limit to 20 for performance
        if community.latitude and community.longitude:
            community_markers.append({
                'name': community.name,
                'lat': community.latitude,
                'lon': community.longitude,
                'city': community.city,
                'phone': community.phone,
                'type': community.community_type,
            })

    # Police/helpline markers (placeholder - no Police model exists yet)
    police_markers = []

    context = {
        'embassies': embassies,
        'bookmarked_ids': bookmarked_ids,
        'current_country_embassy': current_country_embassy,
        'query': query,
        'user': user,
        'unread_count': _unread_count(user),
        'user_lat': user_lat,
        'user_lon': user_lon,
        'embassy_markers': json.dumps(embassy_markers),
        'community_markers': json.dumps(community_markers),
        'police_markers': json.dumps(police_markers),
        'communities': communities[:10],  # Pass first 10 for list display
    }
    return render(request, 'main/embassy_contact_directory.html', context)


# ─── Community Locator ────────────────────────

@login_required(login_url='main:login')
def community_locator(request):
    query = request.GET.get('q', '')
    communities = Community.objects.all()
    if query:
        communities = communities.filter(
            Q(name__icontains=query) | Q(city__icontains=query) | Q(country__icontains=query) | Q(address__icontains=query)
        )

    # Get user's current location for map centering
    user = request.user
    user_lat = user.latitude if user.latitude else 27.7172  # Default to Kathmandu
    user_lon = user.longitude if user.longitude else 85.3240

    # Prepare community markers data
    community_markers = []
    for community in communities:
        if community.latitude and community.longitude:
            community_markers.append({
                'name': community.name,
                'lat': community.latitude,
                'lon': community.longitude,
                'city': community.city,
                'phone': community.phone,
                'type': community.community_type,
            })

    context = {
        'communities': communities,
        'query': query,
        'unread_count': _unread_count(request.user),
        'user_lat': user_lat,
        'user_lon': user_lon,
        'community_markers': json.dumps(community_markers),
    }
    return render(request, 'main/community_locator.html', context)


# ─── Migration Checklist ─────────────────────

@login_required(login_url='main:login')
def migration_checklist_education(request):
    user = request.user
    REQUIRED_DOCUMENTS_COUNT = 10

    # Handle AJAX requests for checkbox updates
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        document_id = request.POST.get('document_id')
        is_checked = request.POST.get('is_checked') == 'true'
        
        # Store in session
        if 'completed_documents' not in request.session:
            request.session['completed_documents'] = {}
        
        request.session['completed_documents'][document_id] = is_checked
        request.session.modified = True
        
        completed_count = sum(1 for v in request.session.get('completed_documents', {}).values() if v)
        return JsonResponse({
            'completed_count': completed_count,
            'progress_pct': int((completed_count / REQUIRED_DOCUMENTS_COUNT) * 100)
        })

    # Regular page load
    completed_documents = request.session.get('completed_documents', {})
    completed_count = sum(1 for v in completed_documents.values() if v)
    progress_pct = int((completed_count / REQUIRED_DOCUMENTS_COUNT) * 100) if REQUIRED_DOCUMENTS_COUNT > 0 else 0

    context = {
        'completed_count': completed_count,
        'total_count': REQUIRED_DOCUMENTS_COUNT,
        'progress_pct': progress_pct,
        'completed_documents': completed_documents,
        'unread_count': _unread_count(user),
    }
    return render(request, 'main/migration_checklist_education.html', context)


# ─── Notifications ────────────────────────────

@login_required(login_url='main:login')
def safety_notifications(request):
    user = request.user
    category = request.GET.get('category', 'all')

    if request.method == 'POST':
        # Mark all read
        if 'mark_all_read' in request.GET or request.POST.get('mark_all_read'):
            user.notifications.filter(is_read=False).update(is_read=True)
            return redirect('main:safety_notifications')
        # Mark single notification read
        mark_read_id = request.POST.get('mark_read')
        if mark_read_id:
            user.notifications.filter(pk=mark_read_id).update(is_read=True)
            return redirect('main:safety_notifications')

    notifications = user.notifications.all()
    if category != 'all':
        notifications = notifications.filter(category=category)

    # Group by today and earlier
    today = timezone.now().date()
    today_notifications = notifications.filter(created_at__date=today)
    earlier_notifications = notifications.filter(created_at__date__lt=today)

    context = {
        'today_notifications': today_notifications,
        'earlier_notifications': earlier_notifications,
        'active_category': category,
        'unread_count': _unread_count(user),
    }
    return render(request, 'main/safety_notifications.html', context)

