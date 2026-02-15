# Pravash: The Bridge for Migrants
**Empowering and protecting Nepali migrant workers with a comprehensive digital safety net.**

> **Status:** Hackathon Prototype (MVP)  
> **Team:** The Debuggers
> **Project Name:** Pravashi

---

## 📖 Table of Contents
1.  [Overview](#overview)
2.  [Team](#team)
3.  [Problem Statement](#problem-statement)
4.  [Solution & Key Features](#solution--key-features)
5.  [Architecture & Technology](#architecture--technology)
6.  [Installation & Setup](#installation--setup)
7.  [Usage Guide](#usage-guide)
8.  [Project Structure](#project-structure)
9.  [Future Roadmap](#future-roadmap)

---

## 🔎 Overview
**Pravash** is a mobile-first web application designed to act as a digital guardian for migrant workers. It addresses critical challenges such as contract exploitation, lack of emergency support, and family anxiety by providing a unified platform for **document security**, **risk analysis**, and **real-time safety monitoring**.

---

## 👥 Team: The Debuggers

| Name | Role | Handle |
| :--- | :--- | :--- |
| **Saugat Bhattarai** | Team Lead, Backend & Frontend | `@saugat2003` |
| **Nischal Dhakal** | Frontend, AI Integration | `@creator-nischal` |
| **Suprim Karki** | Documentation, UI/UX Design, Logo | `@suprim-karki` |
| **Himani Devkota** | Research, Presentation | `@himanidevkota39-del` |

---

## 🚩 Problem Statement
Thousands of Nepali workers migrate daily, facing:
*   **Contract Substitution:** Signing one contract at home but being forced into another abroad.
*   **Legal Opacity:** Inability to read legal documents in foreign languages.
*   **Emergency Vulnerability:** No easy way to alert family or embassies during distress.
*   **Document Theft:** Passports and visas are often confiscated by employers.

## 💡 Solution & Key Features

### 1. 🚨 One-Tap SOS Emergency System
*   **Instant Activation:** Sends an immediate distress signal with **GPS coordinates**, **battery level**, and **signal strength**.
*   **Multi-Channel Alert:** Notifies designated emergency contacts and family members instantly.
*   **Countdown Timer:** Prevents accidental triggers.

### 2. 🤖 AI Contract Analysis (BETA)
*   **Risk Scoring:** Upload a photo of any employment contract to get a risk score (0-100).
*   **Clause Detection:** Identifies predatory clauses (e.g., "Passport Retention", "Undefined Overtime").
*   **Native Translation:** Explains complex legal jargon in simple **Nepali**.

### 3. 🔐 Secure Document Vault
*   **Encrypted Storage:** Safely store digital copies of Passports, Visas, and Insurance policies.
*   **Verification Tracking:** Track which documents are verified and compliant.
*   **Owner-Only Access:** Strict permission controls ensure only the worker can manage their files.

### 4. 🏠 Family Safety Dashboard
*   **Peace of Mind:** Verified family members can view a "Safety Pulse" of the worker.
*   **Activity Feed:** See logs like "Arrived at Site", "Check-in Safe", or "Contract Uploaded".
*   **Privacy First:** Workers control location sharing preferences.

### 5. 📍 Embassy & Community Locator
*   **Geospatial Directory:** Interactive map showing the nearest **Nepali Embassies** and **Community Support Centers**.
*   **One-Touch Connect:** Call hotlines or get directions directly from the app.

---

## 🏗 Architecture & Technology

### Tech Stack
*   **Backend:** Python 3.10+, Django 6.0.2
*   **Frontend:** HTML5, Tailwind CSS (via CDN), Vanilla JavaScript
*   **Database:** SQLite (MVP)
*   **Mapping:** Leaflet.js / OpenStreetMap
*   **Styling:** Custom "Glassmorphism" UI with Plus Jakarta Sans typography.

### Application Flow
1.  **User Layer:** Two distinct profiles – `Worker` and `Family`.
2.  **Logic Layer:** Django Views process document uploads, calculate risk scores (simulated AI), and dispatch SOS alerts.
3.  **Data Layer:** SQLite stores relational data for Users, Documents, and Activity Logs.
4.  **Presentation:** Mobile-responsive templates utilizing a specialized "App Shell" layout.

---

## 🛠 Installation & Setup

### Prerequisites
*   Python 3.10 or higher
*   pip (Python package manager)

### Step-by-Step Guide

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/the_debuggers/pravash.git
    cd pravash
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Create Superuser (Optional)**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run Development Server**
    ```bash
    python manage.py runserver
    ```
    Access the app at `http://127.0.0.1:8000/`.

---

## 📱 Usage Guide

### For Workers
1.  **Register/Login:** Sign up as a "Worker".
2.  **Pre-Departure:** Complete the "Migration Checklist" in the app.
3.  **Upload Documents:** Go to `Profile > Document Vault` to secure your files.
4.  **Check Contract:** Navigate to "Contract Analysis", upload a generic contract image, and view the AI report.
5.  **Daily Check-in:** Tap the "I am Safe" button on the home screen daily.

### For Family
1.  **Register:** Sign up as "Family Member".
2.  **Link Account:** Ask the worker for their username to link profiles (via Admin/Database for MVP).
3.  **Monitor:** Access the "Family Dashboard" to see the worker's latest location and safety status.

---

## 📂 Project Structure

```text
pravash/
├── core/                   # Project configuration
│   ├── settings.py         # Django settings (Auth, Installed Apps)
│   └── urls.py             # Root URL routing
├── main/                   # Core Application Logic
│   ├── models.py           # Database Schemas (User, Document, SOS)
│   ├── views.py            # Business Logic & Controllers
│   ├── urls.py             # App-specific routes
│   └── management/         # Custom management commands
├── templates/              # HTML Templates
│   └── base.html           # Main app shell (Tailwind + Scripts)
├── static/                 # CSS, Images, JS assets
├── db.sqlite3              # Local Database
└── manage.py               # Django task runner
```

---

## 🚀 Future Roadmap
*   [ ] **Real-time AI:** Integrate OpenAI/Gemini API for live contract analysis.
*   [ ] **Offline Mode:** PWA capabilities for low-connectivity usage.
*   [ ] **Fintech Integration:** Remittance tracking and safe transfer guides.
*   [ ] **Legal Aid Marketplace:** Direct connection to pro-bono lawyers.

---

*Built with ❤️ by The Debuggers for Sankalpa Hackathon 2026.*
