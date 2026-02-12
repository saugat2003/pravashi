from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Onboarding
    path('onboarding/', views.onboarding_welcome, name='onboarding_welcome'),
    path('onboarding/features/', views.onboarding_key_features, name='onboarding_key_features'),
    path('onboarding/profile/', views.onboarding_profile_selection, name='onboarding_profile_selection'),

    # Home
    path('', views.home, name='home'),

    # Profile
    path('profile/', views.worker_profile_settings, name='worker_profile_settings'),

    # Documents
    path('document-vault/', views.secure_document_vault, name='secure_document_vault'),
    path('document/upload/', views.document_upload_ajax, name='document_upload_ajax'),
    path('document/<int:pk>/download/', views.document_download, name='document_download'),
    path('document/<int:pk>/delete/', views.document_delete, name='document_delete'),

    # Contract Analysis
    path('contract-analysis/', views.contract_analysis_upload, name='contract_analysis_upload'),
    path('contract-risk-report/', views.contract_risk_report, name='contract_risk_report'),
    path('contract-risk-report/<int:pk>/', views.contract_risk_report, name='contract_risk_report'),
    path('clause-analysis/', views.detailed_ai_clause_analysis, name='detailed_ai_clause_analysis'),
    path('clause-analysis/<int:pk>/', views.detailed_ai_clause_analysis, name='detailed_ai_clause_analysis'),

    # Safety
    path('daily-check-in/', views.daily_safety_check_in, name='daily_safety_check_in'),
    path('emergency-sos/', views.emergency_sos_activation, name='emergency_sos_activation'),
    path('sos-countdown/', views.sos_countdown_timer, name='sos_countdown_timer'),

    # Family
    path('family-dashboard/', views.family_safety_dashboard, name='family_safety_dashboard'),

    # Directory
    path('embassy-contacts/', views.embassy_contact_directory, name='embassy_contact_directory'),
    path('community-locator/', views.community_locator, name='community_locator'),

    # Checklist
    path('migration-checklist/', views.migration_checklist_education, name='migration_checklist_education'),

    # Notifications
    path('notifications/', views.safety_notifications, name='safety_notifications'),
]
