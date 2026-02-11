from django.shortcuts import render


def home(request):
    return render(request, 'main/home.html')

def community_locator(request):
    return render(request, 'main/community_locator.html')

def contract_analysis_upload(request):
    return render(request, 'main/contract_analysis_upload.html')

def contract_risk_report(request):
    return render(request, 'main/contract_risk_report.html')

def daily_safety_check_in(request):
    return render(request, 'main/daily_safety_check_in.html')

def detailed_ai_clause_analysis(request):
    return render(request, 'main/detailed_ai_clause_analysis.html')

def embassy_contact_directory(request):
    return render(request, 'main/embassy_contact_directory.html')

def emergency_sos_activation(request):
    return render(request, 'main/emergency_sos_activation.html')

def family_safety_dashboard(request):
    return render(request, 'main/family_safety_dashboard.html')

def migration_checklist_education(request):
    return render(request, 'main/migration_checklist_education.html')

def onboarding_key_features(request):
    return render(request, 'main/onboarding_key_features.html')

def onboarding_profile_selection(request):
    return render(request, 'main/onboarding_profile_selection.html')

def onboarding_welcome(request):
    return render(request, 'main/onboarding_welcome.html')

def safety_notifications(request):
    return render(request, 'main/safety_notifications.html')

def secure_document_vault(request):
    return render(request, 'main/secure_document_vault.html')

def sos_countdown_timer(request):
    return render(request, 'main/sos_countdown_timer.html')

def worker_profile_settings(request):
    return render(request, 'main/worker_profile_settings.html')
