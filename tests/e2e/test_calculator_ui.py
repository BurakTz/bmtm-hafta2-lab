# tests/e2e/test_calculator_ui.py
"""
Calculator web arayuzunu Playwright ile test eden E2E testler.

Gercek bir tarayicida kullanici etkilesimlerini simule eder.

Kurulum:
    pip install pytest-playwright
    playwright install chromium

Calistirma (Flask server calisirken):
    pytest tests/e2e/ -v
    pytest tests/e2e/ -v --headed              # Tarayiciyi gorerek
    pytest tests/e2e/ -v --headed --slowmo=500 # Yavas modda
"""
import pytest

# ═══════════════════════════════════════════════════════════
# NOT: Bu testler "pytest-playwright" ve calisan bir Flask
# server gerektirir. Kurulum talimatlari README.md'de.
#
# Eger pytest-playwright kurulu degilse testler SKIP edilir.
# ═══════════════════════════════════════════════════════════

try:
    from playwright.sync_api import expect
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not PLAYWRIGHT_AVAILABLE,
    reason="pytest-playwright kurulu degil. Kurulum: pip install pytest-playwright && playwright install chromium"
)

import os
BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")


class TestPageLoad:
    """Sayfa yuklenme ve temel UI element kontrolleri."""

    def test_page_title_is_visible(self, page):
        """Sayfa yuklendiginde baslik gorunur olmali."""
        page.goto(BASE_URL)
        title = page.locator('[data-testid="title"]')
        expect(title).to_be_visible()
        expect(title).to_contain_text("BMTM Calculator")

    def test_input_fields_are_visible(self, page):
        """Giris alanlari ve buton gorunur olmali."""
        page.goto(BASE_URL)
        expect(page.locator('[data-testid="input-a"]')).to_be_visible()
        expect(page.locator('[data-testid="input-b"]')).to_be_visible()
        expect(page.locator('[data-testid="operation-select"]')).to_be_visible()
        expect(page.locator('[data-testid="calculate-btn"]')).to_be_visible()

    def test_result_box_hidden_initially(self, page):
        """Sonuc kutusu baslangicta gizli olmali."""
        page.goto(BASE_URL)
        result_box = page.locator('[data-testid="result-box"]')
        expect(result_box).not_to_be_visible()


class TestAddition:
    """Toplama islemi E2E testleri."""

    def test_add_two_numbers(self, page):
        """Kullanici iki sayi girip Hesapla'ya tikladiginda dogru sonuc gosterilmeli."""
        page.goto(BASE_URL)

        # Sayilari gir
        page.fill('[data-testid="input-a"]', "10")
        page.fill('[data-testid="input-b"]', "5")

        # Islem sec (toplama varsayilan)
        page.select_option('[data-testid="operation-select"]', "add")

        # Hesapla butonuna tikla
        page.click('[data-testid="calculate-btn"]')

        # Sonuc dogru olmali
        result = page.locator('[data-testid="result-value"]')
        expect(result).to_have_text("15")

    def test_add_negative_numbers(self, page):
        page.goto(BASE_URL)
        page.fill('[data-testid="input-a"]', "-3")
        page.fill('[data-testid="input-b"]', "-7")
        page.select_option('[data-testid="operation-select"]', "add")
        page.click('[data-testid="calculate-btn"]')

        expect(page.locator('[data-testid="result-value"]')).to_have_text("-10")


class TestDivision:
    """Bolme islemi E2E testleri."""

    def test_divide_two_numbers(self, page):
        page.goto(BASE_URL)
        page.fill('[data-testid="input-a"]', "10")
        page.fill('[data-testid="input-b"]', "4")
        page.select_option('[data-testid="operation-select"]', "divide")
        page.click('[data-testid="calculate-btn"]')

        expect(page.locator('[data-testid="result-value"]')).to_have_text("2.5")

    def test_divide_by_zero_shows_error(self, page):
        """Sifira bolme hata mesaji gostermeli."""
        page.goto(BASE_URL)
        page.fill('[data-testid="input-a"]', "10")
        page.fill('[data-testid="input-b"]', "0")
        page.select_option('[data-testid="operation-select"]', "divide")
        page.click('[data-testid="calculate-btn"]')

        result = page.locator('[data-testid="result-value"]')
        expect(result).to_contain_text("Sifira bolme hatasi")


