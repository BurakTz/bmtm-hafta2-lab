# 📝 BMTM Hafta 2 — Odev Cevap Sablonu

**Ogrenci Adi:** _______________  
**Ogrenci No:** _______________  
**Tarih:** _______________

---

## Bolum 1: Calculator Genisletme

### 1.1 Eklenen Metotlar

```python
def absolute(self, number):
    """Bir sayinin mutlak degerini dondurur."""
    # TODO: Implementasyonu yazin
    pass

def factorial(self, n):
    """n! (n faktoriyel) hesaplar.
    
    Raises:
        ValueError: n negatif oldugunda
        TypeError: n tam sayi olmadiginda
    """
    # TODO: Implementasyonu yazin
    pass
```

### 1.2 Yazilan Unit Testler

`tests/unit/test_homework.py` — en az 10 test:

```python
# TODO: Testlerinizi buraya yazin
# Ipuclari:
# - absolute: pozitif, negatif, sifir, float
# - factorial: 0!, 1!, 5!, negatif hata, float hata
# - Edge case'leri unutmayin!
```

---

## Bolum 2: Coverage Raporu

| Dosya | Stmts | Miss | Cover |
|-------|-------|------|-------|
| calculator.py | ? | ? | ?% |
| **TOTAL** | ? | ? | ?% |

**Hedef: %95+** ☐ Ulasildi / ☐ Ulasilamadi

---

## Bolum 3: Integration Test

### 3.1 app.py'ye Eklenen Endpoint'ler

```python
# TODO: absolute ve factorial icin endpoint'leri yazin
```

### 3.2 Yazilan Integration Testler

`tests/integration/test_homework_api.py` — en az 5 test

---

## Teslim Kontrol Listesi

- [ ] `src/calculator.py` — 2 yeni metot eklendi
- [ ] `tests/unit/test_homework.py` — En az 10 yeni unit test
- [ ] `tests/integration/test_homework_api.py` — En az 5 integration test
- [ ] Tum testler geciyor (`pytest` → all passed)
- [ ] Coverage %95+ (`pytest --cov=src`)
- [ ] `htmlcov/` klasoru olusturuldu
- [ ] Bu sablon dolduruldu
