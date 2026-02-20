"""Test Event API endpoints."""
import pytest
from fastapi.testclient import TestClient


class TestEventList:
    """Test event list endpoint."""

    def test_list_events_empty(self, client: TestClient):
        """Test listing events when empty."""
        response = client.get("/api/v1/events")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_events_with_data(self, client: TestClient):
        """Test listing events with data."""
        # Create some events first
        client.post(
            "/api/v1/events",
            json={"event_type": "mutation", "description": "Event 1"},
        )
        client.post(
            "/api/v1/events",
            json={"event_type": "validation", "description": "Event 2"},
        )

        response = client.get("/api/v1/events")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_events_filter_by_type(self, client: TestClient):
        """Test filtering events by type."""
        # Create events of different types
        client.post(
            "/api/v1/events",
            json={"event_type": "mutation"},
        )
        client.post(
            "/api/v1/events",
            json={"event_type": "validation"},
        )
        client.post(
            "/api/v1/events",
            json={"event_type": "mutation"},
        )

        # Filter by mutation
        response = client.get("/api/v1/events?event_type=mutation")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(e["event_type"] == "mutation" for e in data)


class TestEventCreate:
    """Test event create endpoint."""

    def test_create_event(self, client: TestClient):
        """Test creating an event."""
        response = client.post(
            "/api/v1/events",
            json={
                "event_type": "mutation",
                "description": "Gene mutated",
                "payload": {"gene_id": "gene-123", "change": "added timeout"},
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["event_type"] == "mutation"
        assert data["description"] == "Gene mutated"
        assert data["payload"]["gene_id"] == "gene-123"

    def test_create_event_with_capsule(self, client: TestClient):
        """Test creating an event linked to a capsule."""
        # Create capsule first
        capsule = client.post(
            "/api/v1/capsules",
            json={"name": "test_capsule"},
        ).json()

        response = client.post(
            "/api/v1/events",
            json={
                "event_type": "validation",
                "capsule_id": capsule["id"],
                "description": "Capsule validated",
            },
        )
        assert response.status_code == 201
        assert response.json()["capsule_id"] == capsule["id"]


class TestEventGet:
    """Test event get endpoint."""

    def test_get_event_by_id(self, client: TestClient):
        """Test getting an event by ID."""
        # Create first
        create_response = client.post(
            "/api/v1/events",
            json={"event_type": "creation", "description": "Test event"},
        )
        event_id = create_response.json()["id"]

        # Get by ID
        response = client.get(f"/api/v1/events/{event_id}")
        assert response.status_code == 200
        assert response.json()["event_type"] == "creation"

    def test_get_event_not_found(self, client: TestClient):
        """Test getting a non-existent event."""
        response = client.get("/api/v1/events/nonexistent")
        assert response.status_code == 404
