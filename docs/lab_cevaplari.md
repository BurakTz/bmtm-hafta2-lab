# 📝 BMTM Hafta 2 — Odev Cevap Sablonu

**Ogrenci Adi:** Burak Tuzcu
**Ogrenci No:** 170423042
**Tarih:** 23.03.2026

---

## Bolum 1: Calculator Genisletme

### 1.1 Eklenen Metotlar

```python
def absolute(self, number):
    """Bir sayinin mutlak degerini dondurur."""
    self._validate_numbers(number)
    result = number if number >= 0 else -number
    self._history.append({"operation": "absolute", "args": (number,), "result": result})
    self._log_operation("absolute", (number,), result)
    return result

def factorial(self, n):
    """n! (n faktoriyel) hesaplar.

    Raises:
        ValueError: n negatif oldugunda
        TypeError: n tam sayi olmadiginda
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
```

### 1.2 Yazilan Unit Testler

`tests/unit/test_homework.py` — 10 test:

```python
import pytest
from calculator import Calculator


class TestAbsolute:
    def setup_method(self):
        self.calc = Calculator()

    def test_absolute_positive_number(self):
        assert self.calc.absolute(5) == 5

    def test_absolute_negative_number(self):
        assert self.calc.absolute(-5) == 5

    def test_absolute_zero(self):
        assert self.calc.absolute(0) == 0

    def test_absolute_float(self):
        assert self.calc.absolute(-3.14) == 3.14

    def test_absolute_string_raises_typeerror(self):
        with pytest.raises(TypeError):
            self.calc.absolute("abc")


class TestFactorial:
    def setup_method(self):
        self.calc = Calculator()

    def test_factorial_normal(self):
        assert self.calc.factorial(5) == 120

    def test_factorial_zero(self):
        assert self.calc.factorial(0) == 1

    def test_factorial_one(self):
        assert self.calc.factorial(1) == 1

    def test_factorial_negative_raises_valueerror(self):
        with pytest.raises(ValueError):
            self.calc.factorial(-1)

    def test_factorial_float_raises_typeerror(self):
        with pytest.raises(TypeError):
            self.calc.factorial(2.5)
```

---

## Bolum 2: Coverage Raporu

| Dosya | Stmts | Miss | Cover |
|-------|-------|------|-------|
| src/app.py | 53 | 4 | 92.5% |
| src/calculator.py | 91 | 0 | 100.0% |
| **TOTAL** | **144** | **4** | **97.2%** |

**Hedef: %95+** ✅ Ulasildi

---

## Bolum 3: Integration Test

### 3.1 app.py'ye Eklenen Endpoint'ler

```python
elif operation == "absolute":
    a = data.get("a")
    if a is None:
        return jsonify({"error": "'a' field is required"}), 400
    result = calc.absolute(a)

elif operation == "factorial":
    a = data.get("a")
    if a is None:
        return jsonify({"error": "'a' field is required"}), 400
    result = calc.factorial(int(a))
```

### 3.2 Yazilan Integration Testler

`tests/integration/test_homework_api.py` — 5 test:

```python
class TestAbsoluteEndpoint:
    def test_absolute_positive(self, client):
        response = client.post("/api/calculate", json={"operation": "absolute", "a": 5, "b": 0})
        assert response.status_code == 200
        assert response.json["result"] == 5

    def test_absolute_negative(self, client):
        response = client.post("/api/calculate", json={"operation": "absolute", "a": -5, "b": 0})
        assert response.status_code == 200
        assert response.json["result"] == 5

    def test_absolute_zero(self, client):
        response = client.post("/api/calculate", json={"operation": "absolute", "a": 0, "b": 0})
        assert response.status_code == 200
        assert response.json["result"] == 0


class TestFactorialEndpoint:
    def test_factorial_normal(self, client):
        response = client.post("/api/calculate", json={"operation": "factorial", "a": 5, "b": 0})
        assert response.status_code == 200
        assert response.json["result"] == 120

    def test_factorial_zero(self, client):
        response = client.post("/api/calculate", json={"operation": "factorial", "a": 0, "b": 0})
        assert response.status_code == 200
        assert response.json["result"] == 1
```

---

## Bonus: Playwright E2E Test

Hocaın verdigi `tests/e2e/` klasoründeki testler calistirildi:

```bash
BASE_URL=http://127.0.0.1:5000 pytest tests/e2e/ -v --headed --slowmo=1000
```

31 test passed — Chromium tarayicisi acilarak form doldurma, buton tiklama,
sonuc dogrulama ve history kontrolu basariyla gerceklestirildi.

---

## Teslim Kontrol Listesi

- [x] `src/calculator.py` — 2 yeni metot eklendi (absolute, factorial)
- [x] `tests/unit/test_homework.py` — 10 yeni unit test yazildi
- [x] `tests/integration/test_homework_api.py` — 5 integration test yazildi
- [x] Tum testler geciyor (`pytest` → 224 passed)
- [x] Coverage %95+ (`pytest --cov=src` → %97.2)
- [x] `htmlcov/` klasoru olusturuldu
- [x] Bu sablon dolduruldu