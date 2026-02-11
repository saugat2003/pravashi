from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, EmergencyContact, Document, ContractAnalysis, FlaggedClause,
    SafetyCheckIn, SOSEvent, Embassy, EmbassyBookmark, Community,
    ChecklistItem, UserChecklistProgress, Notification, ActivityLog,
)


# ── Inlines ──────────────────────────────────

class EmergencyContactInline(admin.TabularInline):
    model = EmergencyContact
    extra = 0


class FlaggedClauseInline(admin.TabularInline):
    model = FlaggedClause
    extra = 0


class UserChecklistProgressInline(admin.TabularInline):
    model = UserChecklistProgress
    extra = 0


# ── Model Admins ─────────────────────────────

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'get_full_name', 'profile_type', 'current_country', 'is_verified', 'is_active_worker')
    list_filter = ('profile_type', 'is_verified', 'is_active_worker', 'current_country')
    search_fields = ('username', 'first_name', 'last_name', 'worker_id', 'phone')
    inlines = [EmergencyContactInline]
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {
            'fields': ('profile_type', 'phone', 'worker_id', 'photo'),
        }),
        ('Location', {
            'fields': ('current_city', 'current_country', 'latitude', 'longitude'),
        }),
        ('Status', {
            'fields': ('is_verified', 'is_active_worker'),
        }),
        ('Preferences', {
            'fields': ('language_preference', 'dark_mode', 'location_sharing', 'checkin_reminders'),
        }),
        ('Family Link', {
            'fields': ('monitored_worker',),
        }),
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'doc_type', 'verification_status', 'uploaded_at')
    list_filter = ('doc_type', 'verification_status')
    search_fields = ('user__username', 'user__first_name')


@admin.register(ContractAnalysis)
class ContractAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'employer_name', 'risk_score', 'risk_level', 'analyzed_at')
    list_filter = ('risk_level',)
    search_fields = ('user__username', 'employer_name')
    inlines = [FlaggedClauseInline]


@admin.register(SafetyCheckIn)
class SafetyCheckInAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'checked_in_at')
    list_filter = ('status',)
    search_fields = ('user__username',)


@admin.register(SOSEvent)
class SOSEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'activated_at', 'latitude', 'longitude')
    list_filter = ('status',)
    search_fields = ('user__username',)


@admin.register(Embassy)
class EmbassyAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'city', 'phone', 'emergency_hotline')
    list_filter = ('country',)
    search_fields = ('name', 'country', 'city')


@admin.register(EmbassyBookmark)
class EmbassyBookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'embassy', 'created_at')


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'availability_hours')
    search_fields = ('name', 'address', 'contact_person')


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    inlines = [UserChecklistProgressInline]


@admin.register(UserChecklistProgress)
class UserChecklistProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'status', 'completed_at')
    list_filter = ('status',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'title', 'is_read', 'created_at')
    list_filter = ('category', 'is_read')
    search_fields = ('title', 'description', 'user__username')


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'description', 'timestamp')
    list_filter = ('event_type',)
    search_fields = ('user__username', 'description')
