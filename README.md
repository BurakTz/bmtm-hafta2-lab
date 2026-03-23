# 🧪 BMTM Hafta 2 — Test Otomasyonu Lab Projesi


**Bulut Mimarilerinde Test Muhendisligi**  
Busra Ayaksiz | 2025–26 Bahar Donemi | Marmara Universitesi

---

## 📁 Proje Yapisi

```
bmtm-hafta2-lab/
├── src/
│   ├── __init__.py
│   ├── calculator.py              # Test edilecek sinif
│   ├── app.py                     # Flask REST API (integration testler icin)
│   └── templates/
│       └── index.html             # Web UI (E2E testler icin)
├── tests/
│   ├── conftest.py                # Paylasilan fixture'lar
│   ├── unit/                      # ── Unit Testler ──
│   │   ├── test_basics.py         # Lab 1: Ilk unit testler
│   │   ├── test_edge_cases.py     # Lab 1: Sinir durum testleri
│   │   ├── test_fixtures.py       # Lab 2: Fixture kullanimi
│   │   ├── test_parametrize.py    # Lab 2: Parametrize
│   │   ├── test_coverage.py       # Lab 3: Coverage odakli testler
│   │   └── test_mocking.py       # Lab 6: Mock/Stub/Spy testleri
│   ├── integration/               # ── Integration Testler ──
│   │   ├── conftest.py            # Flask test client fixture
│   │   └── test_api.py            # Lab 4: API integration testleri
│   └── e2e/                       # ── E2E Testler ──
│       ├── pages/
│       │   └── calculator_page.py # Lab 5: Page Object Model sinifi
│       ├── test_calculator_ui.py  # Lab 5: Playwright UI testleri
│       └── test_calculator_pom.py # Lab 5: POM kullanan E2E testler
├── docs/
│   └── lab_cevaplari.md           # Odev teslim sablonu
├── pytest.ini
├── setup.cfg
├── requirements.txt
└── README.md
```

---

## 🚀 Kurulum (5 dk)

### 1. Python Kontrol
```bash
python3 --version   # Python 3.10+ gerekli
```

### 2. Virtual Environment (Onerilen)
```bash
cd bmtm-hafta2-lab
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### 3. Bagimliliklari Kur
```bash
pip install -r requirements.txt
```

### 4. Playwright Tarayicilarini Kur (E2E icin)
```bash
playwright install chromium
```

### 5. Test Et
```bash
pytest tests/unit/ tests/integration/
```

Tum testler geciyorsa ortam hazir! ✅

---

## 🔬 Lab 1: Ilk Unit Testler (40 dk)

**Dosyalar:** `tests/unit/test_basics.py`, `tests/unit/test_edge_cases.py`

### Hedefler
- Ilk pytest testini yazma ve calistirma
- `assert` ve `pytest.raises` kullanimi
- AAA (Arrange-Act-Assert) pattern
- Edge case (sinir durum) kavrami

### Adimlar

```bash
# Kaynak kodu incele
cat src/calculator.py

# Temel testleri calistir
pytest tests/unit/test_basics.py -v

# Edge case testlerini calistir
pytest tests/unit/test_edge_cases.py -v
```

### 🎯 Kendiniz Deneyin
`test_basics.py` dosyasina su testleri ekleyin:
1. `test_subtract_float` — Float cikarma
2. `test_multiply_by_one` — 1 ile carpmanin etkisizligi
3. `test_power_large_exponent` — 2^20 = 1048576 kontrolu

---

## 🔧 Lab 2: Fixture & Parametrize (40 dk)

### Lab 2a: Fixture Kullanimi
**Dosya:** `tests/unit/test_fixtures.py`

```bash
# conftest.py'deki fixture'lari incele
cat tests/conftest.py

# Fixture testlerini calistir
pytest tests/unit/test_fixtures.py -v
```

| Fixture | Aciklama | Scope |
|---------|----------|-------|
| `calc` | Calculator instance | function |
| `sample_pairs` | Sayi ciftleri + beklenen sonuclar | function |
| `number_lists` | Ortalama icin listeler | function |
| `course_info` | Ders bilgisi | session |

### Lab 2b: Parametrize
**Dosya:** `tests/unit/test_parametrize.py`

```bash
pytest tests/unit/test_parametrize.py -v
```

### 🎯 Kendiniz Deneyin
1. `conftest.py`'ye yeni bir fixture ekleyin
2. `test_parametrize.py`'ye `pytest.param` ile ID'li test ekleyin

---

## 📊 Lab 3: Test Coverage (30 dk)

**Dosya:** `tests/unit/test_coverage.py`

### Adim 1 — Coverage Olc
```bash
pytest tests/unit/ --cov=src --cov-report=term-missing
```

### Adim 2 — HTML Rapor
```bash
pytest tests/unit/ --cov=src --cov-report=html
open htmlcov/index.html
```

### Adim 3 — Minimum Esik
```bash
pytest tests/unit/ --cov=src --cov-fail-under=90
```

HTML raporda: **Yesil** = test edildi, **Kirmizi** = test edilmedi, **Sari** = kismi kapsam

---

## 🌐 Lab 4: Integration Testleri (30 dk)

**Dosya:** `tests/integration/test_api.py`

### Unit Test vs Integration Test

```
Unit Test:
    calc = Calculator()
    assert calc.add(2, 3) == 5
    → Sadece Calculator sinifi test edilir

