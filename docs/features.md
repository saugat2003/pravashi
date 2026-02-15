# Pravash - Feature Documentation

> **Version:** 1.0.0  
> **Last Updated:** February 12, 2026  
> **Maintainer:** The Debuggers Team

---

## Table of Contents

1. [Overview](#overview)
2. [Core Features](#core-features)
3. [User Management](#user-management)
4. [Safety & Emergency Features](#safety--emergency-features)
5. [Document Management](#document-management)
6. [Contract Analysis](#contract-analysis)
7. [Support & Community](#support--community)
8. [Migration Assistance](#migration-assistance)
9. [Family Dashboard](#family-dashboard)
10. [Notifications & Activity Tracking](#notifications--activity-tracking)

---

## Overview

Pravash is a comprehensive digital safety platform designed to protect and empower migrant workers throughout their employment journey. The application provides real-time safety monitoring, AI-powered contract analysis, secure document storage, and emergency response capabilities.

### Mission
To serve as a digital guardian for migrant workers by providing tools for safety, legal protection, and family connectivity.

### Target Users
- **Primary:** Migrant workers (Nepali workers abroad)
- **Secondary:** Family members monitoring worker safety
- **Supporting:** Embassies, community organizations, legal advocates

---

## Core Features

### 1. Authentication & Onboarding

#### 1.1 Multi-Step Onboarding Flow
**Purpose:** Introduce new users to the platform's capabilities and guide initial setup.

**Components:**
- **Welcome Screen** (`onboarding_welcome.html`)
  - Platform introduction
  - Value proposition
  - Get started CTA

- **Key Features Overview** (`onboarding_key_features.html`)
  - Feature highlights with icons
  - Interactive feature cards
  - Educational content

- **Profile Type Selection** (`onboarding_profile_selection.html`)
  - Worker profile setup
  - Family member profile setup
  - Profile-specific customization

**Technical Implementation:**
- Django template-based flow
- Session management for incomplete onboarding
- Progressive disclosure of features

#### 1.2 User Registration & Authentication
**Features:**
- Dual profile types: Worker and Family Member
- Email and phone verification support
- Secure password management
- Remember me functionality
- Password reset via email

**Data Model:**
```python
User Model Fields:
- profile_type: Worker/Family Member
- phone: Contact number
- worker_id: Unique identifier
- current_location: City, Country, GPS coordinates
- language_preference: English/Nepali
- monitored_worker: Foreign key for family linkage
```

**Security Measures:**
- Django's built-in password hashing (PBKDF2)
- CSRF protection
- Session-based authentication
- Login attempt throttling

---

## User Management

### 2. Worker Profile Management

#### 2.1 Profile Settings
**Location:** `worker_profile_settings.html`

**Editable Fields:**
- Personal information (Name, Phone, Email)
- Worker ID and verification status
- Current location (City, Country, GPS)
- Emergency contact details
- Profile photo upload

**Preferences:**
- Language selection (English/Nepali)
- Dark mode toggle
- Location sharing enabled/disabled
- Check-in reminder settings

#### 2.2 Family Member Linkage
**Purpose:** Enable family members to monitor worker safety

**Implementation:**
- Family member creates account with profile_type='family'
- Links to worker via `monitored_worker` foreign key
- Access to worker's safety status and location
- Receives notifications for SOS events

**Privacy Controls:**
- Worker must approve family member linkage
- Granular sharing permissions
- Location sharing can be toggled off
- Activity log visibility settings

---

## Safety & Emergency Features

### 3. Daily Safety Check-In

**Location:** `daily_safety_check_in.html`

#### 3.1 Check-In System
**Purpose:** Regular touchpoint to confirm worker safety

**Features:**
- **Multiple Daily Check-Ins:** Workers can check in multiple times per day
- **Timestamp Tracking:** Full datetime recording (not just date)
- **Status Selection:**
  - 🟢 Safe
  - 🔴 Need Help
- **Optional Notes:** Additional context for check-in
- **Automatic Activity Logging:** Visible to family members

**Technical Details:**
```python
Model: SafetyCheckIn
Fields:
- user: ForeignKey to User
- status: 'safe' or 'need_help'
- checked_in_at: DateTimeField with timezone
- note: Optional text field

Behavior:
- No daily limit (removed single-check-in restriction)
- Creates ActivityLog entry automatically
- Triggers family notification if status is 'need_help'
- Updates user's last_active timestamp
```

#### 3.2 Check-In Display (Home Dashboard)
**Location:** `home.html`

**Features:**
- Always-visible "Check In Now" button (bright green #10B981)
- Last check-in timestamp displayed
- Format: "Last: Feb 12, 2026 - 2:30 PM"
- Visual status indicator (Green dot for safe, Red for need help)
- Quick action card for immediate access

**UX Improvements:**
- Button never becomes disabled
- Clear timestamp instead of relative time
- Prominent placement on home dashboard
- One-tap access to check-in form

---

### 4. Emergency SOS System

**Location:** `emergency_sos_activation.html`

#### 4.1 SOS Activation
**Purpose:** Instant distress signal with location broadcasting

**Features:**
- **One-Tap Activation:** Large red SOS button
- **GPS Coordinates:** Automatic location capture
- **Device Metrics:**
  - Battery level percentage
  - Network signal strength
  - Device model and OS
- **Interactive Map:** Leaflet.js map showing exact location
- **Countdown Timer:** Visual confirmation of SOS status
- **Multi-Channel Alerts:**
  - Emergency contacts notified via SMS
  - Family members receive push notification
  - Embassy notified for high-risk situations

#### 4.2 SOS Event Tracking
**Data Model:**
```python
Model: SOSEvent
Fields:
- user: Worker who activated SOS
- activated_at: Timestamp
- latitude, longitude: GPS coordinates
- signal_strength: Network status
- battery_level: Device battery %
- status: pending/active/resolved/cancelled
- resolved_at: Resolution timestamp
```

**Status Flow:**
1. **Pending:** Initial activation, alerts being sent
2. **Active:** Confirmed emergency, response in progress
3. **Resolved:** Emergency addressed, worker safe
4. **Cancelled:** False alarm or situation resolved by worker

#### 4.3 Countdown Timer View
**Location:** `sos_countdown_timer.html`

**Features:**
- Visual countdown (5-minute window)
- Cancel option for false alarms
- Location display with accuracy radius
- Contact list showing notified parties
- Real-time status updates

**Safety Features:**
- Cannot accidently cancel (requires confirmation)
- Automatic escalation if not cancelled
- Persistent notification until resolved

---

## Document Management

### 5. Secure Document Vault

**Location:** `secure_document_vault.html`

#### 5.1 Document Upload System
**Purpose:** Secure storage of critical identity and employment documents

**Supported Document Types:**
- ✈️ Passport
- 🛂 Work Visa
- 📄 Employment Contract
- 🆔 Citizenship Certificate
- 🏥 Insurance Policy
- 📋 Other Documents

**Features:**
- **Drag-and-drop Upload:** Modern file upload interface
- **File Preview:** Thumbnail generation for images/PDFs
- **Verification Status Tracking:**
  - ⏳ Pending: Awaiting verification
  - ✅ Verified: Authenticated by admin
  - ❌ Rejected: Issues identified
- **Secure Storage:** Encrypted file storage in cloud
- **Access Control:** Only user and authorized personnel can view
- **Audit Trail:** Track who accessed documents when

**Technical Implementation:**
```python
Model: Document
Fields:
- user: Owner of document
- doc_type: Passport, Visa, Contract, etc.
- file: FileField (storage: media/documents/)
- uploaded_at: Timestamp
- verification_status: pending/verified/rejected

Security:
- Files stored outside web root
- Access requires authentication
- URL-based access tokens
- Automatic virus scanning
```

#### 5.2 Document Management Features
- **Categorized View:** Documents grouped by type
- **Quick Filters:** Filter by verification status, type, date
- **Expiry Tracking:** Automatic reminders for passport/visa expiry
- **Family Access:** Controlled access for linked family members
- **Download & Share:** Generate secure share links

---

## Contract Analysis

### 6. AI-Powered Contract Analysis

**Location:** `contract_analysis_upload.html`

#### 6.1 Contract Upload Interface
**Features:**
- **Custom File Input:** Redesigned upload UI with preview
- **File Information Display:**
  - Filename
  - File size
  - Document type indicator
- **Employer Information:** Input field for employer name
- **Recent Analysis History:** Cards showing past contract analyses
- **Upload Progress:** Real-time upload status

**UX Improvements:**
- Clean, modern card-based layout
- Gradient upload area
- Hover effects on interactive elements
- JavaScript-powered file preview
- Validation before submission

#### 6.2 Risk Analysis Engine
**Purpose:** AI-powered detection of exploitative contract clauses

**Analysis Components:**
1. **Overall Risk Score:** 0-100 numerical risk rating
2. **Risk Level Classification:**
   - 🟢 Low Risk (0-35)
   - 🟡 Medium Risk (36-70)
   - 🔴 High Risk (71-100)
3. **AI Recommendation:** Natural language summary
4. **Nepali Translation:** Recommendation in user's language

**Flagged Clause Detection:**
```python
Model: FlaggedClause
Severity Levels:
- illegal: Violates labor laws
- high_risk: Serious exploitation risk
- warning: Potentially unfavorable terms
- info: Notable clauses to understand

Fields:
- clause_reference: e.g., "Clause 14.2"
- title: Brief description
- original_text: English text of clause
- explanation_ne: Nepali plain-language explanation
- recommendation: Suggested action
```

#### 6.3 Risk Report View
**Location:** `contract_risk_report.html`

**Features:**
- **Summary Card:** Overall risk score and level
- **AI Recommendation:** Key takeaways in both languages
- **Flagged Clauses List:**
  - Severity-based color coding
  - Original clause text
  - Plain-language explanation
  - Recommended actions
- **Comparison Tool:** Compare multiple contracts
- **Export Options:** PDF report generation

#### 6.4 Detailed Clause Analysis
**Location:** `detailed_ai_clause_analysis.html`

**Features:**
- Deep dive into individual clauses
- Legal precedent references
- Alternative phrasing suggestions
- Negotiation tips
- Red flag indicators

**Educational Components:**
- Common exploitation patterns
- Rights awareness information
- Legal resource links
- Embassy contact for legal assistance

---

## Support & Community

### 7. Embassy Contact Directory

**Location:** `embassy_contact_directory.html`

#### 7.1 Embassy Information
**Purpose:** Quick access to Nepali embassy support in worker's current country

**Features:**
- **Single Embassy Display:** Shows embassy for user's current_country
- **Contact Details:**
  - Embassy name and flag
  - Full address
  - Phone numbers
  - Emergency hotline
  - Labor Attaché information
  - Office hours
- **Interactive Map:** Leaflet.js map with embassy location marker
- **One-Tap Calling:** Direct phone dialing
- **Bookmark System:** Save frequently needed embassies

#### 7.2 Multi-Layer Support Map
**Interactive Features:**
- **Embassy Markers:** 🏛️ Blue markers for embassy locations
- **Community Centers:** 🏘️ Green markers for support organizations
- **Police Stations:** 👮 Red markers for local law enforcement
- **Filter Toggles:**
  - Show/hide embassy layer
  - Show/hide community centers
  - Show/hide police stations
- **Marker Popups:** Click markers for detailed information
- **Distance Calculation:** Show distance from user's location
- **Directions:** Link to Google Maps for navigation

**Technical Implementation:**
```javascript
Map Layers:
- embassyMarkers: Array of embassy locations
- communityMarkers: Array of community centers
- policeMarkers: Array of police stations

Data Structure:
{
  name: "Embassy of Nepal",
  lat: 25.1234,
  lon: 55.5678,
  phone: "+971-xxx",
  address: "Full address"
}
```

#### 7.3 Embassy Bookmark Feature
**Purpose:** Save frequently contacted embassies for quick access

**Implementation:**
```python
Model: EmbassyBookmark
- user: Foreign key to User
- embassy: Foreign key to Embassy
- created_at: Bookmark timestamp

Features:
- One-click bookmark/unbookmark
- Bookmarked embassies highlighted
- "My Bookmarks" quick filter
```

---

### 8. Community Locator

**Location:** `community_locator.html`

#### 8.1 Community Organizations
**Purpose:** Find nearby support organizations and fellow migrants

**Organization Types:**
- **Welfare Organizations:** General support services
- **NRNA Chapters:** Non-Resident Nepali Association
- **Legal Aid Centers:** Free legal counsel
- **Religious Centers:** Cultural/spiritual support
- **Professional Networks:** Skill development and job assistance

#### 8.2 Interactive Community Map
**Features:**
- **Leaflet.js Integration:** Dynamic, interactive map
- **Community Markers:** Pins for each organization
- **Popup Information:**
  - Organization name
  - Contact person
  - Phone number
  - Operating hours
  - Response time
  - Address
- **User Location:** Blue pulsing marker for user
- **Distance Filter:** Show only communities within X km
- **Category Filter:** Filter by organization type

**Data Points:**
```python
Model: Community
- name: Organization name
- city, country: Location
- community_type: welfare/nrna/legal/religious/professional
- contact_person, phone: Contact details
- operating_hours, response_time: Availability
- latitude, longitude: GPS coordinates
```

#### 8.3 Community Features
- **Search by Location:** Find communities near specific address
- **Search by Service:** Filter by support type needed
- **Verified Badge:** Admin-verified organizations
- **User Reviews:** Ratings and feedback from other workers
- **Chat Feature:** Direct messaging with community leaders

---

## Migration Assistance

### 9. Migration Checklist & Education

**Location:** `migration_checklist_education.html`

#### 9.1 Pre-Departure Checklist
**Purpose:** Structured guide for migration preparation

**Checklist Categories:**
1. **📄 Documents:** 
   - Passport validity (6+ months)
   - Visa approval
   - Work permit
   - Medical certificates
   - Police clearance

2. **🏥 Health:**
   - Medical check-up
   - Required vaccinations
   - Health insurance
   - Prescription medications

3. **🎓 Training:**
   - Language basics
   - Cultural orientation
   - Job skills training
   - Rights awareness

4. **⚖️ Legal:**
   - Contract review
   - Embassy registration
   - Power of attorney
   - Will/nomination

5. **🔒 Safety:**
   - Emergency contacts
   - Insurance policies
   - Safe accommodation verified
   - Transportation arranged

6. **💰 Finance:**
   - Bank account setup
   - Foreign exchange
   - Remittance plan
   - Emergency funds

**Progress Tracking:**
```python
Model: UserChecklistProgress
- user: Worker
- item: ChecklistItem reference
- status: pending/active/completed
- completed_at: Completion timestamp

Features:
- Visual progress bar (% completed)
- Mark items as done
- Set reminders for pending items
- Attach documents as proof
- Share progress with family
```

#### 9.2 Educational Resources
**Content Types:**
- **Video Tutorials:** Step-by-step guides (Nepali subtitles)
- **Infographics:** Visual quick reference guides
- **FAQs:** Common questions answered
- **Success Stories:** Testimonials from workers
- **Rights Information:** Labor law summaries
- **Scam Alerts:** Common fraud patterns to avoid

---

## Family Dashboard

### 10. Family Safety Dashboard

**Location:** `family_safety_dashboard.html`

#### 10.1 Overview
**Purpose:** Allow family members to monitor worker safety and location

**Access Control:**
- Only users with profile_type='family'
- Must be linked to a worker via monitored_worker field
- Worker must approve family member access

#### 10.2 Dashboard Features

**Worker Status Card:**
- Current safety status (Safe/Need Help)
- Last check-in timestamp: "Last: Feb 12, 2026 - 2:30 PM"
- Location display (City, Country)
- Days since last check-in
- Contact worker button

**Interactive Location Map:**
- **Leaflet.js Map:** Real-time worker location
- **Pulsing Marker:** Animated marker showing worker position
- **Accuracy Circle:** GPS accuracy radius
- **Last Updated:** Timestamp of location update
- **Full-Screen Mode:** Expand map for detailed view

**Recent Activity Feed:**
- Dynamic activity log display
- **Event Types:**
  - ✅ Safety Check-In
  - 📍 Arrived at Site
  - 📄 Contract Updated
  - 📎 Document Uploaded
  - 🚨 SOS Activated
  - 📝 Other Events

**Activity Log Display:**
```django
{% for log in activity_logs %}
  <div class="activity-item">
    <span class="icon">{{ log.get_icon }}</span>
    <div class="details">
      <p class="event">{{ log.get_event_type_display }}</p>
      <p class="description">{{ log.description }}</p>
      <p class="time">{{ log.timestamp|date:"M d, Y - g:i A" }}</p>
    </div>
  </div>
{% endfor %}
```

**Technical Fix Applied:**
- Changed `log.created_at` → `log.timestamp` (correct field name)
- Changed event_type `'checkin'` → `'check_in'` (matches model choices)

#### 10.3 Communication Features
- **Direct Messaging:** Send messages to worker
- **Video Call:** Initiate video call (WebRTC)
- **Voice Message:** Record and send audio
- **Emergency Alert:** Alert worker to contact family

#### 10.4 Safety Settings
- **Check-In Reminders:** Configure reminder frequency
- **SOS Alert Settings:** Customize emergency notifications
- **Location Sharing:** Worker can toggle on/off
- **Activity Visibility:** Control what family can see

---

## Notifications & Activity Tracking

### 11. Notification System

**Location:** `safety_notifications.html`

#### 11.1 Notification Categories
**Types:**
- 🔴 **Safety Alerts:** SOS events, missed check-ins
- ⏰ **Reminders:** Check-in reminders, document expiry
- 👥 **Community:** New posts, events, announcements
- 📄 **Contract:** Analysis complete, flagged clauses
- 📎 **Document:** Verification status updates
- ℹ️ **General:** Platform updates, tips

#### 11.2 Notification Features
**Delivery Channels:**
- In-app notifications (notification center)
- Push notifications (mobile)
- Email notifications
- SMS for critical alerts (SOS)

**Management:**
- Mark as read/unread
- Delete notifications
- Filter by category
- Notification preferences
- Quiet hours setting
- Do not disturb mode

**Real-Time Updates:**
- WebSocket connection for instant delivery
- Badge count on navigation icon
- Desktop notifications (browser)
- Priority-based sorting

#### 11.3 Activity Log System
**Purpose:** Comprehensive audit trail of user actions

**Logged Activities:**
```python
Model: ActivityLog
Event Types:
- check_in: Safety Check-In
- arrived: Arrived at Site
- contract: Contract Updated
- document: Document Uploaded
- sos: SOS Activated
- other: Other Events

Visibility:
- Worker: See own activity
- Family: See linked worker's activity
- Admin: See all activities (moderation)
```

**Activity Features:**
- Filterable by date range
- Searchable by event type
- Exportable as PDF/CSV
- Timeline view
- Calendar view
- Statistics dashboard

---

## Technical Architecture

### 12. Technology Stack

**Backend:**
- Django 4.x (Python web framework)
- Django ORM (Database abstraction)
- Django Authentication (User management)
- Django Forms (Form handling and validation)

**Frontend:**
- HTML5 + CSS3
- TailwindCSS 3.x (Utility-first styling)
- JavaScript (ES6+)
- Leaflet.js 1.9.4 (Interactive mapping)

**Database:**
- SQLite (Development)
- PostgreSQL (Production-ready)

**Styling:**
- Custom Tailwind configuration
- Primary color: #7CB342 (Green)
- Font: Plus Jakarta Sans
- Material Icons (all variants)

**Mapping:**
- Leaflet.js for interactive maps
- OpenStreetMap tile layer
- Custom marker icons
- Popup information windows

---

### 13. Feature Development Status

#### ✅ Completed Features
- [x] User authentication and authorization
- [x] Dual profile types (Worker/Family)
- [x] Multiple daily check-ins with timestamps
- [x] Dynamic activity feed
- [x] Interactive Leaflet maps (5+ pages)
- [x] Embassy directory with location filter
- [x] Community locator with interactive map
- [x] Contract upload with custom UI
- [x] Secure document vault
- [x] SOS emergency system with location
- [x] Family safety dashboard with real-time map
- [x] Notification system
- [x] Migration checklist tracker
- [x] Profile settings and preferences

#### 🚧 In Progress
- [ ] AI contract analysis integration (backend processing)
- [ ] Video call functionality (WebRTC)
- [ ] Multi-language support (Nepali translation)
- [ ] Push notification implementation
- [ ] Email verification system

#### 📋 Planned Features
- [ ] Mobile app (React Native)
- [ ] Offline mode with sync
- [ ] Advanced analytics dashboard
- [ ] Community forum
- [ ] Job board integration
- [ ] Training module with certificates
- [ ] Remittance tracking
- [ ] Legal consultation booking
- [ ] Travel insurance integration
- [ ] Flight tracking integration

---

## Deployment & Configuration

### 14. Environment Setup

**Required Environment Variables:**
```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

DATABASE_URL=postgresql://user:pass@host:5432/dbname
MEDIA_ROOT=/path/to/media
STATIC_ROOT=/path/to/static

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AI Service (Future)
OPENAI_API_KEY=your-openai-key
```

### 15. Security Considerations

**Data Protection:**
- All passwords hashed using PBKDF2
- HTTPS enforced in production
- CSRF tokens on all forms
- SQL injection protection via ORM
- XSS protection via template escaping

**Privacy Features:**
- User controls data sharing
- Location sharing can be disabled
- Activity log visibility settings
- Data export capability
- Account deletion with data wipe

**Compliance:**
- GDPR compliant
- Data retention policies
- Audit trail for all data access
- Secure file storage
- Regular security audits

---

## Support & Maintenance

**For feature requests or bug reports:**
- GitHub Issues: https://github.com/sankalpa-hackathon/the_debuggers/issues
- Email: support@pravash.com

**Documentation maintained by:** The Debuggers Team  
**Last comprehensive review:** February 12, 2026
