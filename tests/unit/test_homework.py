# test_homework.py
import pytest
from calculator import Calculator


class TestAbsolute:
    """absolute() metodu testleri"""

    def setup_method(self):
        """Her testten önce yeni bir Calculator oluştur"""
        self.calc = Calculator()

    def test_absolute_positive_number(self):
        # Arrange
        number = 5
        # Act
        result = self.calc.absolute(number)
        # Assert
        assert result == 5

    def test_absolute_negative_number(self):
        # Arrange
        number = -5
        # Act
        result = self.calc.absolute(number)
        # Assert
        assert result == 5

    def test_absolute_zero(self):
        result = self.calc.absolute(0)
        assert result == 0

    def test_absolute_float(self):
        result = self.calc.absolute(-3.14)
        assert result == 3.14

    def test_absolute_string_raises_typeerror(self):
        with pytest.raises(TypeError):
            self.calc.absolute("abc")


class TestFactorial:
    """factorial() metodu testleri"""

    def setup_method(self):
        self.calc = Calculator()

    def test_factorial_normal(self):
        # 5! = 120
        result = self.calc.factorial(5)
        assert result == 120

    def test_factorial_zero(self):
        # 0! = 1 (matematiksel kural)
        result = self.calc.factorial(0)
        assert result == 1

    def test_factorial_one(self):
        # 1! = 1
        result = self.calc.factorial(1)
        assert result == 1

    def test_factorial_negative_raises_valueerror(self):
        with pytest.raises(ValueError):
            self.calc.factorial(-1)

    def test_factorial_float_raises_typeerror(self):
        with pytest.raises(TypeError):
            self.calc.factorial(2.5)