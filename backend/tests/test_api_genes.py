"""Test Gene API endpoints."""
import pytest
from fastapi.testclient import TestClient


class TestGeneList:
    """Test gene list endpoint."""

    def test_list_genes_empty(self, client: TestClient):
        """Test listing genes when empty."""
        response = client.get("/api/v1/genes")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_genes_with_data(self, client: TestClient):
        """Test listing genes with data."""
        # Create some genes first
        client.post("/api/v1/genes", json={"name": "gene_a"})
        client.post("/api/v1/genes", json={"name": "gene_b"})

        response = client.get("/api/v1/genes")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        names = [g["name"] for g in data]
        assert "gene_a" in names
        assert "gene_b" in names

    def test_list_genes_pagination(self, client: TestClient):
        """Test gene list pagination."""
        # Create 5 genes
        for i in range(5):
            client.post("/api/v1/genes", json={"name": f"gene_{i}"})

        # Get first 2
        response = client.get("/api/v1/genes?skip=0&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2

        # Get next 2
        response = client.get("/api/v1/genes?skip=2&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestGeneCreate:
    """Test gene create endpoint."""

    def test_create_gene_minimal(self, client: TestClient):
        """Test creating a gene with minimal data."""
        response = client.post(
            "/api/v1/genes",
            json={"name": "shell_exec"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "shell_exec"
        assert data["status"] == "draft"
        assert "id" in data
        assert "created_at" in data

    def test_create_gene_full(self, client: TestClient):
        """Test creating a gene with all fields."""
        response = client.post(
            "/api/v1/genes",
            json={
                "name": "full_gene",
                "description": "A complete gene",
                "implementation": "print('hello')",
                "prompt_template": "Say {word}",
                "status": "validated",
                "success_rate": 0.95,
                "context_tags": ["test", "example"],
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "full_gene"
        assert data["description"] == "A complete gene"
        assert data["status"] == "validated"
        assert data["success_rate"] == 0.95
        assert "test" in data["context_tags"]

    def test_create_gene_duplicate_name(self, client: TestClient):
        """Test creating a gene with duplicate name fails."""
        client.post("/api/v1/genes", json={"name": "duplicate"})

        response = client.post(
            "/api/v1/genes",
            json={"name": "duplicate"},
        )
        assert response.status_code == 400

    def test_create_gene_invalid_status(self, client: TestClient):
        """Test creating a gene with invalid status."""
        response = client.post(
            "/api/v1/genes",
            json={"name": "invalid", "status": "invalid_status"},
        )
        assert response.status_code == 422


class TestGeneGet:
    """Test gene get endpoint."""

    def test_get_gene_by_id(self, client: TestClient):
        """Test getting a gene by ID."""
        # Create first
        create_response = client.post(
            "/api/v1/genes",
            json={"name": "test_gene"},
        )
        gene_id = create_response.json()["id"]

        # Get by ID
        response = client.get(f"/api/v1/genes/{gene_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "test_gene"

    def test_get_gene_not_found(self, client: TestClient):
        """Test getting a non-existent gene."""
        response = client.get("/api/v1/genes/nonexistent")
        assert response.status_code == 404


class TestGeneUpdate:
    """Test gene update endpoint."""

    def test_update_gene(self, client: TestClient):
        """Test updating a gene."""
        # Create first
        create_response = client.post(
            "/api/v1/genes",
            json={"name": "gene_to_update"},
        )
        gene_id = create_response.json()["id"]

        # Update
        response = client.put(
            f"/api/v1/genes/{gene_id}",
            json={"status": "validated", "success_rate": 0.95},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "validated"
        assert data["success_rate"] == 0.95

    def test_update_gene_not_found(self, client: TestClient):
        """Test updating a non-existent gene."""
        response = client.put(
            "/api/v1/genes/nonexistent",
            json={"status": "validated"},
        )
        assert response.status_code == 404


class TestGeneDelete:
    """Test gene delete endpoint."""

    def test_delete_gene(self, client: TestClient):
        """Test deleting a gene."""
        # Create first
        create_response = client.post(
            "/api/v1/genes",
            json={"name": "gene_to_delete"},
        )
        gene_id = create_response.json()["id"]

        # Delete
        response = client.delete(f"/api/v1/genes/{gene_id}")
        assert response.status_code == 204

        # Verify deleted
        get_response = client.get(f"/api/v1/genes/{gene_id}")
        assert get_response.status_code == 404

    def test_delete_gene_not_found(self, client: TestClient):
        """Test deleting a non-existent gene."""
        response = client.delete("/api/v1/genes/nonexistent")
        assert response.status_code == 404
