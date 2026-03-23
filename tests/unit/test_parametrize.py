# tests/unit/test_parametrize.py
"""
@pytest.mark.parametrize ile ayni testi farkli verilerle calistirma.

Calistirma:
    pytest tests/unit/test_parametrize.py -v
"""
import pytest
from calculator import Calculator

calc = Calculator()


# ═══════════════════════════════════════════
# TEMEL PARAMETRIZE
# ═══════════════════════════════════════════

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
    (100, -50, 50),
    (-10, -20, -30),
])
def test_add(a, b, expected):
    assert calc.add(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [
    (10, 3, 7),
    (3, 10, -7),
    (5, 5, 0),
    (-3, -7, 4),
])
def test_subtract(a, b, expected):
    assert calc.subtract(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [
    (3, 4, 12),
    (0, 100, 0),
    (-3, 4, -12),
    (-3, -4, 12),
])
def test_multiply(a, b, expected):
    assert calc.multiply(a, b) == expected


# ═══════════════════════════════════════════
# FLOAT SONUCLAR (pytest.approx ile)
# ═══════════════════════════════════════════

@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5.0),
    (10, 3, 3.3333),
    (1, 7, 0.1429),
    (-10, 3, -3.3333),
    (0, 5, 0.0),
])
def test_divide(a, b, expected):
    assert calc.divide(a, b) == pytest.approx(expected, rel=1e-3)


# ═══════════════════════════════════════════
# EXCEPTION PARAMETRIZE
# ═══════════════════════════════════════════

@pytest.mark.parametrize("a, b", [
    (10, 0), (-5, 0), (0, 0), (999_999, 0),
])
def test_divide_by_zero_raises(a, b):
    with pytest.raises(ValueError):
        calc.divide(a, b)


@pytest.mark.parametrize("invalid_input", [
    "abc", None, [1, 2], {"key": "val"},
])
def test_add_invalid_input_raises(invalid_input):
    with pytest.raises(TypeError):
        calc.add(invalid_input, 1)


# ═══════════════════════════════════════════
# US ALMA & YUZDE
# ═══════════════════════════════════════════

@pytest.mark.parametrize("base, exp, expected", [
    (2, 0, 1), (2, 1, 2), (2, 10, 1024),
    (3, 3, 27), (-2, 2, 4), (-2, 3, -8), (2, -1, 0.5),
])
def test_power(base, exp, expected):
    assert calc.power(base, exp) == pytest.approx(expected)


@pytest.mark.parametrize("number, rate, expected", [
    (200, 50, 100), (200, 0, 0), (200, 100, 200),
    (50, 10, 5), (99.99, 50, 49.995),
])
def test_percentage(number, rate, expected):
    assert calc.percentage(number, rate) == pytest.approx(expected)


@pytest.mark.parametrize("numbers, expected", [
    ([1, 2, 3], 2.0),
    ([10], 10.0),
    ([0, 0, 0], 0.0),
    ([-5, 5], 0.0),
    (list(range(1, 11)), 5.5),
])
def test_average(numbers, expected):
    assert calc.average(numbers) == pytest.approx(expected)


# ═══════════════════════════════════════════
# OKUNABILIR TEST ID'LERI
# ═══════════════════════════════════════════

@pytest.mark.parametrize("a, b, expected", [
    pytest.param(2, 3, 5, id="two-positives"),
    pytest.param(-1, 1, 0, id="negative-positive"),
    pytest.param(0, 0, 0, id="zeros"),
    pytest.param(1_000_000, 1, 1_000_001, id="large-number"),
])
def test_add_with_ids(a, b, expected):
    """Ciktida: test_add_with_ids[two-positives] PASSED"""
    assert calc.add(a, b) == expected
