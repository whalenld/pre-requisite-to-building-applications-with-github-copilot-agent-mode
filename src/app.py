"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    # Sports-related activities (grouped with original "Gym Class")
    "Gym Class": {
        "category": "Sports",
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "category": "Sports",
        "description": "Competitive soccer practices and matches",
        "schedule": "Daily practice Mon-Fri, 4:00 PM - 6:00 PM; matches on Saturdays",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "category": "Sports",
        "description": "Team practices, drills, and interschool competitions",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 7:00 PM; games on weekends",
        "max_participants": 15,
        "participants": ["logan@mergington.edu", "ethan@mergington.edu"]
    },

    # Artistic activities (grouped with original activities if applicable)
    "Art Club": {
        "category": "Arts",
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["isabella@mergington.edu"]
    },
    "Drama Club": {
        "category": "Arts",
        "description": "Acting workshops, rehearsals, and staged performances",
        "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["mia@mergington.edu", "charlotte@mergington.edu"]
    },

    # Intellectual activities (grouped with original "Chess Club")
    "Chess Club": {
        "category": "Intellectual",
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Debate Team": {
        "category": "Intellectual",
        "description": "Practice public speaking, argumentation, and competitive debate",
        "schedule": "Tuesdays, 4:00 PM - 6:00 PM; tournaments on select weekends",
        "max_participants": 18,
        "participants": ["henry@mergington.edu", "grace@mergington.edu"]
    },

    # STEM / Programming activities (grouped with original "Programming Class")
    "Programming Class": {
        "category": "STEM",
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Robotics Club": {
        "category": "STEM",
        "description": "Design, build, and program robots for competitions and projects",
        "schedule": "Thursdays and Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
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

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")


    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
