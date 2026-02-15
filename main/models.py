from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone


# ──────────────────────────────────────────────
# Custom User Model
# ──────────────────────────────────────────────

class User(AbstractUser):
    """Extended user supporting both migrant workers and family members."""

    class ProfileType(models.TextChoices):
        WORKER = 'worker', 'Worker'
        FAMILY = 'family', 'Family Member'

    class LanguageChoice(models.TextChoices):
        ENGLISH = 'en', 'English'
        NEPALI = 'ne', 'नेपाली'

    profile_type = models.CharField(
        max_length=10,
        choices=ProfileType.choices,
        default=ProfileType.WORKER,
    )
    phone = models.CharField(max_length=20, blank=True)
    worker_id = models.CharField(max_length=30, unique=True, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    # Current location
    current_city = models.CharField(max_length=100, blank=True)
    current_country = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # Status
    is_verified = models.BooleanField(default=False)
    is_active_worker = models.BooleanField(default=True)

    # Preferences
    language_preference = models.CharField(
        max_length=5,
        choices=LanguageChoice.choices,
        default=LanguageChoice.ENGLISH,
    )
    dark_mode = models.BooleanField(default=False)
    location_sharing = models.BooleanField(default=True)
    checkin_reminders = models.BooleanField(default=True)

    # Family linkage — a family member monitors a worker
    monitored_worker = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='family_members',
        limit_choices_to={'profile_type': 'worker'},
        help_text='The worker this family member is monitoring.',
    )

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_profile_type_display()})"


# ──────────────────────────────────────────────
# Emergency Contacts
# ──────────────────────────────────────────────

class EmergencyContact(models.Model):
    """Trusted contacts notified during SOS events."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='emergency_contacts',
    )
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    relationship = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.relationship})"


# ──────────────────────────────────────────────
# Secure Document Vault
# ──────────────────────────────────────────────

class Document(models.Model):
    """Identity and employment documents stored in the secure vault."""

    class DocType(models.TextChoices):
        PASSPORT = 'passport', 'Passport'
        WORK_VISA = 'work_visa', 'Work Visa'
        EMPLOYMENT_CONTRACT = 'employment_contract', 'Employment Contract'
        CITIZENSHIP = 'citizenship', 'Citizenship Certificate'
        INSURANCE = 'insurance', 'Insurance Policy'
        OTHER = 'other', 'Other'

    class VerificationStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        VERIFIED = 'verified', 'Verified'
        REJECTED = 'rejected', 'Rejected'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='documents',
    )
    doc_type = models.CharField(max_length=25, choices=DocType.choices)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verification_status = models.CharField(
        max_length=10,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.get_doc_type_display()} — {self.user.username}"


# ──────────────────────────────────────────────
# Contract Analysis
# ──────────────────────────────────────────────

class ContractAnalysis(models.Model):
    """AI-powered analysis of an uploaded employment contract."""

    class RiskLevel(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contract_analyses',
    )
    employer_name = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to='contracts/')
    analyzed_at = models.DateTimeField(auto_now_add=True)

    risk_score = models.PositiveSmallIntegerField(
        default=0,
        help_text='Overall risk score 0–100',
    )
    risk_level = models.CharField(
        max_length=10,
        choices=RiskLevel.choices,
        default=RiskLevel.LOW,
    )
    ai_recommendation = models.TextField(
        blank=True,
        help_text='AI-generated overall recommendation text',
    )
    ai_recommendation_ne = models.TextField(
        blank=True,
        help_text='Nepali translation of the recommendation',
    )

    class Meta:
        verbose_name_plural = 'Contract analyses'
        ordering = ['-analyzed_at']

    def __str__(self):
        return f"Analysis for {self.employer_name or 'Unknown'} — Risk {self.risk_score}/100"


class FlaggedClause(models.Model):
    """A specific clause flagged by the AI as risky."""

    class Severity(models.TextChoices):
        ILLEGAL = 'illegal', 'Illegal'
        HIGH_RISK = 'high_risk', 'High Risk'
        WARNING = 'warning', 'Warning'
        INFO = 'info', 'Info'

    analysis = models.ForeignKey(
        ContractAnalysis,
        on_delete=models.CASCADE,
        related_name='flagged_clauses',
    )
    clause_reference = models.CharField(
        max_length=50,
        help_text='e.g. "Clause 14.2"',
    )
    title = models.CharField(max_length=200)
    severity = models.CharField(max_length=15, choices=Severity.choices)
    original_text = models.TextField(help_text='Original clause text in English')
    explanation_ne = models.TextField(
        blank=True,
        help_text='Plain-language Nepali explanation',
    )
    recommendation = models.TextField(blank=True)

    class Meta:
        ordering = ['clause_reference']

    def __str__(self):
        return f"{self.clause_reference}: {self.title} ({self.get_severity_display()})"


# ──────────────────────────────────────────────
# Daily Safety Check-In
# ──────────────────────────────────────────────

class SafetyCheckIn(models.Model):
    """Daily check-in recorded by the worker."""

    class Status(models.TextChoices):
        SAFE = 'safe', 'Safe'
        NEED_HELP = 'need_help', 'Need Help'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='safety_checkins',
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.SAFE)
    checked_in_at = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['-checked_in_at']
        get_latest_by = 'checked_in_at'

    def __str__(self):
        return f"{self.user.username} — {self.get_status_display()} @ {self.checked_in_at:%Y-%m-%d %H:%M}"


# ──────────────────────────────────────────────
# Emergency SOS
# ──────────────────────────────────────────────

class SOSEvent(models.Model):
    """An emergency SOS activation by the worker."""

    class SOSStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACTIVE = 'active', 'Active'
        RESOLVED = 'resolved', 'Resolved'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sos_events',
    )
    activated_at = models.DateTimeField(default=timezone.now)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    signal_strength = models.CharField(max_length=20, blank=True)
    battery_level = models.PositiveSmallIntegerField(
        blank=True, null=True,
        help_text='Battery % at activation',
    )
    status = models.CharField(
        max_length=10,
        choices=SOSStatus.choices,
        default=SOSStatus.PENDING,
    )
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-activated_at']
        verbose_name = 'SOS Event'

    def __str__(self):
        return f"SOS by {self.user.username} @ {self.activated_at:%Y-%m-%d %H:%M} [{self.get_status_display()}]"


# ──────────────────────────────────────────────
# Embassy Directory
# ──────────────────────────────────────────────

class Embassy(models.Model):
    """Embassy or consulate contact information."""

    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    flag_emoji = models.CharField(max_length=10, blank=True)
    labor_attache_name = models.CharField(max_length=150, blank=True)
    labor_attache = models.CharField(max_length=150, blank=True, help_text='Alias for template')
    office_hours = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    emergency_hotline = models.CharField(max_length=30, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Embassies'
        ordering = ['country', 'city']

    def __str__(self):
        return f"{self.name} — {self.city}, {self.country}"


class EmbassyBookmark(models.Model):
    """User bookmark for a specific embassy."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarked_embassies',
    )
    embassy = models.ForeignKey(
        Embassy,
        on_delete=models.CASCADE,
        related_name='bookmarks',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'embassy')

    def __str__(self):
        return f"{self.user.username} ★ {self.embassy.name}"


