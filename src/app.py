"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Bomboclaat High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Bomboclaat High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@bomboclaat.edu", "daniel@bomboclaat.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@bomboclaat.edu", "sophia@bomboclaat.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@bomboclaat.edu", "olivia@bomboclaat.edu"]
    },
    # Additional Sports Activities
    "Soccer Team": {
        "description": "Team practices focusing on drills, strategy, and scrimmages",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@bomboclaat.edu", "noah@bomboclaat.edu"]
    },
    "Track & Field": {
        "description": "Conditioning and event-specific training for runners and field athletes",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 28,
        "participants": ["ava@bomboclaat.edu"]
    },
    # Artistic Activities
    "Drama Club": {
        "description": "Acting exercises, script reading, and play production rehearsals",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["mia@bomboclaat.edu", "elijah@bomboclaat.edu"]
    },
    "Art Workshop": {
        "description": "Exploration of painting, drawing, and mixed media techniques",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["amelia@bomboclaat.edu"]
    },
    # Intellectual Activities
    "Math Olympiad Training": {
        "description": "Problem-solving sessions preparing for regional math competitions",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ethan@bomboclaat.edu", "harper@bomboclaat.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments and STEM project exploration",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["lucas@bomboclaat.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # (optional) Enforce capacity
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
