# Daily Health Partner

> An all-in-one daily health tracking application with an AI-powered health assistant.

Daily Health Partner is a full-stack health tracking and awareness application designed to bring a user's daily health information into one place.

Instead of tracking water, sleep, activity, mood, meals, medications, and appointments across different applications, the system provides a unified dashboard where users can log their data, view trends, receive reminders, and get AI-generated insights based on their own health records.

---

## Problem Statement

Health information is often fragmented across multiple applications.

For example:

- Water intake may be tracked in one application.
- Steps and exercise may be tracked somewhere else.
- Sleep may have its own tracker.
- Mood may be recorded in a journal.
- Medication reminders may exist in another application.
- Doctor appointments may be stored in a calendar.
- Meals may be tracked using a nutrition application.

This fragmentation makes it difficult to understand the overall picture of a person's daily health.

Most health trackers primarily collect data. They do not necessarily help the user understand relationships between different parts of their routine.

For example:

> "I have been feeling tired lately. Is there anything in my recent health data that could explain this?"

Daily Health Partner aims to solve this by combining health tracking, reminders, visualization, and AI-assisted interpretation into a single application.

---

## Solution

Daily Health Partner provides a centralized platform where users can:

- Track daily health metrics.
- Record meals using natural language.
- Track mood and journal entries.
- Record symptoms.
- Manage medication schedules.
- Manage doctor appointments.
- View health trends.
- Ask an AI assistant questions using their own logged data as context.
- Receive automated daily health summaries.
- Store emergency information.

The application focuses on **health awareness and lifestyle tracking**, not medical diagnosis.

---

# Features

## 1. Health & Activity Tracking

Users can record:

- Water intake
- Sleep duration
- Steps
- Exercise/activity
- Weight

This information forms the core data layer of the application.

---

## 2. Meal Logging

Users can enter meals using normal language instead of selecting items from a rigid food database.

Example:

```text
2 rotis, dal and a bowl of curd
```

The AI layer can estimate:

- Calories
- Protein
- Carbohydrates
- Fat

Nutrition values are estimates and should not be treated as medically or scientifically exact measurements.

---

## 3. Mood Tracking

Users can record a daily mood score from 1–5.

Example:

```text
Mood: 2/5

Journal:
"Felt tired throughout the day and couldn't concentrate."
```

Mood history can later be compared with other health metrics such as sleep and activity.

---

## 4. Symptom Tracker

Users can record symptoms along with:

- Date
- Severity
- Optional notes

Example:

```text
Symptom: Headache
Severity: 3/5
Date: 25 September
```

This creates a historical health journal that can help users observe patterns over time.

---

## 5. Medication Reminders

Users can create medication schedules.

Example:

```text
Medicine: Example Medicine
Time: 09:00 AM
Frequency: Daily
```

The system is planned to provide reminders for scheduled medications.

---

## 6. Doctor Appointment Reminders

Users can store upcoming appointments.

Example:

```text
Doctor Appointment

Date: 10 October
Time: 04:30 PM
```

Appointments can later be connected to the notification system.

---

## 7. AI Health Assistant

One of the major features of the application is an AI health assistant.

Users can ask questions such as:

```text
Why have I been feeling tired lately?
```

Instead of providing a completely generic response, the system retrieves relevant recent health data from the user's records.

Example:

```text
Recent Health Data

Sleep:
5.5 hours
6 hours
5 hours

Water:
1.2 L
1.5 L
1.1 L

Mood:
2
2
3
```

This information is supplied to the AI as context.

### AI Flow

```text
User Question
      |
      v
Retrieve Relevant Health Data
      |
      v
Build Context
      |
      v
Send Context + Question to LLM
      |
      v
Generate Grounded Response
```

This is the RAG-style component of the application.

---

## 8. Smart Daily Summary

The system can generate a natural-language summary of the user's day.

Example:

```text
Today's Summary

You slept less than your recent average and
logged lower water intake today.

Your mood was also lower than your recent entries.

Consider prioritizing adequate sleep and hydration
tomorrow.
```

The purpose is to convert raw health records into information that is easier to understand.

---

## 9. Reminders & Nudges

The application can eventually provide reminders such as:

```text
You haven't logged water in 6 hours.
```

or:

```text
Medication Reminder

Time to take your scheduled medication.
```

---

## 10. Trend Dashboard

The dashboard will visualize historical health information.

Planned metrics include:

- Sleep
- Water
- Steps
- Weight
- Mood

Planned views:

- Last 7 days
- Weekly trends
- Monthly trends

Future comparisons may include:

