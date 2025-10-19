from fastapi.testclient import TestClient
import pytest

from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # at least one known activity exists
    assert "Gym Class" in data


def test_signup_and_unregister_flow():
    activity = "Gym Class"
    email = "testuser@example.com"

    # Ensure the email is not already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    json_data = resp.json()
    assert "Signed up" in json_data["message"]
    assert email in activities[activity]["participants"]

    # Signing up again should return 400
    resp_repeat = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_repeat.status_code == 400

    # Unregister
    resp_del = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp_del.status_code == 200
    del_json = resp_del.json()
    assert "Unregistered" in del_json["message"]
    assert email not in activities[activity]["participants"]

    # Unregistering again should return 404
    resp_del2 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp_del2.status_code == 404


def test_signup_unknown_activity():
    resp = client.post("/activities/Nonexistent/signup?email=x@example.com")
    assert resp.status_code == 404


def test_unregister_unknown_activity():
    resp = client.delete("/activities/Nonexistent/participants?email=x@example.com")
    assert resp.status_code == 404
