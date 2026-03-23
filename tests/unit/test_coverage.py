# tests/unit/test_coverage.py
"""
calculator.py'nin yuksek coverage'a ulasmasini hedefleyen testler.

Calistirma:
    pytest tests/unit/test_coverage.py --cov=src --cov-report=term-missing
    pytest tests/ --cov=src --cov-report=html   # HTML rapor
"""
import pytest
from calculator import Calculator


class TestCoverageAdd:
    def setup_method(self):
        self.calc = Calculator()

    def test_add_int(self):
        assert self.calc.add(1, 2) == 3

    def test_add_float(self):
        assert self.calc.add(1.5, 2.5) == pytest.approx(4.0)

    def test_add_invalid_first_arg(self):
        with pytest.raises(TypeError):
            self.calc.add("x", 1)

    def test_add_invalid_second_arg(self):
        with pytest.raises(TypeError):
            self.calc.add(1, "x")


class TestCoverageDivide:
    def setup_method(self):
        self.calc = Calculator()

    def test_divide_normal(self):
        assert self.calc.divide(10, 5) == 2.0

    def test_divide_by_zero(self):
        with pytest.raises(ValueError):
            self.calc.divide(10, 0)

    def test_divide_invalid_type(self):
        with pytest.raises(TypeError):
            self.calc.divide("10", 2)


class TestCoveragePercentage:
    def setup_method(self):
        self.calc = Calculator()

    def test_percentage_normal(self):
        assert self.calc.percentage(100, 25) == 25

    def test_percentage_negative_rate(self):
        with pytest.raises(ValueError):
            self.calc.percentage(100, -5)

    def test_percentage_invalid_type(self):
        with pytest.raises(TypeError):
            self.calc.percentage("100", 25)


class TestCoverageAverage:
    def setup_method(self):
        self.calc = Calculator()

    def test_average_normal(self):
        assert self.calc.average([1, 2, 3]) == 2.0

    def test_average_tuple(self):
        assert self.calc.average((4, 5, 6)) == 5.0

    def test_average_empty_list(self):
        with pytest.raises(ValueError, match="empty"):
            self.calc.average([])

    def test_average_non_list(self):
        with pytest.raises(TypeError, match="list or tuple"):
            self.calc.average("abc")

    def test_average_non_numeric_element(self):
        with pytest.raises(TypeError, match="Non-numeric"):
            self.calc.average([1, "two", 3])

    def test_average_int_input(self):
        with pytest.raises(TypeError):
            self.calc.average(42)


class TestCoverageHistory:
    def setup_method(self):
        self.calc = Calculator()

    def test_get_history_empty(self):
        assert self.calc.get_history() == []

    def test_get_history_after_ops(self):
        self.calc.add(1, 2)
        assert len(self.calc.get_history()) == 1

    def test_clear_history(self):
        self.calc.add(1, 2)
        self.calc.clear_history()
        assert self.calc.get_history() == []

    def test_get_last_result_success(self):
        self.calc.add(10, 20)
        assert self.calc.get_last_result() == 30

    def test_get_last_result_no_ops(self):
        with pytest.raises(ValueError, match="No operations"):
            self.calc.get_last_result()


class TestCoverageValidate:
    """_validate_numbers tum metotlardan cagriliyor — her biri uzerinden test."""

    def setup_method(self):
        self.calc = Calculator()

    def test_validate_via_subtract(self):
        with pytest.raises(TypeError):
            self.calc.subtract(None, 5)

    def test_validate_via_multiply(self):
        with pytest.raises(TypeError):
            self.calc.multiply([1], 5)

    def test_validate_via_power(self):
        with pytest.raises(TypeError):
            self.calc.power("2", 3)
