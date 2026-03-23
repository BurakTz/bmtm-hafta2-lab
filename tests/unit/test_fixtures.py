# tests/unit/test_fixtures.py
"""
conftest.py'deki fixture'lari kullanarak yazilmis testler.

Calistirma:
    pytest tests/unit/test_fixtures.py -v
"""
import pytest


class TestWithFixtures:
    """conftest.py'deki fixture'lari kullanan testler.

    `calc`, `sample_pairs`, `number_lists` fixture'lari
    conftest.py'de tanimlidir — pytest bunlari otomatik bulur.
    """

    # ── Tek Fixture ──

    def test_add_basic(self, calc):
        assert calc.add(1, 2) == 3

    def test_subtract_basic(self, calc):
        """Her test kendi taze calc instance'ini alir."""
        assert calc.subtract(10, 3) == 7

    # ── Iki Fixture Birlikte ──

    def test_add_positive_pair(self, calc, sample_pairs):
        p = sample_pairs["positive"]
        assert calc.add(p["a"], p["b"]) == p["sum"]

    def test_add_negative_pair(self, calc, sample_pairs):
        p = sample_pairs["negative"]
        assert calc.add(p["a"], p["b"]) == p["sum"]

    def test_subtract_positive_pair(self, calc, sample_pairs):
        p = sample_pairs["positive"]
        assert calc.subtract(p["a"], p["b"]) == p["diff"]

    def test_multiply_positive_pair(self, calc, sample_pairs):
        p = sample_pairs["positive"]
        assert calc.multiply(p["a"], p["b"]) == p["prod"]

    def test_add_mixed_pair(self, calc, sample_pairs):
        p = sample_pairs["mixed"]
        assert calc.add(p["a"], p["b"]) == pytest.approx(p["sum"])

    # ── Tum Ciftleri Donguyle Test Et ──

    def test_add_all_pairs(self, calc, sample_pairs):
        """Tum sayi ciftlerini tek test'te dogrula."""
        for key, p in sample_pairs.items():
            result = calc.add(p["a"], p["b"])
            assert result == pytest.approx(p["sum"]), \
                f"Hata: add({p['a']}, {p['b']}) = {result}, beklenen: {p['sum']}"

    # ── Number Lists Fixture ──

    def test_average_simple_list(self, calc, number_lists):
        assert calc.average(number_lists["simple"]) == 3.0

    def test_average_single_element(self, calc, number_lists):
        assert calc.average(number_lists["single"]) == 42

    def test_average_large_list(self, calc, number_lists):
        """1'den 100'e kadar ortalamasi 50.5'tir."""
        assert calc.average(number_lists["large"]) == pytest.approx(50.5)

    # ── Session Fixture ──

    def test_course_info(self, course_info):
        """session-scoped fixture tum testlerde ayni instance."""
        assert course_info["course"] == "BMTM"
        assert course_info["week"] == 2
