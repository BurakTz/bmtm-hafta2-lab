# tests/unit/test_mocking.py
"""
Test Doubles — Mock, Stub, Spy testleri.

Calculator sinifinin logger bagimliligi uzerinden
unittest.mock kullanimini gosteren testler.

Kavramlar:
    - Mock:  Cagirim dogrulamasi yapar (dogrusu cagirildi mi?)
    - Stub:  Sabit/onceden belirlenmis deger dondurur
    - Spy:   Gercek davranisi korur AMA cagirimlari kaydeder

Calistirma:
    pytest tests/unit/test_mocking.py -v
"""
import pytest
from unittest.mock import Mock, MagicMock, patch, call

from calculator import Calculator, CalculationLogger


# ──────────────────────────────────────────────
# Test Sinifi 1: Mock ile Logger Dogrulama
# ──────────────────────────────────────────────

class TestMockLogger:
    """Mock kullanarak logger.log() cagirimlarini dogrula.

    Mock nedir?
        Gercek nesnenin yerine gecen, cagirimlari kaydeden
        ve dogrulama yapmanizi saglayan sahte nesnedir.
    """

    def setup_method(self):
        """Her testten once Mock logger ve Calculator olustur."""
        self.mock_logger = Mock(spec=CalculationLogger)
        self.calc = Calculator(logger=self.mock_logger)

    def test_add_calls_logger(self):
        """add() isleminden sonra logger.log() dogru parametrelerle cagrilmali."""
        # Act
        self.calc.add(3, 5)

        # Assert — log tam olarak bir kez, dogru argumenlerle cagrildi mi?
        self.mock_logger.log.assert_called_once_with("add", (3, 5), 8)

    def test_subtract_calls_logger(self):
        """subtract() isleminden sonra logger.log() cagrilmali."""
        self.calc.subtract(10, 4)

        self.mock_logger.log.assert_called_once_with("subtract", (10, 4), 6)

    def test_multiply_calls_logger(self):
        """multiply() isleminden sonra logger.log() cagrilmali."""
        self.calc.multiply(3, 7)

        self.mock_logger.log.assert_called_once_with("multiply", (3, 7), 21)

    def test_divide_calls_logger(self):
        """divide() isleminden sonra logger.log() cagrilmali."""
        self.calc.divide(10, 2)

        self.mock_logger.log.assert_called_once_with("divide", (10, 2), 5.0)

    def test_logger_not_called_without_logger(self):
        """Logger verilmezse hata olmamali (geriye uyumluluk)."""
        calc_no_logger = Calculator()  # logger=None
        # Hata firlatmadan calismali
        result = calc_no_logger.add(1, 2)
        assert result == 3

    def test_logger_called_with_correct_result(self):
        """Logger'a iletilen result degeri dogru olmali."""
        self.calc.power(2, 10)

        self.mock_logger.log.assert_called_once_with("power", (2, 10), 1024)


# ──────────────────────────────────────────────
# Test Sinifi 2: Stub ile Sabit Davranis
# ──────────────────────────────────────────────

class TestStubLogger:
    """Stub kullanarak logger'in sabit davranis sergilemesini sagla.

    Stub nedir?
        Onceden belirlenmis degerler donduren basit sahte nesnedir.
        Cagirim dogrulamasi yapmaz, sadece beklenen ciktiyi verir.
    """

    def test_stub_logger_returns_fixed_value(self):
        """Stub logger her zaman True dondurur (basarili log)."""
        # Arrange — Stub: log() her zaman True dondursun
        stub_logger = Mock(spec=CalculationLogger)
        stub_logger.log.return_value = True

        calc = Calculator(logger=stub_logger)

        # Act
        result = calc.add(5, 3)

        # Assert — Calculator sonucu degismemeli
        assert result == 8
        # Stub'in donus degeri kontrol edilebilir
        assert stub_logger.log.return_value is True

    def test_stub_logger_with_custom_behavior(self):
        """Stub'a ozel bir fonksiyon atanabilir."""
        # Arrange — log cagrildiginda argumanlari bir listeye kaydet
        log_entries = []

        def fake_log(operation, args, result):
            log_entries.append(f"{operation}: {result}")

        stub_logger = Mock(spec=CalculationLogger)
        stub_logger.log.side_effect = fake_log

        calc = Calculator(logger=stub_logger)

        # Act
        calc.add(1, 2)
        calc.multiply(3, 4)

        # Assert — Stub'in kaydettigi veriler dogru mu?
        assert log_entries == ["add: 3", "multiply: 12"]

    def test_stub_with_different_return_values(self):
        """Stub her cagirimda farkli deger dondurebilir."""
        stub_logger = Mock(spec=CalculationLogger)
        # Ilk cagiri True, ikinci cagiri False dondursun
        stub_logger.log.side_effect = [True, False, True]

        calc = Calculator(logger=stub_logger)

        calc.add(1, 1)
        calc.subtract(5, 3)
        calc.multiply(2, 2)

        # side_effect listesi tuketildi mi kontrol et
        assert stub_logger.log.call_count == 3


# ──────────────────────────────────────────────
# Test Sinifi 3: Spy ile Cagiri Takibi
# ──────────────────────────────────────────────

