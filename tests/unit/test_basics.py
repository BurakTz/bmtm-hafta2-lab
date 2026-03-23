# tests/unit/test_basics.py
"""
Calculator sinifinin temel islevselligini test eden unit testler.

Calistirma:
    pytest tests/unit/test_basics.py -v
"""
import pytest
from calculator import Calculator


class TestAdd:
    """add() metodu testleri.

    Isimlendirme: test_<method>_<scenario>_<expected>
    """

    def setup_method(self):
        """Her testten once calisir — taze Calculator olusturur."""
        self.calc = Calculator()

    def test_add_two_positive_numbers(self):
        """Iki pozitif sayinin toplamini dogrular."""
        # Arrange
        a, b = 2, 3
        # Act
        result = self.calc.add(a, b)
        # Assert
        assert result == 5

    def test_add_two_negative_numbers(self):
        assert self.calc.add(-1, -1) == -2

    def test_add_positive_and_negative(self):
        assert self.calc.add(-1, 1) == 0

    def test_add_with_zero(self):
        """Sifir ile toplama — birden fazla assertion ayni davranis icin."""
        assert self.calc.add(0, 0) == 0
        assert self.calc.add(5, 0) == 5
        assert self.calc.add(0, 5) == 5


class TestSubtract:
    """subtract() metodu testleri."""

    def setup_method(self):
        self.calc = Calculator()

    def test_subtract_positive_result(self):
        assert self.calc.subtract(10, 3) == 7

    def test_subtract_negative_result(self):
        assert self.calc.subtract(3, 10) == -7

    def test_subtract_equal_numbers(self):
        """Ayni sayilarin farki sifirdir."""
        assert self.calc.subtract(5, 5) == 0


class TestMultiply:
    """multiply() metodu testleri."""

    def setup_method(self):
        self.calc = Calculator()

    def test_multiply_two_positive(self):
        assert self.calc.multiply(3, 4) == 12

    def test_multiply_with_zero(self):
        """Sifir ile carpma her zaman sifir verir."""
        assert self.calc.multiply(100, 0) == 0
        assert self.calc.multiply(0, 100) == 0

    def test_multiply_two_negatives(self):
        """(-) × (-) = (+)"""
        assert self.calc.multiply(-3, -4) == 12

    def test_multiply_mixed_sign(self):
        """(-) × (+) = (-)"""
        assert self.calc.multiply(-3, 4) == -12


class TestDivide:
    """divide() metodu testleri."""

    def setup_method(self):
        self.calc = Calculator()

    def test_divide_exact(self):
        assert self.calc.divide(10, 2) == 5.0

    def test_divide_decimal_result(self):
        assert self.calc.divide(10, 3) == pytest.approx(3.333, rel=1e-2)

    def test_divide_negative(self):
        assert self.calc.divide(-10, 2) == -5.0

    def test_divide_by_zero_raises_error(self):
        """Sifira bolme ValueError firlatmali."""
        with pytest.raises(ValueError, match="Division by zero"):
            self.calc.divide(10, 0)

    def test_divide_by_zero_error_message(self):
        """Exception mesajinin dogrulugunu kontrol et."""
        with pytest.raises(ValueError) as exc_info:
            self.calc.divide(10, 0)
        assert "Division by zero!" in str(exc_info.value)


class TestPower:
    """power() metodu testleri."""

    def setup_method(self):
        self.calc = Calculator()

    def test_power_positive(self):
        assert self.calc.power(2, 3) == 8

    def test_power_zero_exponent(self):
        """Herhangi bir sayinin 0. ussu 1'dir."""
        assert self.calc.power(5, 0) == 1

    def test_power_one_exponent(self):
        assert self.calc.power(7, 1) == 7

    def test_power_negative_exponent(self):
        """Negatif us → kesirli sonuc."""
        assert self.calc.power(2, -1) == 0.5


class TestPercentage:
    """percentage() metodu testleri."""

    def setup_method(self):
        self.calc = Calculator()

    def test_percentage_basic(self):
        """200'un %50'si = 100"""
        assert self.calc.percentage(200, 50) == 100

    def test_percentage_zero_rate(self):
        assert self.calc.percentage(200, 0) == 0

    def test_percentage_full_rate(self):
        assert self.calc.percentage(200, 100) == 200

    def test_percentage_negative_rate_raises(self):
        with pytest.raises(ValueError, match="negative"):
            self.calc.percentage(100, -10)


class TestAverage:
    """average() metodu testleri."""

    def setup_method(self):
        self.calc = Calculator()

    def test_average_simple(self):
        assert self.calc.average([1, 2, 3, 4, 5]) == 3.0

    def test_average_single_element(self):
        assert self.calc.average([42]) == 42

    def test_average_empty_list_raises(self):
        with pytest.raises(ValueError, match="empty"):
            self.calc.average([])

    def test_average_non_list_raises(self):
        with pytest.raises(TypeError, match="list or tuple"):
            self.calc.average("abc")


class TestHistory:
    """get_history(), clear_history(), get_last_result() testleri."""

    def setup_method(self):
        self.calc = Calculator()

    def test_history_starts_empty(self):
        assert self.calc.get_history() == []

    def test_history_records_operation(self):
        self.calc.add(2, 3)
        history = self.calc.get_history()
        assert len(history) == 1
        assert history[0]["operation"] == "add"
        assert history[0]["result"] == 5

    def test_history_multiple_operations(self):
        self.calc.add(1, 2)
        self.calc.multiply(3, 4)
        assert len(self.calc.get_history()) == 2

    def test_clear_history(self):
        self.calc.add(1, 2)
        self.calc.clear_history()
        assert self.calc.get_history() == []

    def test_get_last_result(self):
        self.calc.add(10, 20)
        self.calc.multiply(3, 4)
        assert self.calc.get_last_result() == 12

    def test_get_last_result_no_operations_raises(self):
        with pytest.raises(ValueError, match="No operations"):
            self.calc.get_last_result()
