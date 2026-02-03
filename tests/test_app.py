import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestActivitiesEndpoint:
    """Test the /activities GET endpoint"""
    
    def test_get_activities(self):
        """Test retrieving all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Tennis Club" in data
        assert "Basketball Team" in data
        assert "Art Studio" in data
        assert "Drama Club" in data
        assert "Debate Team" in data
        assert "Science Club" in data
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_activity_has_required_fields(self):
        """Test that activities have required fields"""
        response = client.get("/activities")
        data = response.json()
        activity = data["Tennis Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity


class TestSignupEndpoint:
    """Test the /activities/{activity_name}/signup POST endpoint"""
    
    def test_signup_for_activity_success(self):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Tennis%20Club/signup?email=test@example.com"
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "test@example.com" in data["message"]

    def test_signup_activity_not_found(self):
        """Test signup for non-existent activity"""
        response = client.post(
            "/activities/NonExistent/signup?email=test@example.com"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_email(self):
        """Test duplicate signup for same activity"""
        email = "duplicate@example.com"
        # First signup should succeed
        response1 = client.post(
            f"/activities/Tennis%20Club/signup?email={email}"
        )
        assert response1.status_code == 200
        
        # Second signup with same email should fail
        response2 = client.post(
            f"/activities/Tennis%20Club/signup?email={email}"
        )
        assert response2.status_code == 400
        data = response2.json()
        assert "already signed up" in data["detail"]


class TestUnregisterEndpoint:
    """Test the /activities/{activity_name}/unregister POST endpoint"""
    
    def test_unregister_success(self):
        """Test successful unregister from activity"""
        email = "unregister@example.com"
        # First signup
        client.post(f"/activities/Basketball%20Team/signup?email={email}")
        
        # Then unregister
        response = client.post(
            f"/activities/Basketball%20Team/unregister?email={email}"
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]

    def test_unregister_activity_not_found(self):
        """Test unregister from non-existent activity"""
        response = client.post(
            "/activities/NonExistent/unregister?email=test@example.com"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_participant_not_found(self):
        """Test unregister non-existent participant"""
        response = client.post(
            "/activities/Tennis%20Club/unregister?email=notaparticipant@example.com"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Participant not found" in data["detail"]


class TestRootEndpoint:
    """Test the root endpoint redirect"""
    
    def test_root_redirect(self):
        """Test that root redirects to static HTML"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
