from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('community-locator/', views.community_locator, name='community_locator'),
    path('contract-analysis/', views.contract_analysis_upload, name='contract_analysis_upload'),
    path('contract-risk-report/', views.contract_risk_report, name='contract_risk_report'),
    path('daily-check-in/', views.daily_safety_check_in, name='daily_safety_check_in'),
    path('clause-analysis/', views.detailed_ai_clause_analysis, name='detailed_ai_clause_analysis'),
    path('embassy-contacts/', views.embassy_contact_directory, name='embassy_contact_directory'),
    path('emergency-sos/', views.emergency_sos_activation, name='emergency_sos_activation'),
    path('family-dashboard/', views.family_safety_dashboard, name='family_safety_dashboard'),
    path('migration-checklist/', views.migration_checklist_education, name='migration_checklist_education'),
    path('onboarding/features/', views.onboarding_key_features, name='onboarding_key_features'),
    path('onboarding/profile/', views.onboarding_profile_selection, name='onboarding_profile_selection'),
    path('onboarding/', views.onboarding_welcome, name='onboarding_welcome'),
    path('notifications/', views.safety_notifications, name='safety_notifications'),
    path('document-vault/', views.secure_document_vault, name='secure_document_vault'),
    path('sos-countdown/', views.sos_countdown_timer, name='sos_countdown_timer'),
    path('profile/', views.worker_profile_settings, name='worker_profile_settings'),
]
