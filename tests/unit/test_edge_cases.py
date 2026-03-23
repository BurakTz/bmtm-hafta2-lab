# tests/unit/test_edge_cases.py
"""
Sinir degerler ve beklenmedik girdilerle dayaniklilik testleri.

Calistirma:
    pytest tests/unit/test_edge_cases.py -v
"""
import pytest
from calculator import Calculator


class TestEdgeCases:

    def setup_method(self):
        self.calc = Calculator()

    # ── Buyuk Sayilar ──

    def test_add_large_numbers(self):
        assert self.calc.add(999_999_999, 1) == 1_000_000_000

    def test_multiply_large_numbers(self):
        assert self.calc.multiply(10**6, 10**6) == 10**12

    # ── Float Hassasiyet ──

    def test_add_float_precision(self):
        """Klasik floating point sorunu: 0.1 + 0.2 ≠ 0.3
        Cozum: pytest.approx kullanin!
        """
        result = self.calc.add(0.1, 0.2)
        # ❌ assert result == 0.3  → basarisiz olabilir
        assert result == pytest.approx(0.3)  # ✅

    def test_multiply_float_precision(self):
        result = self.calc.multiply(0.1, 0.2)
        assert result == pytest.approx(0.02, abs=1e-9)

    def test_divide_repeating_decimal(self):
        result = self.calc.divide(1, 3)
        assert result == pytest.approx(0.3333, rel=1e-3)

    # ── Negatif Sayilar ──

    def test_divide_two_negatives_positive_result(self):
        """(-) / (-) = (+)"""
        assert self.calc.divide(-10, -2) == 5.0

    def test_power_negative_base_even_exponent(self):
        """Negatif tabanin cift ussu pozitiftir."""
        assert self.calc.power(-2, 2) == 4

    def test_power_negative_base_odd_exponent(self):
        """Negatif tabanin tek ussu negatiftir."""
        assert self.calc.power(-2, 3) == -8

    # ── Sifir Senaryolari ──

    def test_multiply_zero_by_zero(self):
        assert self.calc.multiply(0, 0) == 0

    def test_power_zero_to_zero(self):
        """Python'da 0**0 = 1"""
        assert self.calc.power(0, 0) == 1

    def test_percentage_of_zero(self):
        assert self.calc.percentage(0, 50) == 0

    # ── Tip Hatalari (TypeError) ──

    def test_add_string_raises(self):
        with pytest.raises(TypeError):
            self.calc.add("a", 1)

    def test_add_none_raises(self):
        with pytest.raises(TypeError):
            self.calc.add(None, 1)

    def test_add_list_raises(self):
        with pytest.raises(TypeError):
            self.calc.add([1, 2], 3)

    def test_divide_string_raises(self):
        with pytest.raises(TypeError):
            self.calc.divide("10", "2")

    def test_multiply_boolean_accepted(self):
        """Python'da bool, int'in alt sinifidir!
        True = 1, False = 0 → isinstance(True, int) == True
        """
        assert self.calc.multiply(True, 5) == 5
        assert self.calc.multiply(False, 5) == 0

    # ── Average Edge Cases ──

    def test_average_negative_numbers(self):
        assert self.calc.average([-10, -20, -30]) == pytest.approx(-20.0)

    def test_average_tuple_input(self):
        """Tuple da kabul edilmeli."""
        assert self.calc.average((1, 2, 3)) == 2.0

    def test_average_string_element_raises(self):
        with pytest.raises(TypeError, match="Non-numeric"):
            self.calc.average([1, "two", 3])

    def test_average_none_element_raises(self):
        with pytest.raises(TypeError, match="Non-numeric"):
            self.calc.average([1, None, 3])

    # ── History Edge Cases ──

    def test_history_survives_error(self):
        """Hatali islem gecmisi bozmamali."""
        self.calc.add(1, 2)
        with pytest.raises(ValueError):
            self.calc.divide(1, 0)
        assert len(self.calc.get_history()) == 1  # sadece add kaydedildi

    def test_history_returns_copy(self):
        """get_history() orijinal listeyi degil kopyasini dondurmeli."""
        self.calc.add(1, 2)
        history = self.calc.get_history()
        history.clear()
        assert len(self.calc.get_history()) == 1  # orijinal bozulmadi
