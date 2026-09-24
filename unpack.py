from pathlib import Path

ROOT = Path("daily-health-partner")

directories = [
    # Backend
    "backend/app/database",
    "backend/app/auth",
    "backend/app/health",
    "backend/app/mood",
    "backend/app/medications",
    "backend/app/appointments",
    "backend/app/symptoms",
    "backend/app/ai",
    "backend/app/dashboard",

    # Frontend
    "frontend/src/components",
    "frontend/src/pages",
    "frontend/src/services",
    "frontend/src/hooks",
]

files = [
    # Backend
    "backend/app/main.py",
    "backend/app/database/connection.py",
    "backend/app/database/models.py",

    "backend/app/auth/routes.py",
    "backend/app/auth/schemas.py",
    "backend/app/auth/service.py",

    "backend/app/health/routes.py",
    "backend/app/health/schemas.py",
    "backend/app/health/service.py",

    "backend/app/mood/routes.py",
    "backend/app/mood/schemas.py",

    "backend/app/medications/routes.py",
    "backend/app/medications/schemas.py",

    "backend/app/appointments/routes.py",
    "backend/app/appointments/schemas.py",

    "backend/app/symptoms/routes.py",
    "backend/app/symptoms/schemas.py",

    "backend/app/ai/routes.py",
    "backend/app/ai/service.py",
    "backend/app/ai/prompts.py",

    "backend/app/dashboard/routes.py",
    "backend/app/dashboard/service.py",

    "backend/requirements.txt",
    "backend/.env",

    # Frontend
    "frontend/src/components/Navbar.jsx",
    "frontend/src/components/HealthCard.jsx",
    "frontend/src/components/HealthInput.jsx",
    "frontend/src/components/MoodCard.jsx",
    "frontend/src/components/Chart.jsx",
    "frontend/src/components/ReminderCard.jsx",
    "frontend/src/components/EmergencyCard.jsx",

    "frontend/src/pages/Login.jsx",
    "frontend/src/pages/Register.jsx",
    "frontend/src/pages/Dashboard.jsx",
    "frontend/src/pages/Health.jsx",
    "frontend/src/pages/Mood.jsx",
    "frontend/src/pages/Meals.jsx",
    "frontend/src/pages/Medications.jsx",
    "frontend/src/pages/Appointments.jsx",
    "frontend/src/pages/Symptoms.jsx",
    "frontend/src/pages/Assistant.jsx",
    "frontend/src/pages/Profile.jsx",

    "frontend/src/services/api.js",
    "frontend/src/services/auth.js",
    "frontend/src/services/health.js",
    "frontend/src/services/ai.js",

    "frontend/src/App.jsx",
    "frontend/src/main.jsx",
]


def create_skeleton():
    for directory in directories:
        path = ROOT / directory
        path.mkdir(parents=True, exist_ok=True)

    for file in files:
        path = ROOT / file
        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            path.touch()

    print("Daily Health Partner skeleton created successfully!")
    print(f"Location: {ROOT.resolve()}")


if __name__ == "__main__":
    create_skeleton()