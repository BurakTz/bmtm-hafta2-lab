# tests/integration/test_api.py
"""
Calculator API'sini Flask test client ile test eden integration testler.

Birden fazla bilesen birlikte test edilir:
HTTP katmani + JSON parsing + Calculator + response.

Calistirma:
    pytest tests/integration/ -v
"""
import pytest


class TestHealthEndpoint:
    """GET /api/health — Saglik kontrolu."""

    def test_health_returns_200(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200

    def test_health_returns_healthy_status(self, client):
        response = client.get("/api/health")
        data = response.get_json()
        assert data["status"] == "healthy"
        assert data["service"] == "calculator-api"


class TestCalculateEndpoint:
    """POST /api/calculate — Ana hesaplama endpoint'i."""

    # ── Basarili Islemler (200 OK) ──

    def test_add_returns_correct_result(self, clean_client):
        response = clean_client.post("/api/calculate", json={
            "operation": "add", "a": 10, "b": 5
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data["result"] == 15
        assert data["operation"] == "add"

    def test_subtract_returns_correct_result(self, clean_client):
        response = clean_client.post("/api/calculate", json={
            "operation": "subtract", "a": 10, "b": 3
        })
        assert response.status_code == 200
        assert response.get_json()["result"] == 7

    def test_multiply_returns_correct_result(self, clean_client):
        response = clean_client.post("/api/calculate", json={
            "operation": "multiply", "a": 4, "b": 5
        })
        assert response.status_code == 200
        assert response.get_json()["result"] == 20

    def test_divide_returns_correct_result(self, clean_client):
        response = clean_client.post("/api/calculate", json={
            "operation": "divide", "a": 10, "b": 4
        })
        assert response.status_code == 200
        assert response.get_json()["result"] == 2.5

    def test_power_returns_correct_result(self, clean_client):
        response = clean_client.post("/api/calculate", json={
            "operation": "power", "a": 2, "b": 8
        })
        assert response.status_code == 200
        assert response.get_json()["result"] == 256

    def test_percentage_returns_correct_result(self, clean_client):
        response = clean_client.post("/api/calculate", json={
            "operation": "percentage", "a": 200, "b": 15
        })
        assert response.status_code == 200
        assert response.get_json()["result"] == 30

    def test_average_returns_correct_result(self, clean_client):
        response = clean_client.post("/api/calculate", json={
            "operation": "average", "numbers": [10, 20, 30]
        })
        assert response.status_code == 200
        assert response.get_json()["result"] == 20

    # ── Hata Senaryolari (400 Bad Request) ──

    def test_missing_body_returns_400(self, client):
        response = client.post("/api/calculate",
                               content_type="application/json")
        assert response.status_code == 400

    def test_missing_operation_returns_400(self, client):
        response = client.post("/api/calculate", json={"a": 1, "b": 2})
        assert response.status_code == 400
        assert "Operation is required" in response.get_json()["error"]

    def test_unknown_operation_returns_400(self, client):
        response = client.post("/api/calculate", json={
            "operation": "modulo", "a": 10, "b": 3
        })
        assert response.status_code == 400
        assert "Unknown operation" in response.get_json()["error"]

    def test_missing_operands_returns_400(self, client):
        response = client.post("/api/calculate", json={
            "operation": "add", "a": 5
        })
        assert response.status_code == 400
        assert "'a' and 'b'" in response.get_json()["error"]

    def test_average_missing_numbers_returns_400(self, client):
        response = client.post("/api/calculate", json={
            "operation": "average"
        })
        assert response.status_code == 400

    # ── Is Mantigi Hatalari (422 Unprocessable Entity) ──

    def test_divide_by_zero_returns_422(self, client):
        response = client.post("/api/calculate", json={
            "operation": "divide", "a": 10, "b": 0
        })
        assert response.status_code == 422
        assert "Division by zero" in response.get_json()["error"]

    def test_negative_percentage_returns_422(self, client):
        response = client.post("/api/calculate", json={
            "operation": "percentage", "a": 100, "b": -5
        })
        assert response.status_code == 422
        assert "negative" in response.get_json()["error"]

    def test_average_empty_list_returns_422(self, client):
        response = client.post("/api/calculate", json={
            "operation": "average", "numbers": []
        })
        assert response.status_code == 422


class TestHistoryEndpoint:
    """GET/DELETE /api/history — Islem gecmisi."""

    def test_history_starts_empty(self, clean_client):
        response = clean_client.get("/api/history")
        assert response.status_code == 200
        data = response.get_json()
        assert data["count"] == 0
        assert data["history"] == []

    def test_history_records_calculations(self, clean_client):
        """Birden fazla islem yaptiktan sonra gecmis dogru olmali."""
        clean_client.post("/api/calculate", json={"operation": "add", "a": 1, "b": 2})
        clean_client.post("/api/calculate", json={"operation": "multiply", "a": 3, "b": 4})

        response = clean_client.get("/api/history")
        data = response.get_json()
        assert data["count"] == 2
        assert data["history"][0]["operation"] == "add"
        assert data["history"][1]["operation"] == "multiply"

    def test_clear_history(self, clean_client):
        clean_client.post("/api/calculate", json={"operation": "add", "a": 1, "b": 2})

        response = clean_client.delete("/api/history")
        assert response.status_code == 200
        assert "cleared" in response.get_json()["message"]

        # Gecmis gercekten temizlendi mi?
        history_response = clean_client.get("/api/history")
        assert history_response.get_json()["count"] == 0


class TestAPIWorkflow:
    """Gercek kullanim senaryolarini simule eden entegrasyon testleri.

    Bu testler birden fazla endpoint'i sirayla kullanarak
    gercek bir kullanici akisini test eder.
    """

    def test_full_calculation_workflow(self, clean_client):
        """Hesapla → gecmisi kontrol et → temizle → tekrar kontrol et."""
        # 1. Birkac hesaplama yap
        clean_client.post("/api/calculate", json={"operation": "add", "a": 10, "b": 20})
        clean_client.post("/api/calculate", json={"operation": "multiply", "a": 5, "b": 3})
        clean_client.post("/api/calculate", json={"operation": "divide", "a": 100, "b": 4})

        # 2. Gecmiste 3 kayit olmali
        resp = clean_client.get("/api/history")
        assert resp.get_json()["count"] == 3

        # 3. Gecmisi temizle
        clean_client.delete("/api/history")

        # 4. Gecmis bos olmali
        resp = clean_client.get("/api/history")
        assert resp.get_json()["count"] == 0

    def test_error_does_not_break_subsequent_requests(self, clean_client):
        """Hatali istek sonrasi API duzgun calismaya devam etmeli."""
        # Hatali istek
        resp1 = clean_client.post("/api/calculate", json={
            "operation": "divide", "a": 10, "b": 0
        })
        assert resp1.status_code == 422

        # Sonraki istek duzgun calismali
        resp2 = clean_client.post("/api/calculate", json={
            "operation": "add", "a": 5, "b": 3
        })
        assert resp2.status_code == 200
        assert resp2.get_json()["result"] == 8
