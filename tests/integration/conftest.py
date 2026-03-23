# tests/integration/conftest.py
"""
Integration testleri icin Flask test client fixture.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from app import app as flask_app


@pytest.fixture
def client():
    """Flask test client — gercek HTTP server baslatmadan API test eder.

    Flask'in built-in test client'i sayesinde integration testlerini
    hizli ve guvenilir sekilde calistirabiliriz.
    """
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def clean_client(client):
    """Her testten once history'yi temizleyen client.

    Testler arasi state paylasimini engeller.
    """
    client.delete("/api/history")
    return client
