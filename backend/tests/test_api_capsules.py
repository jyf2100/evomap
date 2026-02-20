"""Test Capsule API endpoints."""
import pytest
from fastapi.testclient import TestClient


class TestCapsuleList:
    """Test capsule list endpoint."""

    def test_list_capsules_empty(self, client: TestClient):
        """Test listing capsules when empty."""
        response = client.get("/api/v1/capsules")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_capsules_with_data(self, client: TestClient):
        """Test listing capsules with data."""
        # Create some capsules first
        client.post("/api/v1/capsules", json={"name": "capsule_a"})
        client.post("/api/v1/capsules", json={"name": "capsule_b"})

        response = client.get("/api/v1/capsules")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        names = [c["name"] for c in data]
        assert "capsule_a" in names
        assert "capsule_b" in names


class TestCapsuleCreate:
    """Test capsule create endpoint."""

    def test_create_capsule_minimal(self, client: TestClient):
        """Test creating a capsule with minimal data."""
        response = client.post(
            "/api/v1/capsules",
            json={"name": "test_capsule"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "test_capsule"
        assert "id" in data
        assert data["gene_ids"] == []

    def test_create_capsule_with_genes(self, client: TestClient):
        """Test creating a capsule with associated genes."""
        # Create genes first
        gene1 = client.post("/api/v1/genes", json={"name": "gene_1"}).json()
        gene2 = client.post("/api/v1/genes", json={"name": "gene_2"}).json()

        response = client.post(
            "/api/v1/capsules",
            json={
                "name": "capsule_with_genes",
                "gene_ids": [gene1["id"], gene2["id"]],
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert len(data["gene_ids"]) == 2
        assert gene1["id"] in data["gene_ids"]

    def test_create_capsule_duplicate_name(self, client: TestClient):
        """Test creating a capsule with duplicate name fails."""
        client.post("/api/v1/capsules", json={"name": "duplicate"})

        response = client.post(
            "/api/v1/capsules",
            json={"name": "duplicate"},
        )
        assert response.status_code == 400


class TestCapsuleGet:
    """Test capsule get endpoint."""

    def test_get_capsule_by_id(self, client: TestClient):
        """Test getting a capsule by ID."""
        # Create first
        create_response = client.post(
            "/api/v1/capsules",
            json={"name": "test_capsule"},
        )
        capsule_id = create_response.json()["id"]

        # Get by ID
        response = client.get(f"/api/v1/capsules/{capsule_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "test_capsule"

    def test_get_capsule_not_found(self, client: TestClient):
        """Test getting a non-existent capsule."""
        response = client.get("/api/v1/capsules/nonexistent")
        assert response.status_code == 404


class TestCapsuleUpdate:
    """Test capsule update endpoint."""

    def test_update_capsule(self, client: TestClient):
        """Test updating a capsule."""
        # Create first
        create_response = client.post(
            "/api/v1/capsules",
            json={"name": "capsule_to_update"},
        )
        capsule_id = create_response.json()["id"]

        # Update
        response = client.put(
            f"/api/v1/capsules/{capsule_id}",
            json={"description": "Updated description"},
        )
        assert response.status_code == 200
        assert response.json()["description"] == "Updated description"


class TestCapsuleDelete:
    """Test capsule delete endpoint."""

    def test_delete_capsule(self, client: TestClient):
        """Test deleting a capsule."""
        # Create first
        create_response = client.post(
            "/api/v1/capsules",
            json={"name": "capsule_to_delete"},
        )
        capsule_id = create_response.json()["id"]

        # Delete
        response = client.delete(f"/api/v1/capsules/{capsule_id}")
        assert response.status_code == 204

        # Verify deleted
        get_response = client.get(f"/api/v1/capsules/{capsule_id}")
        assert get_response.status_code == 404