Integration Test:
    response = client.post("/api/calculate", json={"operation": "add", "a": 2, "b": 3})
    assert response.status_code == 200
    assert response.json["result"] == 5
    → Flask routing + JSON parsing + Calculator + response birlikte test edilir
```

### Calistir
```bash
pytest tests/integration/ -v
```

### API Endpoints

| Method | Endpoint | Aciklama |
|--------|----------|----------|
| GET | `/api/health` | Saglik kontrolu |
| POST | `/api/calculate` | Hesaplama yap |
| GET | `/api/history` | Islem gecmisi |
| DELETE | `/api/history` | Gecmisi temizle |

### Request Ornegi
```json
POST /api/calculate
{
  "operation": "add",
  "a": 10,
  "b": 5
}
→ {"result": 15, "operation": "add"}
```

### 🎯 Kendiniz Deneyin
1. `test_api.py`'ye yeni bir hata senaryosu ekleyin
2. Birden fazla endpoint kullanan bir workflow testi yazin

---

## 🎭 Lab 5: Playwright ile E2E Test (20 dk)

**Dosya:** `tests/e2e/test_calculator_ui.py`

### Test Piramidinde E2E'nin Yeri

```
        /  E2E  \         ← Yavas, az sayida, kullanici akislari
       / Integr. \        ← Orta hiz, API & bilesen testleri
      /   Unit    \       ← Hizli, cok sayida, izole
```

### Kurulum ve Calistirma

> **macOS Notu:** Port 5000 AirPlay Receiver tarafindan kullaniliyor olabilir.
> Bu yuzden server'i **port 5050**'de baslatiyoruz.
> Alternatif olarak AirPlay Receiver'i kapatabilirsiniz:
> System Settings > General > AirDrop & Handoff > AirPlay Receiver → Kapat

```bash
# Adim 1: Flask server'i baslat (ayri terminal)
cd src && python3 -c "from app import app; app.run(port=5050)"

# Adim 2: Tarayicida arayuzu ac (opsiyonel, gormek icin)
open http://localhost:5050

# Adim 3: E2E testleri calistir (baska terminal)
BASE_URL=http://localhost:5050 pytest tests/e2e/ -v

# Adim 4: Tarayiciyi acik gorerek calistir (DEMO icin onerilen!)
BASE_URL=http://localhost:5050 pytest tests/e2e/ -v --headed --slowmo=2000
```

**`--headed`** Chromium tarayicisini acar, **`--slowmo=2000`** her adimi 2 saniye bekletir.
Boylece Playwright'in input doldurmesini, butona tiklamasini ve sonuc kontrolunu canli izleyebilirsiniz.

### Playwright Temelleri

```python
# Sayfaya git
page.goto("http://localhost:5000")

# Element bul ve tikla (data-testid ile)
page.click('[data-testid="calculate-btn"]')

# Input'a deger yaz
page.fill('[data-testid="input-a"]', "10")

# Dropdown sec
page.select_option('[data-testid="operation-select"]', "multiply")

# Assertion — element gorunur mu?
expect(page.locator('[data-testid="result-value"]')).to_be_visible()

# Assertion — metin dogru mu?
expect(page.locator('[data-testid="result-value"]')).to_have_text("15")
```

### Neden `data-testid` Kullaniyoruz?
CSS class ve ID'ler degisebilir, ama `data-testid` attribute'lari
test icin ozel olarak eklenir ve daha kararlidir.

### Page Object Model (POM) ile E2E Test

Page Object Model, UI testlerinde **selector'leri ve sayfa etkilesimlerini**
tek bir sinifta toplayan bir tasarim kalıbidir. Boylece UI degistiginde
sadece Page Object guncellenir, testler ayni kalir.

**POM olmadan** (`test_calculator_ui.py`):
```python
page.fill('[data-testid="input-a"]', "10")
page.fill('[data-testid="input-b"]', "5")
page.select_option('[data-testid="operation-select"]', "add")
page.click('[data-testid="calculate-btn"]')
expect(page.locator('[data-testid="result-value"]')).to_have_text("15")
```

**POM ile** (`test_calculator_pom.py`):
```python
calc.set_number_a("10")
calc.set_number_b("5")
calc.set_operation("add")
calc.calculate()
calc.expect_result("15")
```

**Neden POM?**
- Selector'ler **tek yerde** — UI degisirse sadece `CalculatorPage` guncellenir
- Testler **daha okunakli** — ne yapildigini anlatir, nasil yapildigini gizler
- **Kod tekrari azalir** — ayni selector 10 testte tekrarlanmaz

**Dosyalar:**
- `tests/e2e/pages/calculator_page.py` — Page Object sinifi
- `tests/e2e/test_calculator_pom.py` — POM kullanan testler

```bash
# POM testlerini calistir
BASE_URL=http://localhost:5050 pytest tests/e2e/test_calculator_pom.py -v

