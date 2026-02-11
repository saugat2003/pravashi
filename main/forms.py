from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User, EmergencyContact, Document, ContractAnalysis,
    SafetyCheckIn, SOSEvent, Community, Notification,
)


# ── Authentication ───────────────────────────

class RegisterForm(UserCreationForm):
    """Registration form for new users."""

    profile_type = forms.ChoiceField(
        choices=User.ProfileType.choices,
        widget=forms.RadioSelect,
        initial='worker',
    )
    language_preference = forms.ChoiceField(
        choices=User.LanguageChoice.choices,
        initial='en',
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'phone', 'profile_type', 'language_preference',
            'password1', 'password2',
        ]


class ProfileUpdateForm(forms.ModelForm):
    """Update worker profile settings."""

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'photo',
            'current_city', 'current_country',
            'language_preference', 'dark_mode',
            'location_sharing', 'checkin_reminders',
        ]


# ── Emergency Contacts ──────────────────────

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'phone', 'relationship']


# ── Document Vault ───────────────────────────

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['doc_type', 'file']


# ── Contract Analysis ────────────────────────

class ContractUploadForm(forms.ModelForm):
    class Meta:
        model = ContractAnalysis
        fields = ['employer_name', 'file']


# ── Safety Check-In ──────────────────────────

class SafetyCheckInForm(forms.Form):
    status = forms.ChoiceField(choices=SafetyCheckIn.Status.choices)


# ── SOS Event ────────────────────────────────

class SOSEventForm(forms.Form):
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)
    signal_strength = forms.CharField(max_length=20, required=False)
    battery_level = forms.IntegerField(required=False)