```text
Sleep vs Mood
Water vs Mood
Sleep vs Activity
```

---

## 11. Emergency Information

Users can store important emergency information such as:

```text
Blood Group
Allergies
Emergency Contact
```

The information can be displayed through a quick-access emergency card.

---

## 12. Doctor / Family Sharing

This is a later-stage feature.

Potential functionality:

- Generate health reports.
- Export health information as PDF.
- Share read-only information.
- Provide controlled access to doctors or family members.

This is intentionally not part of the initial MVP because multi-user permissions and access control introduce additional complexity.

---

# Technology Stack

## Backend

- Python
- FastAPI
- SQLAlchemy

## Database

- PostgreSQL

## Frontend

- React
- JavaScript
- HTML
- CSS

## AI

- LLM API
- Context-based health data retrieval
- Prompt-based safety constraints

---

# Architecture

```text
                    DAILY HEALTH PARTNER
                            |
                            v
                  +--------------------+
                  |   React Frontend   |
                  |--------------------|
                  | Login              |
                  | Dashboard          |
                  | Health Tracking    |
                  | Mood               |
                  | Meals              |
                  | AI Assistant       |
                  | Medications        |
                  | Appointments       |
                  | Symptoms           |
                  +---------+----------+
                            |
                         REST API
                            |
                            v
                  +--------------------+
                  | Python / FastAPI   |
                  |--------------------|
                  | Authentication     |
                  | Health             |
                  | Mood               |
                  | Dashboard          |
                  | AI                 |
                  | Medications        |
                  | Appointments       |
                  | Symptoms           |
                  +---------+----------+
                            |
                       SQLAlchemy
                            |
                            v
                  +--------------------+
                  |    PostgreSQL      |
                  |--------------------|
                  | Users              |
                  | Health Logs        |
                  | Mood Entries       |
                  | Meals              |
                  | Medications        |
                  | Appointments       |
                  | Symptoms           |
                  | Chat History       |
                  +--------------------+
```

---

# Project Structure

```text
daily-health-partner/
│
├── backend/
│   │
│   ├── .env
│   ├── requirements.txt
│   │
│   └── app/
│       │
│       ├── main.py
│       │
│       ├── ai/
│       │   ├── prompts.py
│       │   ├── routes.py
│       │   └── service.py
│       │
│       ├── appointments/
│       │   ├── routes.py
│       │   └── schemas.py
│       │
│       ├── auth/
│       │   ├── routes.py
│       │   ├── schemas.py
│       │   └── service.py
│       │
│       ├── dashboard/
│       │   ├── routes.py
│       │   └── service.py
│       │
│       ├── database/
│       │   ├── connection.py
│       │   └── models.py
│       │
│       ├── health/
│       │   ├── routes.py
│       │   ├── schemas.py
│       │   └── service.py
│       │
│       ├── medications/
│       │   ├── routes.py
│       │   └── schemas.py
│       │
│       ├── mood/
│       │   ├── routes.py
│       │   └── schemas.py
│       │
│       └── symptoms/
│           ├── routes.py
│           └── schemas.py
│
└── frontend/
    │
    └── src/
        │
        ├── App.jsx
        ├── main.jsx
        │
        ├── components/
        │   ├── Chart.jsx
        │   ├── EmergencyCard.jsx
        │   ├── HealthCard.jsx
        │   ├── HealthInput.jsx
        │   ├── MoodCard.jsx
        │   ├── Navbar.jsx
        │   └── ReminderCard.jsx
        │
        ├── hooks/
        │
        ├── pages/
        │   ├── Appointments.jsx
        │   ├── Assistant.jsx
        │   ├── Dashboard.jsx
        │   ├── Health.jsx
        │   ├── Login.jsx
        │   ├── Meals.jsx
        │   ├── Medications.jsx
        │   ├── Mood.jsx
        │   ├── Profile.jsx
        │   ├── Register.jsx
        │   └── Symptoms.jsx
        │
        └── services/
            ├── ai.js
            ├── api.js
            ├── auth.js
            └── health.js
```

---

# Backend Module Responsibilities

## `main.py`

Application entry point.

Responsible for:

- Creating the FastAPI application.
- Registering routers.
- Starting the API.

## `database/`

Database layer.

`connection.py` handles the PostgreSQL connection, SQLAlchemy engine, and database sessions.

`models.py` will contain:

- User model
- Health data models
- Mood model
- Meal model
- Medication model
- Appointment model
- Symptom model
- Chat history

## `auth/`

Authentication functionality:

