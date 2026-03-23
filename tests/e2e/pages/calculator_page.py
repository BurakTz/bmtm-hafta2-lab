# tests/e2e/pages/calculator_page.py
"""
Page Object Model (POM) — CalculatorPage
=========================================

Bu sinif, Calculator web arayuzunun tum UI etkilesimlerini
tek bir yerde toplar. Testler dogrudan selector kullanmak yerine
bu sinifin metodlarini cagirir.

POM Avantajlari:
    - Selector'ler tek yerde → UI degisirse sadece burasi guncellenir
    - Testler daha okunakli → page.fill('[data-testid="input-a"]', "10")
      yerine calculator.set_number_a("10")
    - Tekrar eden kod azalir → goto + fill + click her testte tekrarlanmaz

Kullanim:
    def test_add(page):
        calc = CalculatorPage(page)
        calc.goto()
        calc.set_number_a("10")
        calc.set_number_b("5")
        calc.set_operation("add")
        calc.calculate()
        calc.expect_result("15")
"""

import os

from playwright.sync_api import Page, expect

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")


class CalculatorPage:
    """Calculator sayfasinin Page Object'i.

    Tum selector'ler ve UI etkilesimleri bu sinifta toplanir.
    Testler bu sinifin metodlarini kullanarak sayfa ile etkilesir.
    """

    # ── Selector'ler (tek yerde, degisirse sadece burasi guncellenir) ──
    TITLE = '[data-testid="title"]'
    INPUT_A = '[data-testid="input-a"]'
    INPUT_B = '[data-testid="input-b"]'
    OPERATION_SELECT = '[data-testid="operation-select"]'
    CALCULATE_BTN = '[data-testid="calculate-btn"]'
    RESULT_BOX = '[data-testid="result-box"]'
    RESULT_VALUE = '[data-testid="result-value"]'
    HISTORY_ITEM = '[data-testid="history-item"]'
    CLEAR_HISTORY_BTN = '[data-testid="clear-history-btn"]'

    def __init__(self, page: Page) -> None:
        self.page = page

    # ── Navigasyon ──

    def goto(self) -> None:
        """Calculator sayfasina git."""
        self.page.goto(BASE_URL)

    # ── Input islemleri ──

    def set_number_a(self, value: str) -> None:
        """Birinci sayi alanini doldur."""
        self.page.fill(self.INPUT_A, value)

    def set_number_b(self, value: str) -> None:
        """Ikinci sayi alanini doldur."""
        self.page.fill(self.INPUT_B, value)

    def set_operation(self, op: str) -> None:
        """Islem turunu sec (add, subtract, multiply, divide, power, percentage)."""
        self.page.select_option(self.OPERATION_SELECT, op)

    def calculate(self) -> None:
        """Hesapla butonuna tikla."""
        self.page.click(self.CALCULATE_BTN)

    # ── Sonuc okuma ──

    def get_result(self) -> str:
        """Sonuc metnini dondur."""
        return self.page.locator(self.RESULT_VALUE).inner_text()

    # ── Gecmis islemleri ──

    def get_history_count(self) -> int:
        """Gecmis kayit sayisini dondur."""
        return self.page.locator(self.HISTORY_ITEM).count()

    def clear_history(self) -> None:
        """Gecmisi temizle butonuna tikla."""
        self.page.click(self.CLEAR_HISTORY_BTN)

    # ── Assertion metodlari ──

    def expect_result(self, text: str) -> None:
        """Sonucun tam olarak `text` oldugunu dogrula."""
        expect(self.page.locator(self.RESULT_VALUE)).to_have_text(text)

    def expect_result_contains(self, text: str) -> None:
        """Sonucun `text` icerdigini dogrula."""
        expect(self.page.locator(self.RESULT_VALUE)).to_contain_text(text)

    def expect_history_count(self, count: int) -> None:
        """Gecmis kayit sayisini dogrula."""
        expect(self.page.locator(self.HISTORY_ITEM)).to_have_count(count)

    def expect_history_contains(self, text: str) -> None:
        """Ilk gecmis kaydinin `text` icerdigini dogrula."""
        expect(self.page.locator(self.HISTORY_ITEM).first).to_contain_text(text)
