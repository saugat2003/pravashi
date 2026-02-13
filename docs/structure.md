# Pravash - Project Structure Documentation

> **Version:** 1.0.0  
> **Last Updated:** February 12, 2026  
> **Architecture:** Django Monolithic Web Application

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Directory Structure](#directory-structure)
3. [Application Architecture](#application-architecture)
4. [Core Modules](#core-modules)
5. [Data Models](#data-models)
6. [View Layer](#view-layer)
7. [Template System](#template-system)
8. [Static Assets](#static-assets)
9. [URL Routing](#url-routing)
10. [Database Schema](#database-schema)
11. [Development Workflow](#development-workflow)

---

## Project Overview

Pravash is built as a Django-based monolithic web application following the Model-View-Template (MVT) architectural pattern. The project emphasizes security, scalability, and maintainability through clear separation of concerns and modular design.

### Technical Stack
- **Framework:** Django 4.x
- **Language:** Python 3.9+
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Styling:** TailwindCSS 3.x
- **Mapping:** Leaflet.js 1.9.4

---

## Directory Structure

```
the_debuggers/
│
├── core/                           # Django project configuration
│   ├── __init__.py
│   ├── asgi.py                    # ASGI configuration for async support
│   ├── settings.py                # Global settings and configuration
│   ├── urls.py                    # Root URL configuration
│   ├── wsgi.py                    # WSGI configuration for deployment
│   └── __pycache__/
│
├── main/                          # Primary application module
│   ├── __init__.py
│   ├── admin.py                   # Django admin customizations
│   ├── apps.py                    # App configuration
│   ├── forms.py                   # Form definitions and validation
│   ├── models.py                  # Database models (478 lines)
│   ├── tests.py                   # Unit and integration tests
│   ├── urls.py                    # App-level URL routing
│   ├── views.py                   # View functions and business logic (772 lines)
│   ├── __pycache__/
│   │
│   ├── management/                # Custom Django management commands
│   │   ├── __init__.py
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── seed_data.py       # Database seeding script
│   │   │   └── __pycache__/
│   │   └── __pycache__/
│   │
│   └── migrations/                # Database migration files
│       ├── __init__.py
│       ├── 0001_initial.py        # Initial schema
│       ├── 0002_checklistitem_category_community_city_and_more.py
│       └── __pycache__/
│
├── templates/                     # Django template files
│   ├── base.html                  # Master template with navigation
│   └── main/                      # App-specific templates (19 files)
│       ├── community_locator.html
│       ├── contract_analysis_upload.html
│       ├── contract_risk_report.html
│       ├── daily_safety_check_in.html
│       ├── detailed_ai_clause_analysis.html
│       ├── embassy_contact_directory.html
│       ├── emergency_sos_activation.html
│       ├── family_safety_dashboard.html
│       ├── home.html
│       ├── login.html
│       ├── migration_checklist_education.html
│       ├── onboarding_key_features.html
│       ├── onboarding_profile_selection.html
│       ├── onboarding_welcome.html
│       ├── register.html
│       ├── safety_notifications.html
│       ├── secure_document_vault.html
│       ├── sos_countdown_timer.html
│       └── worker_profile_settings.html
│
├── static/                        # Static files (CSS, JS, Images)
│   ├── css/
│   │   └── style.css             # Custom CSS (TailwindCSS overrides)
│   ├── images/
│   │   └── logo.jpeg             # Application logo (favicon)
│   └── js/
│       └── main.js               # Global JavaScript utilities
│
├── media/                         # User-uploaded files
│   └── contracts/                 # Uploaded employment contracts
│
├── docs/                          # Project documentation
│   ├── features.md               # Feature documentation
│   └── structure.md              # This file - project structure
│
├── db.sqlite3                     # SQLite database (development)
├── manage.py                      # Django management script
├── README.md                      # Project README
└── LICENSE                        # Project license (MIT)
```

---

## Application Architecture

### MVT Pattern (Model-View-Template)

Pravash follows Django's MVT architectural pattern:

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────┐
│  URL Router │ (urls.py)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    View     │ (views.py)
│             │ - Business Logic
│             │ - Data Processing
│             │ - Authorization
└──────┬──────┘
       │
       ├──────────────┐
       ▼              ▼
┌─────────────┐  ┌─────────────┐
│    Model    │  │  Template   │
│  (models.py)│  │ (*.html)    │
│             │  │             │
│  Database   │  │  Rendering  │
└─────────────┘  └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │  HTTP       │
                 │  Response   │
                 └─────────────┘
```

### Request Flow

1. **URL Resolution:** `core/urls.py` → `main/urls.py`
2. **View Execution:** View function in `main/views.py`
3. **Data Retrieval:** Query models defined in `main/models.py`
4. **Authorization:** Check user permissions via decorators
5. **Template Rendering:** Render template from `templates/main/`
6. **Response:** Return HTML to browser

---

## Core Modules

### 1. Project Configuration (`core/`)

#### `settings.py` - Global Configuration
**Key Sections:**

```python
# Security Settings
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost'])

# Application Definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',  # Primary application
]

# Custom User Model
AUTH_USER_MODEL = 'main.User'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
```

#### `urls.py` - Root URL Configuration
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### `wsgi.py` & `asgi.py` - Server Interface
- **WSGI:** Synchronous server interface (Gunicorn, uWSGI)
- **ASGI:** Asynchronous server interface (Daphne, Uvicorn)

---

### 2. Main Application (`main/`)

#### `apps.py` - Application Configuration
```python
class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    verbose_name = 'Pravash Main App'
```

#### `admin.py` - Django Admin Customization
Registers models for admin interface with custom list displays, filters, and search capabilities.

**Example:**
```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'profile_type', 'current_country', 'is_verified']
    list_filter = ['profile_type', 'is_verified', 'current_country']
    search_fields = ['username', 'email', 'phone', 'worker_id']
```

---

## Data Models

### Model Architecture (`main/models.py`)

The application uses **11 core models** organized into logical domains:

#### 1. User Management

**User (Custom User Model - extends AbstractUser)**
```python
class User(AbstractUser):
    """Extended user supporting both migrant workers and family members."""
    
    # Profile
    profile_type = CharField(choices=ProfileType.choices)  # worker/family
    phone = CharField(max_length=20)
    worker_id = CharField(unique=True)
    photo = ImageField(upload_to='profile_photos/')
    
    # Location
    current_city = CharField(max_length=100)
    current_country = CharField(max_length=100)
    latitude = FloatField()
    longitude = FloatField()
    
    # Status
    is_verified = BooleanField(default=False)
    is_active_worker = BooleanField(default=True)
    
    # Preferences
    language_preference = CharField(choices=LanguageChoice.choices)
    dark_mode = BooleanField(default=False)
    location_sharing = BooleanField(default=True)
    checkin_reminders = BooleanField(default=True)
    
    # Family Linkage
    monitored_worker = ForeignKey('self', related_name='family_members')
```

**EmergencyContact**
```python
class EmergencyContact(models.Model):
    """Trusted contacts notified during SOS events."""
    user = ForeignKey(User)
    name = CharField(max_length=150)
    phone = CharField(max_length=20)
    relationship = CharField(max_length=50)
```

#### 2. Document Management

**Document**
```python
class Document(models.Model):
    """Identity and employment documents stored in secure vault."""
    user = ForeignKey(User)
    doc_type = CharField(choices=DocType.choices)  # passport/visa/contract/etc
    file = FileField(upload_to='documents/')
    uploaded_at = DateTimeField(auto_now_add=True)
    verification_status = CharField(choices=VerificationStatus.choices)
```

**ContractAnalysis**
```python
class ContractAnalysis(models.Model):
    """AI-powered analysis of employment contract."""
    user = ForeignKey(User)
    employer_name = CharField(max_length=200)
    file = FileField(upload_to='contracts/')
    analyzed_at = DateTimeField(auto_now_add=True)
    
    # Risk Assessment
    risk_score = PositiveSmallIntegerField()  # 0-100
    risk_level = CharField(choices=RiskLevel.choices)  # low/medium/high
    ai_recommendation = TextField()
    ai_recommendation_ne = TextField()  # Nepali translation
```

**FlaggedClause**
```python
class FlaggedClause(models.Model):
    """Specific clause flagged by AI as risky."""
    analysis = ForeignKey(ContractAnalysis)
    clause_reference = CharField(max_length=50)  # e.g., "Clause 14.2"
    title = CharField(max_length=200)
    severity = CharField(choices=Severity.choices)  # illegal/high_risk/warning/info
    original_text = TextField()
    explanation_ne = TextField()
    recommendation = TextField()
```

#### 3. Safety Features

**SafetyCheckIn**
```python
class SafetyCheckIn(models.Model):
    """Daily check-in recorded by worker."""
    user = ForeignKey(User)
    status = CharField(choices=Status.choices)  # safe/need_help
    checked_in_at = DateTimeField(default=timezone.now)
    note = TextField(blank=True)
```

**SOSEvent**
```python
class SOSEvent(models.Model):
    """Emergency SOS activation by worker."""
    user = ForeignKey(User)
    activated_at = DateTimeField(default=timezone.now)
    
    # Location Data
    latitude = FloatField()
    longitude = FloatField()
    
    # Device Metrics
    signal_strength = CharField(max_length=20)
    battery_level = PositiveSmallIntegerField()
    
    # Status Tracking
    status = CharField(choices=SOSStatus.choices)  # pending/active/resolved/cancelled
    resolved_at = DateTimeField(null=True)
```

#### 4. Support Infrastructure

**Embassy**
```python
class Embassy(models.Model):
    """Embassy or consulate contact information."""
    name = CharField(max_length=200)
    country = CharField(max_length=100)
    city = CharField(max_length=100)
    address = TextField()
    flag_emoji = CharField(max_length=10)
    
    # Contact Information
    labor_attache_name = CharField(max_length=150)
    phone = CharField(max_length=30)
    emergency_hotline = CharField(max_length=30)
    office_hours = CharField(max_length=200)
    
    # Location
    latitude = FloatField()
    longitude = FloatField()
```

**Community**
```python
class Community(models.Model):
    """Community organizations/support centers."""
    name = CharField(max_length=200)
    city = CharField(max_length=100)
    country = CharField(max_length=100)
    community_type = CharField(max_length=50)  # welfare/nrna/legal/religious/professional
    
    # Contact
    address = TextField()
    contact_person = CharField(max_length=150)
    phone = CharField(max_length=30)
    operating_hours = CharField(max_length=200)
    response_time = CharField(max_length=100)
    
    # Location
    latitude = FloatField()
    longitude = FloatField()
```

#### 5. Tracking & Notifications

**ChecklistItem & UserChecklistProgress**
```python
class ChecklistItem(models.Model):
    """Pre-departure migration checklist template."""
    title = CharField(max_length=200)
    description = TextField()
    category = CharField(max_length=50)  # documents/health/training/legal/safety/finance
    order = PositiveSmallIntegerField()

class UserChecklistProgress(models.Model):
    """User's progress on checklist item."""
    user = ForeignKey(User)
    item = ForeignKey(ChecklistItem)
    status = CharField(choices=ItemStatus.choices)  # pending/active/completed
    completed_at = DateTimeField(null=True)
```

**Notification**
```python
class Notification(models.Model):
    """In-app notifications."""
    user = ForeignKey(User)
    category = CharField(choices=Category.choices)  # safety/reminder/community/contract/document/general
    title = CharField(max_length=200)
    description = TextField()
    is_read = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
```

**ActivityLog**
```python
class ActivityLog(models.Model):
    """Timestamped activity entries visible to family."""
    user = ForeignKey(User)
    event_type = CharField(choices=EventType.choices)  # check_in/arrived/contract/document/sos/other
    description = TextField()
    timestamp = DateTimeField(default=timezone.now)
```

### Database Relationships

```
User (1) ─→ (N) EmergencyContact
User (1) ─→ (N) Document
User (1) ─→ (N) ContractAnalysis
User (1) ─→ (N) SafetyCheckIn
User (1) ─→ (N) SOSEvent
User (1) ─→ (N) Notification
User (1) ─→ (N) ActivityLog
User (1) ─→ (N) UserChecklistProgress

User (Worker) (1) ─→ (N) User (Family) [monitored_worker]

ContractAnalysis (1) ─→ (N) FlaggedClause

User (N) ─→ (N) Embassy [through EmbassyBookmark]

ChecklistItem (1) ─→ (N) UserChecklistProgress
```

---

## View Layer

### View Architecture (`main/views.py`)

The view layer handles **all business logic**, authentication, authorization, and data preparation for templates.

#### View Organization (772 lines)

**1. Helper Functions**
```python
def _unread_count(user):
    """Return count of unread notifications for nav badge."""

def _log_activity(user, event_type, description=''):
    """Create activity log entry visible to family."""
```

**2. Authentication Views**
```python
def login_view(request):
    """Handle user login with credentials."""

def register_view(request):
    """User registration with profile type selection."""

def logout_view(request):
    """Logout and redirect to onboarding."""
```

**3. Onboarding Flow**
```python
def onboarding_welcome(request):
    """Landing page with app introduction."""

def onboarding_key_features(request):
    """Feature overview carousel."""

def onboarding_profile_selection(request):
    """Worker vs Family profile selection."""
```

**4. Dashboard & Home**
```python
@login_required
def home(request):
    """Main dashboard showing safety status, notifications, quick actions."""
    
    # Context includes:
    # - last_checkin: Most recent SafetyCheckIn with full timestamp
    # - recent_notifications: Unread notifications
    # - active_sos: Any pending SOS events
    # - checklist_progress: Migration checklist completion %
```

**5. Safety Features**
```python
@login_required
def daily_safety_check_in(request):
    """Multiple daily check-ins with timestamp tracking."""
    # Removed single-check-in-per-day restriction
    # Always allows new check-in
    # Creates ActivityLog entry

@login_required
def emergency_sos_activation(request):
    """One-tap SOS with location and device metrics."""
    # Captures GPS coordinates
    # Records battery level, signal strength
    # Notifies emergency contacts and family
    # Creates ActivityLog entry

@login_required
def sos_countdown_timer(request, sos_id):
    """Countdown interface with cancel option."""
```

**6. Document Management**
```python
@login_required
def secure_document_vault(request):
    """Upload and manage identity/employment documents."""
    # Grouped by document type
    # Verification status tracking

@login_required
def contract_analysis_upload(request):
    """Upload contract for AI-powered risk analysis."""
    # Custom file upload UI
    # Employer name input
    # Recent analysis display

@login_required
def contract_risk_report(request, analysis_id):
    """Display comprehensive risk analysis report."""
    # Overall risk score and level
    # Flagged clauses with severity
    # AI recommendations in English and Nepali

@login_required
def detailed_ai_clause_analysis(request, clause_id):
    """Deep dive into specific flagged clause."""
```

**7. Support & Community**
```python
@login_required
def embassy_contact_directory(request):
    """Embassy for user's current country with interactive map."""
    # Filters embassies by user.current_country
    # Provides embassy_markers, community_markers, police_markers
    # Leaflet map integration

@login_required
def community_locator(request):
    """Find nearby community organizations."""
    # Interactive Leaflet map
    # Filter by community type
    # Distance calculation
```

**8. Migration Tools**
```python
@login_required
def migration_checklist_education(request):
    """Pre-departure checklist with progress tracking."""
    # Categorized checklist items
    # Mark items complete
    # Progress percentage
```

**9. Family Dashboard**
```python
@login_required
def family_safety_dashboard(request):
    """Family member view of worker safety."""
    # Requires profile_type='family'
    # Displays monitored_worker data
    # Real-time location map
    # Activity log with proper field names:
    #   - timestamp (not created_at)
    #   - event_type='check_in' (not 'checkin')
```

**10. Profile & Settings**
```python
@login_required
def worker_profile_settings(request):
    """Update profile information and preferences."""
    # Personal info, location
    # Language, dark mode
    # Location sharing toggle
    # Check-in reminder settings
```

**11. Notifications**
```python
@login_required
def safety_notifications(request):
    """Notification center with filtering."""
    # Categorized notifications
    # Mark as read functionality
    # Real-time count updates
```

### Authorization Decorators

**@login_required**
- Ensures user is authenticated
- Redirects to login if not authenticated

**Custom Decorators (Future Implementation):**
```python
def worker_required(view_func):
    """Restrict view to workers only."""
    
def family_required(view_func):
    """Restrict view to family members only."""
    
def verified_required(view_func):
    """Restrict view to verified users only."""
```

---

## Template System

### Base Template (`templates/base.html`)

**Structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>{% block title %}Pravash{% endblock %}</title>
    
    <!-- Favicon -->
    <link rel="icon" type="image/jpeg" href="{% static 'images/logo.jpeg' %}"/>
    
    <!-- TailwindCSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans" rel="stylesheet"/>
    
    <!-- Material Icons -->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet"/>
    
    <!-- Leaflet.js -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    
    <!-- Custom Config -->
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#7CB342',
                    }
                }
            }
        }
    </script>
    
    {% block extra_head %}{% endblock %}
</head>
<body>
    {% if user.is_authenticated %}
    <!-- Top Navigation Bar -->
    <nav>
        <div class="logo">Pravash</div>
        <div class="notifications">
            <span class="badge">{{ unread_count }}</span>
        </div>
    </nav>
    {% endif %}
    
    <!-- Main Content Area -->
    <main>
        {% block content %}{% endblock %}
    </main>
    
    {% if user.is_authenticated %}
    <!-- Bottom Navigation (Mobile) -->
    <nav class="bottom-nav">
        <a href="{% url 'main:home' %}">🏠 Home</a>
        <a href="{% url 'main:community_locator' %}">👥 Community</a>
        <a href="{% url 'main:emergency_sos_activation' %}">🚨 SOS</a>
        <a href="{% url 'main:embassy_contact_directory' %}">🏛️ Support</a>
        <a href="{% url 'main:worker_profile_settings' %}">👤 Profile</a>
    </nav>
    {% endif %}
    
    {% block extra_scripts %}{% endblock %}
</body>
</html>
```

### Template Inheritance Pattern

**Child Template Example:**
```django
{% extends 'base.html' %}
{% load static %}

{% block title %}Feature Name - Pravash{% endblock %}

{% block extra_head %}
    <!-- Page-specific CSS -->
{% endblock %}

{% block content %}
    <!-- Page content here -->
{% endblock %}

{% block extra_scripts %}
    <!-- Page-specific JavaScript -->
    <script>
        // Custom functionality
    </script>
{% endblock %}
```

### Template Features

**1. Leaflet Map Integration**
```javascript
// Common Leaflet pattern in all map pages
var map = L.map('map').setView([{{ lat }}, {{ lon }}], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Add markers
var marker = L.marker([{{ lat }}, {{ lon }}]).addTo(map);
marker.bindPopup("<b>Location Name</b><br>Details");
```

**2. Pulsing Location Marker (Family Dashboard)**
```css
@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.5); opacity: 0.5; }
    100% { transform: scale(1); opacity: 1; }
}

.pulsing-marker {
    animation: pulse 2s infinite;
}
```

**3. Custom File Upload (Contract Analysis)**
```javascript
const fileInput = document.getElementById('id_file');
const uploadArea = document.getElementById('upload-area');

// Drag and drop support
uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    fileInput.files = files;
    updateFilePreview(files[0]);
});

// Show file info
function updateFilePreview(file) {
    document.getElementById('file-name').textContent = file.name;
    document.getElementById('file-size').textContent = formatBytes(file.size);
}
```

---

## Static Assets

### CSS Architecture (`static/css/style.css`)

**Purpose:** Custom styles supplementing TailwindCSS

**Contents:**
- Component-specific overrides
- Animation keyframes
- Print styles
- Responsive utilities
- Dark mode variants (future)

### JavaScript (`static/js/main.js`)

**Global Utilities:**
```javascript
// CSRF Token for AJAX requests
function getCookie(name) {
    // Django CSRF token retrieval
}

// Notification handling
function showNotification(message, type) {
    // Toast notification display
}

// Location services
function getCurrentLocation(callback) {
    // HTML5 Geolocation API
}

// Real-time updates
function initializeWebSocket() {
    // WebSocket connection for live updates
}
```

### Images (`static/images/`)

**Assets:**
- `logo.jpeg` - Application logo (used as favicon)
- Icon set (future addition)
- Placeholder images
- Flag emojis (fallback)

---

## URL Routing

### URL Structure (`main/urls.py`)

```python
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Onboarding
    path('', views.onboarding_welcome, name='onboarding_welcome'),
    path('features/', views.onboarding_key_features, name='onboarding_key_features'),
    path('select-profile/', views.onboarding_profile_selection, name='onboarding_profile_selection'),
    
    # Dashboard
    path('home/', views.home, name='home'),
    
    # Safety
    path('check-in/', views.daily_safety_check_in, name='daily_safety_check_in'),
    path('sos/', views.emergency_sos_activation, name='emergency_sos_activation'),
    path('sos/<int:sos_id>/countdown/', views.sos_countdown_timer, name='sos_countdown_timer'),
    
    # Documents
    path('documents/', views.secure_document_vault, name='secure_document_vault'),
    path('contract/upload/', views.contract_analysis_upload, name='contract_analysis_upload'),
    path('contract/<int:analysis_id>/report/', views.contract_risk_report, name='contract_risk_report'),
    path('clause/<int:clause_id>/', views.detailed_ai_clause_analysis, name='detailed_ai_clause_analysis'),
    
    # Support
    path('embassy/', views.embassy_contact_directory, name='embassy_contact_directory'),
    path('community/', views.community_locator, name='community_locator'),
    
    # Migration Tools
    path('checklist/', views.migration_checklist_education, name='migration_checklist_education'),
    
    # Family
    path('family/dashboard/', views.family_safety_dashboard, name='family_safety_dashboard'),
    
    # Settings
    path('profile/', views.worker_profile_settings, name='worker_profile_settings'),
    path('notifications/', views.safety_notifications, name='safety_notifications'),
]
```

### URL Naming Convention

**Pattern:** `<feature>_<action>` or `<feature>_<view_type>`

**Examples:**
- `daily_safety_check_in` - Action-based
- `embassy_contact_directory` - View-type-based
- `contract_analysis_upload` - Feature + action

---

## Database Schema

### Migration Strategy

**Current Migrations:**
1. **0001_initial.py** - Initial schema creation
   - User model
   - Document, Contract models
   - Safety models

2. **0002_checklistitem_category_community_city_and_more.py** - Feature additions
   - Checklist system
   - Community locator
   - Enhanced embassy data

### Migration Commands

```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Reverse migration
python manage.py migrate main 0001_initial
```

### Database Seeding

**Location:** `main/management/commands/seed_data.py`

**Purpose:** Populate database with demo data for development

**Data Created:**
- Demo users (workers and family members)
- Embassy contacts for major countries
- Community organizations
- Checklist items
- Sample documents and contracts
- Safety check-ins

**Usage:**
```bash
python manage.py seed_data
```

---

## Development Workflow

### Local Development Setup

**1. Clone Repository**
```bash
git clone https://github.com/sankalpa-hackathon/the_debuggers.git
cd the_debuggers
```

**2. Create Virtual Environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Run Migrations**
```bash
python manage.py migrate
```

**5. Seed Database (Optional)**
```bash
python manage.py seed_data
```

**6. Create Superuser**
```bash
python manage.py createsuperuser
```

**7. Run Development Server**
```bash
python manage.py runserver
```

**8. Access Application**
- Application: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

### Git Workflow

**Branch Strategy:**
```
main
├── feature/check-in-improvements
├── feature/leaflet-maps-integration
├── feature/ui-enhancements
└── hotfix/critical-bug
```

**Commit Message Convention:**
```
<type>(<scope>): <subject>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Code formatting
- refactor: Code restructuring
- test: Test additions
- chore: Maintenance tasks

Example:
feat(safety): add multiple daily check-ins with timestamp tracking
```

### Code Quality Standards

**PEP 8 Compliance:**
```bash
# Check code style
flake8 .

# Auto-format code
black .
```

**Import Organization:**
```python
# 1. Standard library
import os
from datetime import datetime

# 2. Third-party packages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# 3. Local application
from .models import User, SafetyCheckIn
from .forms import SafetyCheckInForm
```

---

## Testing Strategy

### Test Organization

**Location:** `main/tests.py`

**Test Categories:**
1. **Model Tests** - Data integrity, validation
2. **View Tests** - HTTP responses, permissions
3. **Form Tests** - Validation logic
4. **Integration Tests** - End-to-end workflows

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test main

# Run with coverage report
coverage run --source='.' manage.py test
coverage report
```

---

## Deployment Architecture

### Production Checklist

**1. Environment Configuration**
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set `SECRET_KEY` from environment
- [ ] Configure production database (PostgreSQL)
- [ ] Set up media file storage (AWS S3)
- [ ] Configure email backend

**2. Security Hardening**
- [ ] Enable HTTPS
- [ ] Set secure cookie flags
- [ ] Configure CORS headers
- [ ] Set up Content Security Policy
- [ ] Enable SQL injection protection
- [ ] Configure rate limiting

**3. Static Files**
```bash
# Collect static files
python manage.py collectstatic --noinput
```

**4. Database**
```bash
# Run migrations
python manage.py migrate --noinput
```

**5. Server Configuration**
- **Web Server:** Nginx
- **Application Server:** Gunicorn
- **Process Manager:** Supervisor/Systemd
- **Database:** PostgreSQL 14+
- **Cache:** Redis

### Deployment Commands

```bash
# Install production dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Start Gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

---

## Performance Optimization

### Database Optimization

**1. Query Optimization**
```python
# Use select_related for foreign keys
SafetyCheckIn.objects.select_related('user').all()

# Use prefetch_related for reverse foreign keys
User.objects.prefetch_related('safety_checkins').all()

# Avoid N+1 queries
activities = ActivityLog.objects.select_related('user').filter(
    timestamp__gte=timezone.now() - timedelta(days=7)
)
```

**2. Indexing**
```python
class SafetyCheckIn(models.Model):
    # Add database indexes
    class Meta:
        indexes = [
            models.Index(fields=['user', '-checked_in_at']),
        ]
```

### Caching Strategy

**1. Template Fragment Caching**
```django
{% load cache %}
{% cache 500 embassy_list user.current_country %}
    <!-- Embassy list HTML -->
{% endcache %}
```

**2. View Caching**
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # 5 minutes
def community_locator(request):
    # View logic
```

---

## Maintenance & Monitoring

### Logging Configuration

```python
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

### Health Checks

**Endpoint:** `/health/`
```python
def health_check(request):
    """System health check for monitoring."""
    return JsonResponse({
        'status': 'healthy',
        'database': check_database(),
        'cache': check_cache(),
        'storage': check_storage(),
    })
```

---

## Future Enhancements

### Planned Structural Changes

1. **Modular App Architecture**
   - Split into: `users`, `safety`, `documents`, `support`
   - Improved separation of concerns
   - Better scalability

2. **API Layer**
   - Django REST Framework
   - GraphQL endpoint (Graphene)
   - Mobile app support

3. **Microservices (Long-term)**
   - AI Analysis Service
   - Notification Service
   - Location Service

4. **Enhanced Security**
   - Two-factor authentication
   - Biometric authentication
   - End-to-end encryption for documents

---

## Contributing Guidelines

### Code Contribution Process

1. **Fork Repository**
2. **Create Feature Branch**
3. **Implement Changes**
4. **Write Tests**
5. **Update Documentation**
6. **Submit Pull Request**

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] Browser compatibility checked

## Screenshots (if applicable)
```

---

## Support & Resources

**Documentation:** `/docs/`  
**GitHub Repository:** https://github.com/sankalpa-hackathon/the_debuggers  
**Issue Tracker:** https://github.com/sankalpa-hackathon/the_debuggers/issues

**Maintained by:** The Debuggers Team  
**Last Updated:** February 12, 2026  
**Version:** 1.0.0