- User registration
- Login
- Password handling
- Authentication
- User identity

## `health/`

Core health tracking:

- Water
- Sleep
- Steps
- Exercise
- Weight

## `mood/`

Responsible for:

- Mood score
- Journal entry
- Mood history

## `ai/`

Responsible for:

- AI health assistant
- Meal estimation
- Daily summaries
- Prompt handling
- Health-data context generation

## `dashboard/`

Responsible for:

- Today's overview
- Historical data
- Aggregated metrics
- Dashboard statistics

## `medications/`

Responsible for:

- Medication records
- Medication schedules
- Reminder information

## `appointments/`

Responsible for:

- Doctor appointments
- Appointment dates
- Appointment times
- Reminder information

## `symptoms/`

Responsible for:

- Symptom records
- Severity
- Dates
- Notes

---

# Frontend Structure

## `pages/`

Application screens:

```text
Login
Register
Dashboard
Health
Meals
Mood
Symptoms
Medications
Appointments
Assistant
Profile
```

## `components/`

Reusable UI components:

```text
HealthCard
MoodCard
Chart
ReminderCard
EmergencyCard
Navbar
HealthInput
```

## `services/`

Frontend API communication:

```text
api.js
auth.js
health.js
ai.js
```

These modules will communicate with the FastAPI backend.

---

# Database Concept

The initial database will revolve around the user and their health records.

```text
User
 |
 +---- Health Logs
 |
 +---- Mood Entries
 |
 +---- Meal Logs
 |
 +---- Medications
 |
 +---- Appointments
 |
 +---- Symptoms
 |
 +---- Chat History
```

Each user's health information should remain associated with that user.

This becomes especially important when authentication and multi-user support are implemented.

---

# Development Roadmap

The application will be built incrementally rather than trying to implement everything simultaneously.

## Phase 0 — Setup

- [x] Define project idea
- [x] Define feature set
- [x] Choose technology stack
- [x] Create project structure
- [x] Create backend skeleton
- [x] Create frontend skeleton
- [x] Create Python virtual environment
- [x] Install backend dependencies
- [x] Install PostgreSQL
- [ ] Complete PostgreSQL server/service setup
- [ ] Connect FastAPI to PostgreSQL
- [ ] Verify backend startup

## Phase 1 — Core MVP

### Authentication

- [ ] Register
- [ ] Login
- [ ] User authentication

### Health Tracking

- [ ] Water
- [ ] Sleep
- [ ] Steps
- [ ] Weight

### Mood

- [ ] Mood score
- [ ] Journal entry

### Dashboard

- [ ] Today's health overview
- [ ] Recent entries
- [ ] Basic charts
- [ ] 7-day history

The goal of this phase is to have a genuinely working full-stack application.

---

# Phase 2 — AI Layer

## Meal AI

- [ ] Free-text meal input
- [ ] LLM calorie estimation
- [ ] Macro estimation
- [ ] Store estimated results

## AI Health Assistant

- [ ] User question
- [ ] Retrieve recent health data
- [ ] Build context
- [ ] Send context to LLM
- [ ] Generate grounded response
- [ ] Store chat history

## Smart Summary

- [ ] Generate daily summary
- [ ] Compare current data with recent history
- [ ] Present lifestyle observations

## AI Safety

- [ ] Avoid medical diagnosis
- [ ] Clearly communicate limitations
- [ ] Keep responses grounded in available user data

---

# Phase 3 — Advanced Features

- [ ] Medication reminders
- [ ] Appointment reminders
- [ ] Symptom tracker
- [ ] Emergency information
- [ ] Weekly trends
- [ ] Monthly trends
- [ ] Sleep vs mood analysis
- [ ] Water vs mood analysis
- [ ] Improved dashboard

---

# Phase 4 — Polish & Portfolio

- [ ] PDF health report
- [ ] Doctor/family sharing
- [ ] Improved UI
- [ ] Better error handling
- [ ] Authentication/security improvements
- [ ] API documentation
- [ ] Deployment
- [ ] Demo video
- [ ] Portfolio presentation

---

# Current Backend Setup

The backend uses a Python virtual environment:

```text
backend/
└── .venv/
```

Current backend dependencies include:

```text
FastAPI
Uvicorn
SQLAlchemy
psycopg2-binary
Pydantic
python-dotenv
```

---

# Environment Variables

The backend will use a `.env` file for configuration.