class TestAllOperations:
    """Tum islem turlerini test eder."""

    @pytest.mark.parametrize("operation, a, b, expected", [
        ("add", "8", "3", "11"),
        ("subtract", "8", "3", "5"),
        ("multiply", "8", "3", "24"),
        ("divide", "9", "3", "3"),
        ("power", "2", "10", "1024"),
        ("percentage", "200", "15", "30"),
    ])
    def test_operation(self, page, operation, a, b, expected):
        """Tum islem turlerini parametrize ile test et."""
        page.goto(BASE_URL)
        page.fill('[data-testid="input-a"]', a)
        page.fill('[data-testid="input-b"]', b)
        page.select_option('[data-testid="operation-select"]', operation)
        page.click('[data-testid="calculate-btn"]')

        expect(page.locator('[data-testid="result-value"]')).to_have_text(expected)


class TestValidation:
    """Girdi dogrulama E2E testleri."""

    def test_empty_inputs_show_error(self, page):
        """Bos giris alanlari hata mesaji gostermeli."""
        page.goto(BASE_URL)
        page.click('[data-testid="calculate-btn"]')

        result = page.locator('[data-testid="result-value"]')
        expect(result).to_contain_text("gecerli sayi")


class TestHistory:
    """Islem gecmisi E2E testleri."""

    def test_history_records_calculation(self, page):
        """Hesaplama sonrasi gecmise kayit eklenmeli."""
        page.goto(BASE_URL)

        # Hesaplama yap
        page.fill('[data-testid="input-a"]', "5")
        page.fill('[data-testid="input-b"]', "3")
        page.select_option('[data-testid="operation-select"]', "add")
        page.click('[data-testid="calculate-btn"]')

        # Gecmiste bir kayit olmali
        history_items = page.locator('[data-testid="history-item"]')
        expect(history_items).to_have_count(1)
        expect(history_items.first).to_contain_text("5 + 3 = 8")

    def test_history_multiple_entries(self, page):
        """Birden fazla hesaplama sonrasi gecmis dogru olmali."""
        page.goto(BASE_URL)

        # Ilk hesaplama
        page.fill('[data-testid="input-a"]', "10")
        page.fill('[data-testid="input-b"]', "5")
        page.click('[data-testid="calculate-btn"]')

        # Ikinci hesaplama
        page.fill('[data-testid="input-a"]', "3")
        page.fill('[data-testid="input-b"]', "4")
        page.select_option('[data-testid="operation-select"]', "multiply")
        page.click('[data-testid="calculate-btn"]')

        # 2 kayit olmali (en yeni en ustte)
        history_items = page.locator('[data-testid="history-item"]')
        expect(history_items).to_have_count(2)

    def test_clear_history(self, page):
        """Gecmisi temizle butonu calismali."""
        page.goto(BASE_URL)

        # Hesaplama yap
        page.fill('[data-testid="input-a"]', "1")
        page.fill('[data-testid="input-b"]', "2")
        page.click('[data-testid="calculate-btn"]')

        # Gecmisi temizle
        page.click('[data-testid="clear-history-btn"]')

        # Gecmis bos olmali
        history_items = page.locator('[data-testid="history-item"]')
        expect(history_items).to_have_count(0)


class TestUserWorkflow:
    """Gercek kullanici senaryolarini simule eder.

    E2E testlerin en guclu yani: Gercek kullanici akislarini
    bastan sona test edebilmesidir.
    """

    def test_complete_calculation_flow(self, page):
        """
        Senaryo: Kullanici birkac hesaplama yapar ve gecmisi kontrol eder.

        1. Sayfayi ac
        2. 10 + 5 = 15 hesapla
        3. Sonucu kontrol et
        4. 15 * 3 = 45 hesapla
        5. Gecmiste 2 kayit oldugunu dogrula
        6. Gecmisi temizle
        7. Gecmisin bos oldugunu dogrula
        """
        page.goto(BASE_URL)

        # Adim 1: 10 + 5
        page.fill('[data-testid="input-a"]', "10")
        page.fill('[data-testid="input-b"]', "5")
        page.click('[data-testid="calculate-btn"]')
        expect(page.locator('[data-testid="result-value"]')).to_have_text("15")

        # Adim 2: 15 * 3
        page.fill('[data-testid="input-a"]', "15")
        page.fill('[data-testid="input-b"]', "3")
        page.select_option('[data-testid="operation-select"]', "multiply")
        page.click('[data-testid="calculate-btn"]')
        expect(page.locator('[data-testid="result-value"]')).to_have_text("45")

        # Adim 3: Gecmiste 2 kayit
        expect(page.locator('[data-testid="history-item"]')).to_have_count(2)

        # Adim 4: Temizle
        page.click('[data-testid="clear-history-btn"]')
        expect(page.locator('[data-testid="history-item"]')).to_have_count(0)