# Kiyaslama: POM'suz testler
BASE_URL=http://localhost:5050 pytest tests/e2e/test_calculator_ui.py -v

# Tum E2E testler birlikte
BASE_URL=http://localhost:5050 pytest tests/e2e/ -v
```

### 🎯 Kendiniz Deneyin
1. Yeni bir islem turu icin E2E test ekleyin
2. `--headed` modda testlerin tarayicida calismasini izleyin

---

## 🎭 Lab 6: Test Doubles — Mock, Stub, Spy (40 dk)

**Dosya:** `tests/unit/test_mocking.py`

### Hedefler
- `unittest.mock.Mock` ve `MagicMock` kullanimini ogrenme
- Mock, Stub ve Spy arasindaki farklari anlama
- `assert_called_once_with`, `call_count` ile cagirim dogrulama
- `side_effect` ile hata simulasyonu
- `@patch` dekoratoru kullanimi

### Test Double Turleri

```
Mock:   Cagirim dogrulamasi yapar → "log() cagrildi mi?"
Stub:   Sabit deger dondurur      → "log() her zaman True donsun"
Spy:    Gercek davranis + kayit   → "log() calisti ve 3 kez cagirildi"
```

### Adimlar

```bash
# 1. CalculationLogger sinifini incele
cat src/calculator.py

# 2. Mock testlerini calistir
pytest tests/unit/test_mocking.py -v

# 3. Sadece belirli bir test sinifini calistir
pytest tests/unit/test_mocking.py::TestMockLogger -v
pytest tests/unit/test_mocking.py::TestStubLogger -v
pytest tests/unit/test_mocking.py::TestSpyBehavior -v
pytest tests/unit/test_mocking.py::TestSideEffect -v
```

### Temel Kavramlar

```python
from unittest.mock import Mock, patch, call

# Mock olustur
mock_logger = Mock()

# Cagirim dogrula
mock_logger.log.assert_called_once_with("add", (1, 2), 3)

# Cagri sayisi
assert mock_logger.log.call_count == 3

# Stub: sabit deger dondur
mock_logger.log.return_value = True

# side_effect: hata firlatma
mock_logger.log.side_effect = RuntimeError("Hata!")

# Cagri sirasi kontrolu
mock_logger.log.assert_has_calls([
    call("add", (1, 2), 3),
    call("multiply", (2, 3), 6),
], any_order=False)
```

### 🎯 Kendiniz Deneyin
1. `TestSideEffect`'teki ilk testi gecirmek icin `Calculator._log_operation`'a `try/except` ekleyin
2. `percentage()` ve `average()` icin yeni Mock testleri yazin
3. `MagicMock` kullanarak logger'in context manager gibi davranmasini saglayin

---

## 📝 Odev

### Zorunlu (Teslim: Gelecek Hafta)

1. **Calculator Genisletme**
   - `src/calculator.py`'ye 2 yeni metot ekleyin:
     - `absolute(number)` → Mutlak deger
     - `factorial(n)` → Faktoriyel (n >= 0 kontrolu ile)
   - En az **10 yeni unit test** yazin (edge case dahil)

2. **Coverage Hedefi**
   - Tum testlerle `%95+` coverage elde edin
   - HTML coverage raporu olusturun

3. **Integration Test**
   - Yeni metotlar icin `app.py`'ye endpoint ekleyin
   - En az **5 integration test** yazin

### Bonus (Opsiyonel)
- Playwright ile yeni islemler icin E2E test yazin
- `pytest-html` ile HTML test raporu olusturun
- `@pytest.mark.slow` marker'i ile yavas testleri isaretleyin

---

## 📚 Faydali Komutlar

```bash
# Tum testleri calistir (E2E haric)
pytest tests/unit/ tests/integration/

# Sadece unit testler
pytest tests/unit/ -v

# Sadece integration testler
pytest tests/integration/ -v

# Sadece E2E testler (Flask server gerekli)
pytest tests/e2e/ -v --headed

# Belirli test sinifi
pytest tests/unit/test_basics.py::TestAdd -v

# Keyword ile filtrele
pytest -k "divide" -v

# Ilk hatada dur
pytest -x

# Coverage
pytest tests/unit/ tests/integration/ --cov=src --cov-report=term-missing

# HTML coverage raporu
pytest tests/unit/ tests/integration/ --cov=src --cov-report=html
```

---

## 🔗 Kaynaklar

- [Pytest Dokumantasyonu](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [Flask Testing](https://flask.palletsprojects.com/en/3.0.x/testing/)
- [Playwright for Python](https://playwright.dev/python/)

---

*Busra Ayaksiz — Bulut Mimarilerinde Test Muhendisligi — 2025-26 Bahar*

Burak Tuzcu