# ──────────────────────────────────────────────
# Community Locator
# ──────────────────────────────────────────────

class Community(models.Model):
    """Community organisations/support centres near the worker."""

    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    community_type = models.CharField(max_length=50, blank=True, help_text='e.g. welfare, nrna, community, legal, religious, professional')
    address = models.TextField(blank=True)
    contact_person = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    operating_hours = models.CharField(max_length=200, blank=True)
    availability_hours = models.CharField(max_length=200, blank=True)
    response_time = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Communities'
        ordering = ['name']

    def __str__(self):
        return self.name


# ──────────────────────────────────────────────
# Migration Checklist
# ──────────────────────────────────────────────

class ChecklistItem(models.Model):
    """Pre-departure migration checklist item template."""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True, help_text='e.g. documents, health, training, legal, safety, finance')
    icon = models.CharField(max_length=50, default='description', help_text='Material Icons name')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class UserChecklistProgress(models.Model):
    """Tracks a worker's progress on a checklist item."""

    class ItemStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Completed'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='checklist_progress',
    )
    item = models.ForeignKey(
        ChecklistItem,
        on_delete=models.CASCADE,
        related_name='user_progress',
    )
    status = models.CharField(
        max_length=10,
        choices=ItemStatus.choices,
        default=ItemStatus.PENDING,
    )
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'item')
        ordering = ['item__order']

    def __str__(self):
        return f"{self.user.username} — {self.item.title}: {self.get_status_display()}"


# ──────────────────────────────────────────────
# Notifications
# ──────────────────────────────────────────────

class Notification(models.Model):
    """In-app notifications for the user."""

    class Category(models.TextChoices):
        SAFETY = 'safety', 'Safety Alert'
        REMINDER = 'reminder', 'Reminder'
        COMMUNITY = 'community', 'Community'
        CONTRACT = 'contract', 'Contract'
        DOCUMENT = 'document', 'Document'
        GENERAL = 'general', 'General'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    category = models.CharField(
        max_length=15,
        choices=Category.choices,
        default=Category.GENERAL,
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"


# ──────────────────────────────────────────────
# Activity Log (visible to family members)
# ──────────────────────────────────────────────

class ActivityLog(models.Model):
    """Timestamped activity entries visible on the family dashboard."""

    class EventType(models.TextChoices):
        CHECK_IN = 'check_in', 'Safety Check-In'
        ARRIVED = 'arrived', 'Arrived at Site'
        CONTRACT = 'contract', 'Contract Updated'
        DOCUMENT = 'document', 'Document Uploaded'
        SOS = 'sos', 'SOS Activated'
        OTHER = 'other', 'Other'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activity_logs',
    )
    event_type = models.CharField(max_length=15, choices=EventType.choices)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_event_type_display()} — {self.user.username} @ {self.timestamp:%H:%M}"
