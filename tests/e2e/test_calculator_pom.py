# tests/e2e/test_calculator_pom.py
"""
Page Object Model (POM) kullanarak yazilmis E2E testler.

test_calculator_ui.py'deki ayni senaryolarin POM versiyonu.
Selector'ler CalculatorPage sinifinda toplanir, testler daha okunakli olur.

Calistirma:
    BASE_URL=http://localhost:5050 pytest tests/e2e/test_calculator_pom.py -v
"""

import pytest

try:
    from playwright.sync_api import expect  # noqa: F401

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not PLAYWRIGHT_AVAILABLE,
    reason="pytest-playwright kurulu degil. Kurulum: pip install pytest-playwright && playwright install chromium",
)

if PLAYWRIGHT_AVAILABLE:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from pages.calculator_page import CalculatorPage


# ── Fixture: Her testte yeni CalculatorPage ──


@pytest.fixture()
def calc(page):
    """CalculatorPage fixture'u — her test icin yeni bir instance olusturur."""
    calculator = CalculatorPage(page)
    calculator.goto()
    return calculator


# ═══════════════════════════════════════════════════════════
# TOPLAMA TESTLERI
# ═══════════════════════════════════════════════════════════


class TestPomAddition:
    """Toplama islemi — POM versiyonu."""

    def test_add_two_numbers(self, calc):
        """10 + 5 = 15"""
        calc.set_number_a("10")
        calc.set_number_b("5")
        calc.set_operation("add")
        calc.calculate()
        calc.expect_result("15")

    def test_add_negative_numbers(self, calc):
        """-3 + -7 = -10"""
        calc.set_number_a("-3")
        calc.set_number_b("-7")
        calc.set_operation("add")
        calc.calculate()
        calc.expect_result("-10")


# ═══════════════════════════════════════════════════════════
# TUM ISLEMLER — PARAMETRIZE
# ═══════════════════════════════════════════════════════════


class TestPomOperations:
    """Tum islem turlerini parametrize ile test eder — POM versiyonu."""

    @pytest.mark.parametrize(
        "operation, a, b, expected",
        [
            ("add", "8", "3", "11"),
            ("subtract", "8", "3", "5"),
            ("multiply", "8", "3", "24"),
            ("divide", "9", "3", "3"),
            ("power", "2", "10", "1024"),
            ("percentage", "200", "15", "30"),
        ],
    )
    def test_operation(self, calc, operation, a, b, expected):
        calc.set_number_a(a)
        calc.set_number_b(b)
        calc.set_operation(operation)
        calc.calculate()
        calc.expect_result(expected)

    def test_divide_by_zero_shows_error(self, calc):
        """Sifira bolme hata mesaji gostermeli."""
        calc.set_number_a("10")
        calc.set_number_b("0")
        calc.set_operation("divide")
        calc.calculate()
        calc.expect_result_contains("Sifira bolme hatasi")


# ═══════════════════════════════════════════════════════════
# KULLANICI AKISI (WORKFLOW)
# ═══════════════════════════════════════════════════════════


class TestPomWorkflow:
    """Gercek kullanici senaryosu — POM versiyonu.

    Senaryo:
        1. 10 + 5 = 15 hesapla
        2. 15 * 3 = 45 hesapla
        3. Gecmiste 2 kayit oldugunu dogrula
        4. Gecmisi temizle
        5. Gecmisin bos oldugunu dogrula
    """

    def test_complete_calculation_flow(self, calc):
        # Adim 1: 10 + 5
        calc.set_number_a("10")
        calc.set_number_b("5")
        calc.calculate()
        calc.expect_result("15")

        # Adim 2: 15 * 3
        calc.set_number_a("15")
        calc.set_number_b("3")
        calc.set_operation("multiply")
        calc.calculate()
        calc.expect_result("45")

        # Adim 3: Gecmiste 2 kayit
        calc.expect_history_count(2)

        # Adim 4-5: Temizle ve dogrula
        calc.clear_history()
        calc.expect_history_count(0)


# ═══════════════════════════════════════════════════════════
# GECMIS ISLEMLERI
# ═══════════════════════════════════════════════════════════


class TestPomHistory:
    """Islem gecmisi testleri — POM versiyonu."""

    def test_history_records_calculation(self, calc):
        """Hesaplama sonrasi gecmise kayit eklenmeli."""
        calc.set_number_a("5")
        calc.set_number_b("3")
        calc.set_operation("add")
        calc.calculate()

        calc.expect_history_count(1)
        calc.expect_history_contains("5 + 3 = 8")

    def test_history_multiple_entries(self, calc):
        """Birden fazla hesaplama sonrasi gecmis dogru olmali."""
        # Ilk hesaplama
        calc.set_number_a("10")
        calc.set_number_b("5")
        calc.calculate()

        # Ikinci hesaplama
        calc.set_number_a("3")
        calc.set_number_b("4")
        calc.set_operation("multiply")
        calc.calculate()

        calc.expect_history_count(2)

    def test_clear_history(self, calc):
        """Gecmisi temizle butonu calismali."""
        calc.set_number_a("1")
        calc.set_number_b("2")
        calc.calculate()

        calc.clear_history()
        calc.expect_history_count(0)
