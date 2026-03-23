# test_homework_api.py
import pytest


class TestAbsoluteEndpoint:
    """absolute endpoint integration testleri"""

    def test_absolute_positive(self, client):
        # Arrange
        payload = {"operation": "absolute", "a": 5, "b": 0}
        # Act
        response = client.post("/api/calculate", json=payload)
        # Assert
        assert response.status_code == 200
        assert response.json["result"] == 5

    def test_absolute_negative(self, client):
        payload = {"operation": "absolute", "a": -5, "b": 0}
        response = client.post("/api/calculate", json=payload)
        assert response.status_code == 200
        assert response.json["result"] == 5

    def test_absolute_zero(self, client):
        payload = {"operation": "absolute", "a": 0, "b": 0}
        response = client.post("/api/calculate", json=payload)
        assert response.status_code == 200
        assert response.json["result"] == 0


class TestFactorialEndpoint:
    """factorial endpoint integration testleri"""

    def test_factorial_normal(self, client):
        payload = {"operation": "factorial", "a": 5, "b": 0}
        response = client.post("/api/calculate", json=payload)
        assert response.status_code == 200
        assert response.json["result"] == 120

    def test_factorial_zero(self, client):
        payload = {"operation": "factorial", "a": 0, "b": 0}
        response = client.post("/api/calculate", json=payload)
        assert response.status_code == 200
        assert response.json["result"] == 1