# calculator.py
"""
Calculator modulu.

Temel aritmetik islemleri yapan hesap makinesi ve loglama sinifi.
"""


class CalculationLogger:
    """Hesap makinesi islemlerini loglayan sinif.

    Test Doubles (Mock/Stub/Spy) ile degistirilerek
    bagimliliklarin izole test edilmesini saglar.
    """

    def log(self, operation, args, result):
        """Bir islemi loglar.

        Args:
            operation: Islem adi (orn. "add", "multiply")
            args: Islem argumanlari (tuple)
            result: Islem sonucu
        """
        print(f"[LOG] {operation}{args} = {result}")


class Calculator:
    """Temel aritmetik islemleri yapan hesap makinesi sinifi.

    Desteklenen islemler:
        - add, subtract, multiply, divide
        - power, percentage
        - average
        - history (islem gecmisi)
    """

    def __init__(self, logger=None):
        self._history = []
        self._logger = logger

    def add(self, a, b):
        """Iki sayiyi toplar.

        Args:
            a: Birinci sayi (int veya float)
            b: Ikinci sayi (int veya float)

        Returns:
            Iki sayinin toplami

        Raises:
            TypeError: Sayisal olmayan deger verildiginde
        """
        self._validate_numbers(a, b)
        result = a + b
        self._history.append({"operation": "add", "args": (a, b), "result": result})
        self._log_operation("add", (a, b), result)
        return result

    def subtract(self, a, b):
        """Ilk sayidan ikinci sayiyi cikarir."""
        self._validate_numbers(a, b)
        result = a - b
        self._history.append({"operation": "subtract", "args": (a, b), "result": result})
        self._log_operation("subtract", (a, b), result)
        return result

    def multiply(self, a, b):
        """Iki sayiyi carpar."""
        self._validate_numbers(a, b)
        result = a * b
        self._history.append({"operation": "multiply", "args": (a, b), "result": result})
        self._log_operation("multiply", (a, b), result)
        return result

    def divide(self, a, b):
        """Ilk sayiyi ikinci sayiya boler.

        Raises:
            ValueError: Bolen sifir oldugunda
        """
        self._validate_numbers(a, b)
        if b == 0:
            raise ValueError("Division by zero!")
        result = a / b
        self._history.append({"operation": "divide", "args": (a, b), "result": result})
        self._log_operation("divide", (a, b), result)
        return result

    def power(self, base, exponent):
        """Us alma islemi: base ** exponent"""
        self._validate_numbers(base, exponent)
        result = base ** exponent
        self._history.append({"operation": "power", "args": (base, exponent), "result": result})
        self._log_operation("power", (base, exponent), result)
        return result

    def percentage(self, number, rate):
        """Bir sayinin yuzdesini hesaplar: number * rate / 100

        Raises:
            ValueError: rate negatif oldugunda
        """
        self._validate_numbers(number, rate)
        if rate < 0:
            raise ValueError("Percentage rate cannot be negative!")
        result = number * rate / 100
        self._history.append({"operation": "percentage", "args": (number, rate), "result": result})
        self._log_operation("percentage", (number, rate), result)
        return result

    def average(self, numbers):
        """Sayi listesinin aritmetik ortalamasini hesaplar.

        Raises:
            ValueError: Liste bos oldugunda
            TypeError: Liste olmayan deger verildiginde
        """
        if not isinstance(numbers, (list, tuple)):
            raise TypeError("Expected list or tuple!")
        if len(numbers) == 0:
            raise ValueError("Cannot calculate average of empty list!")
        for n in numbers:
            if not isinstance(n, (int, float)):
                raise TypeError(f"Non-numeric value: {n}")
        result = sum(numbers) / len(numbers)
        self._history.append({"operation": "average", "args": tuple(numbers), "result": result})
        self._log_operation("average", tuple(numbers), result)
        return result

    def get_history(self):
        """Islem gecmisini dondurur."""
        return list(self._history)

    def clear_history(self):
        """Islem gecmisini temizler."""
        self._history.clear()

    def get_last_result(self):
        """Son islemin sonucunu dondurur.

        Raises:
            ValueError: Henuz islem yapilmamissa
        """
        if not self._history:
            raise ValueError("No operations performed yet!")
        return self._history[-1]["result"]

    def _log_operation(self, operation, args, result):
        """Logger varsa islemi loglar."""
        if self._logger:
            self._logger.log(operation, args, result)

    def _validate_numbers(self, *args):
        """Girdi degerlerinin sayisal oldugunu dogrular."""
        for arg in args:
            if not isinstance(arg, (int, float)):
                raise TypeError(f"Expected numeric value, got {type(arg).__name__}!")

    def absolute(self, number):
        """Bir sayinin mutlak degerini dondurur.

        Args:
            number: Sayisal deger (int veya float)

        Returns:
            Sayinin mutlak degeri (her zaman pozitif)

        Raises:
            TypeError: Sayisal olmayan deger verildiginde
        """
        self._validate_numbers(number)
        result = number if number >= 0 else -number
        self._history.append({"operation": "absolute", "args": (number,), "result": result})
        self._log_operation("absolute", (number,), result)
        return result

    def factorial(self, n):
        """n! (n faktoriyel) hesaplar.

        Args:
            n: Tam sayi (int), 0 veya pozitif olmali

        Returns:
            n! degeri

        Raises:
            TypeError: n tam sayi degilse
            ValueError: n negatifse
        """
        if not isinstance(n, int):
            raise TypeError("Factorial only works with integers!")
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers!")
        result = 1
        for i in range(2, n + 1):
            result *= i
        self._history.append({"operation": "factorial", "args": (n,), "result": result})
        self._log_operation("factorial", (n,), result)
        return result