Example:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/daily_health_partner
```

Do not commit the `.env` file containing real credentials to GitHub.

Recommended `.gitignore` entries:

```text
.env
.venv/
__pycache__/
*.pyc
```

---

# Current PostgreSQL Setup Issue

PostgreSQL 18 has been installed on the development machine.

Installation path:

```text
C:\Program Files\PostgreSQL8
```

The installation contains:

```text
bin/
data/
lib/
pgAdmin 4/
```

However, the PostgreSQL Windows service is currently not appearing in Windows Services.

The following command returned no PostgreSQL service:

```powershell
Get-Service *postgres*
```

The PostgreSQL control utility was also blocked by the Windows Application Control policy:

```text
Application Control policy has blocked this file
```

Because of this, the PostgreSQL server is currently not accepting connections on:

```text
localhost:5432
```

The immediate setup task is:

```text
PostgreSQL Installation
        |
        v
Register PostgreSQL Server
        |
        v
Start PostgreSQL Service
        |
        v
Verify localhost:5432
        |
        v
Create daily_health_partner database
        |
        v
Connect FastAPI
```

This is a development environment/setup issue and does not change the application architecture.

---

# Planned API Structure

The backend will eventually expose endpoints similar to:

```text
/api/auth
/api/health
/api/mood
/api/meals
/api/medications
/api/appointments
/api/symptoms
/api/dashboard
/api/ai
```

Example endpoints:

```text
POST /api/auth/register
POST /api/auth/login

POST /api/health
GET  /api/health

POST /api/mood
GET  /api/mood

POST /api/meals

POST /api/medications
GET  /api/medications

POST /api/appointments
GET  /api/appointments

POST /api/symptoms
GET  /api/symptoms

GET  /api/dashboard

POST /api/ai/chat
POST /api/ai/meal-estimate
```

These endpoints will be implemented progressively rather than all at once.

---

# Security & Privacy

Health information is sensitive.

The project should eventually implement:

- Password hashing
- Authentication
- Authorization
- User-specific data access
- Environment variables for secrets
- Database access controls
- Secure API configuration
- HTTPS in deployment
- Appropriate privacy documentation

For the initial portfolio version, the project should be treated as a demo/portfolio application rather than a production medical system.

---

# Limitations

### Not a medical device

The application does not diagnose medical conditions.

### AI limitations

AI responses depend on the information the user logs.

Missing or incorrect data can produce weak or misleading observations.

### Nutrition estimation

Meal calorie and macro values generated from natural-language descriptions are approximate.

### No wearable integration initially

The initial version relies on manual data entry.

### Health data privacy

Real health information should not be treated casually. Production deployment would require stronger security, privacy controls, and appropriate compliance considerations.

### AI cost and latency

LLM requests can introduce:

- API costs
- Network latency
- Rate limits

Caching and rate limiting may eventually be required.

---

# MVP Definition

The first meaningful version of Daily Health Partner will contain:

```text
                    MVP
                     |
        +------------+------------+
        |            |            |
    Tracking       Mood       Dashboard
        |            |            |
   Water           1-5       7-day data
   Sleep         Journal      Charts
   Steps
   Weight
        |            |            |
        +------------+------------+
                     |
                Authentication
```

After this works properly, the AI layer will be added.

---

# Development Philosophy

The project will be developed in small, testable steps.

Development order:

```text
Setup
  |
  v
Database
  |
  v
Authentication
  |
  v
Health Tracking
  |
  v
Dashboard
  |
  v
Mood
  |
  v
AI
  |
  v
Medications
  |
  v
Appointments
  |
  v
Symptoms
  |
  v
Trends
  |
  v
Reports
  |
  v
Deployment
```

Each stage should leave the application in a usable state.

---

# Project Goal

The final goal is to demonstrate the ability to build a complete full-stack application involving:

- REST API development
- Python/FastAPI
- PostgreSQL
- SQLAlchemy
- React
- Authentication
- Database design
- Data visualization
- LLM integration
- Context-based AI responses
- Health-data processing
- API integration
- Frontend/backend communication
- Deployment
- Documentation

The project is intended as a portfolio-grade full-stack + AI application while maintaining a clear distinction between lifestyle tracking and medical diagnosis.

---

# Status

**Current Stage: Phase 0 — Setup**

```text
Project Structure        [x]
Backend Skeleton         [x]
Frontend Skeleton        [x]
Python Virtual Env       [x]
Python Dependencies      [x]
PostgreSQL Installation  [x]
PostgreSQL Server        [ ]
Database Connection      [ ]
Backend Implementation   [ ]
Frontend Implementation  [ ]
AI Layer                 [ ]
Deployment               [ ]
```

---

## License

This project is currently being developed as a personal portfolio project.
