# tests/conftest.py
"""
Tum test dosyalarinda kullanilabilecek ortak fixture'lar.

Fixture Scope'lari:
    function  → Her test fonksiyonu icin yeni instance (varsayilan)
    class     → Her test sinifi icin bir instance
    module    → Her test dosyasi icin bir instance
    session   → Tum test oturumu boyunca tek instance
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from calculator import Calculator


# ═══════════════════════════════════════════
# CALCULATOR FIXTURE
# ═══════════════════════════════════════════
@pytest.fixture
def calc():
    """Her test icin taze bir Calculator instance.

    Kullanim:
        def test_add(calc):
            assert calc.add(2, 3) == 5
    """
    return Calculator()


# ═══════════════════════════════════════════
# TEST VERILERI
# ═══════════════════════════════════════════
@pytest.fixture
def sample_pairs():
    """Farkli senaryolar icin sayi ciftleri ve beklenen toplama sonuclari."""
    return {
        "positive": {"a": 10, "b": 5, "sum": 15, "diff": 5, "prod": 50, "quot": 2.0},
        "negative": {"a": -3, "b": -7, "sum": -10, "diff": 4, "prod": 21, "quot": 3 / 7},
        "zero": {"a": 0, "b": 0, "sum": 0, "diff": 0, "prod": 0},
        "mixed": {"a": 3.14, "b": 2.71, "sum": 5.85, "diff": 0.43, "prod": 8.5094},
        "large": {"a": 999_999, "b": 1, "sum": 1_000_000, "diff": 999_998, "prod": 999_999},
    }


@pytest.fixture
def number_lists():
    """average() testleri icin cesitli sayi listeleri."""
    return {
        "simple": [1, 2, 3, 4, 5],
        "single": [42],
        "negative": [-10, -20, -30],
        "float": [1.5, 2.5, 3.5],
        "large": list(range(1, 101)),
    }


# ═══════════════════════════════════════════
# SESSION FIXTURE (gosterim amacli)
# ═══════════════════════════════════════════
@pytest.fixture(scope="session")
def course_info():
    """Tum oturum boyunca degismeyen ders bilgileri."""
    return {
        "course": "BMTM",
        "week": 2,
        "topic": "Test Otomasyonu Temelleri",
        "instructor": "Busra Ayaksiz",
    }