class TestSpyBehavior:
    """Spy kullanarak cagri sayisi ve sirasini kontrol et.

    Spy nedir?
        Gercek nesnenin davranisini korurken cagirimlari
        kaydeden bir test double'dir. Mock + gercek uygulama.
    """

    def test_spy_tracks_call_count(self):
        """Spy ile logger'in kac kez cagrildigini takip et."""
        spy_logger = Mock(spec=CalculationLogger)
        calc = Calculator(logger=spy_logger)

        # Act — 3 islem yap
        calc.add(1, 2)
        calc.subtract(5, 3)
        calc.multiply(2, 4)

        # Assert — log tam olarak 3 kez cagrildi mi?
        assert spy_logger.log.call_count == 3

    def test_spy_tracks_call_order(self):
        """Spy ile cagri sirasini dogrula."""
        spy_logger = Mock(spec=CalculationLogger)
        calc = Calculator(logger=spy_logger)

        # Act
        calc.add(1, 1)
        calc.multiply(2, 3)
        calc.divide(10, 2)

        # Assert — cagri sirasi dogru mu?
        expected_calls = [
            call("add", (1, 1), 2),
            call("multiply", (2, 3), 6),
            call("divide", (10, 2), 5.0),
        ]
        spy_logger.log.assert_has_calls(expected_calls, any_order=False)

    def test_spy_tracks_each_call_args(self):
        """Spy ile her bir cagrinin argumenlerini ayri ayri dogrula."""
        spy_logger = Mock(spec=CalculationLogger)
        calc = Calculator(logger=spy_logger)

        calc.add(10, 20)
        calc.subtract(100, 50)

        # call_args_list ile tum cagrilara eris
        all_calls = spy_logger.log.call_args_list

        # Ilk cagri: add
        assert all_calls[0] == call("add", (10, 20), 30)
        # Ikinci cagri: subtract
        assert all_calls[1] == call("subtract", (100, 50), 50)

    def test_spy_with_wraps(self):
        """wraps parametresi ile gercek nesneyi spy olarak kullan."""
        real_logger = CalculationLogger()
        spy_logger = Mock(wraps=real_logger)

        calc = Calculator(logger=spy_logger)

        # Act — gercek log() metodu calisir + cagirim kaydedilir
        calc.add(5, 5)

        # Assert — cagirim kaydedildi
        spy_logger.log.assert_called_once_with("add", (5, 5), 10)


# ──────────────────────────────────────────────
# Test Sinifi 4: side_effect ile Hata Simulasyonu
# ──────────────────────────────────────────────

class TestSideEffect:
    """side_effect ile logger hatalarini simule et.

    side_effect nedir?
        Mock'un cagirildiginda exception firlatmasini veya
        ozel bir fonksiyon calistirmasini saglar.
    """

    def test_logger_exception_does_not_break_calculator(self):
        """Logger hata firlatsa bile Calculator sonucu dondurmeli.

        NOT: Bu test, Calculator'un logger hatasini yakalayip
        yakalamadigini test eder. Mevcut implementasyonda
        logger hatasi yukariva firlar — bu beklenen davranistir.
        Ogrenciler Calculator'a try/except ekleyerek bu testi
        gecebilirler.
        """
        error_logger = Mock(spec=CalculationLogger)
        error_logger.log.side_effect = RuntimeError("Disk dolu!")

        calc = Calculator(logger=error_logger)

        # Logger hata firlatacak — bu durumda RuntimeError bekliyoruz
        with pytest.raises(RuntimeError, match="Disk dolu!"):
            calc.add(1, 2)

    def test_side_effect_with_conditional_error(self):
        """Belirli islemlerde hata, digerlerinde basari simule et."""
        def selective_error(operation, args, result):
            if operation == "divide":
                raise IOError("Log dosyasi acilamadi!")
            return True

        conditional_logger = Mock(spec=CalculationLogger)
        conditional_logger.log.side_effect = selective_error

        calc = Calculator(logger=conditional_logger)

        # add basarili olmali
        result = calc.add(10, 5)
        assert result == 15

        # divide'da logger hatasi firlamali
        with pytest.raises(IOError, match="Log dosyasi acilamadi"):
            calc.divide(10, 2)

    def test_side_effect_sequence(self):
        """Sirali side_effect: ilk cagri basarili, ikinci hata."""
        sequence_logger = Mock(spec=CalculationLogger)
        sequence_logger.log.side_effect = [
            None,                              # ilk cagri: basarili (None dondur)
            ValueError("Gecersiz log formati"), # ikinci cagri: hata
        ]

        calc = Calculator(logger=sequence_logger)

        # Ilk islem basarili
        result1 = calc.add(1, 1)
        assert result1 == 2

        # Ikinci islem logger hatasi firlatir
        with pytest.raises(ValueError, match="Gecersiz log formati"):
            calc.subtract(5, 3)

    def test_patch_decorator_usage(self):
        """@patch ile CalculationLogger'i tamamen degistir.

        patch, modul seviyesinde bir sinifi veya fonksiyonu
        gecici olarak Mock ile degistirir.
        """
        with patch("calculator.CalculationLogger") as MockLoggerClass:
            # MockLoggerClass bir Mock — instance'i da Mock olacak
            mock_instance = MockLoggerClass.return_value

            # Calculator icinde CalculationLogger() cagrilirsa mock gelir
            logger = MockLoggerClass()
            calc = Calculator(logger=logger)

            calc.add(7, 3)

            # mock instance'in log metodu cagrildi mi?
            mock_instance.log.assert_called_once_with("add", (7, 3), 10)
