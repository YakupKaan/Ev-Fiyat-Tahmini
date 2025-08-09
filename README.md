# Elazığ Ev Fiyat Tahmini

Bu proje, Elazığ ilinde satılık konutların özelliklerinden **fiyat tahmini** yapan bir makine öğrenmesi modeli ve bu modeli kullanıcıya sunan **Streamlit arayüzünden** oluşur. Ayrıca ham verilerin temizlenmesi için bir betik ve proje sunum dosyası da yer alır.

---

## Proje İçeriği

- **`arayuz.py`** — Streamlit tabanlı web arayüzü (kullanıcı formu + tahmin sonucu).
- **`ev_fiyat.py`** — Ham CSV verilerini temizleyen Python betiği.
- **`elazig_ev_fiyatlari.csv`** — Ham veri dosyası.
- **`ev_fiyat_tahmin_modeli.joblib`** — Eğitilmiş `RandomForestRegressor` modelini içeren `scikit-learn` Pipeline.
- **`veri madenciliği sunumu.pptx`** — Projenin veri toplama, model eğitimi ve arayüz oluşturma sürecini anlatan sunum.

---

## Kurulum ve Çalıştırma

### 1️⃣ Ortam Kurulumu
```bash
# Sanal ortam oluştur (opsiyonel)
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Gerekli paketleri yükle
pip install -U pip
pip install streamlit pandas numpy scikit-learn joblib
```

---

### 2️⃣ Dosya Yapısı (Önerilen)
```
proje_kok/
├─ arayuz.py
├─ ev_fiyat.py
├─ data/
│  └─ elazig_ev_fiyatlari.csv
├─ models/
│  └─ ev_fiyat_tahmin_modeli.joblib
└─ README.md
```

---

### 3️⃣ Model Yolunu Düzenle
`arayuz.py` içinde model yolunu kendi dizinine göre değiştir:
```python
model_path = "models/ev_fiyat_tahmin_modeli.joblib"
```

---

### 4️⃣ Streamlit Arayüzünü Çalıştır
```bash
streamlit run arayuz.py
```
Tarayıcı otomatik açılmazsa terminalde yazan URL'yi (`http://localhost:8501`) ziyaret et.

---

## Veri Temizleme (ev_fiyat.py)

**Amaç:**  
Ham CSV verisindeki fiyat, metrekare vb. sütunları temizlemek, eksik/hatalı değerleri işaretlemek ve düzenli bir formatta yeni CSV olarak kaydetmek.

**Özellikler:**
- `Fiyat` sütunundaki virgüller ve gereksiz karakterler kaldırılır, sayıya dönüştürülür.
- `Net Metrekare` ve `Brüt Metrekare` değerlerinden `m²` eki silinir, bilinmeyenler `NaN` yapılır.
- Eksik veriler raporlanır.
- Temiz veri `_temizlenmis_` ön eki ile yeni CSV’ye kaydedilir.

**Çalıştırma:**
```bash
python ev_fiyat.py
```

---

## Model Özeti

Model, `RandomForestRegressor` tabanlıdır ve bir **Pipeline** içerisinde şu adımları uygular:
- Sayısal özelliklerde (`Net/Brüt Metrekare`, `Bina Kat Sayısı`) **SimpleImputer** + **StandardScaler**.
- Kategorik özelliklerde (`Oda Sayısı`, `Bulunduğu Kat`, `Bina Yaşı`, `Isıtma Tipi`, `Kullanım Durumu`, `Adres`) **OneHotEncoder**.
- `RandomForestRegressor` ile regresyon.

Eğitim sonucu: **Test R² skoru ≈ 0.79**.

---

## Streamlit Arayüzü

Kullanıcıdan alınan veriler:
- Net Metrekare
- Brüt Metrekare
- Oda Sayısı
- Bulunduğu Kat
- Bina Kat Sayısı
- Bina Yaşı
- Isıtma Tipi
- Kullanım Durumu
- İlçe (Adres)

Girilen veriler `pandas.DataFrame` formatında modele verilir ve tahmini fiyat TL olarak gösterilir.

---

## Sık Karşılaşılan Sorunlar

- **`FileNotFoundError: ev_fiyat_tahmin_modeli.joblib`**
  → Model yolunun doğru olduğundan emin ol.
- **Özellik sayısı/isim hataları**
  → Eğitimde kullanılan sütun isimleri ile arayüzdeki girdi isimleri aynı olmalı.
- **scikit-learn sürüm uyumsuzluğu**
  → Modelin eğitildiği sürümü kur:  
    `pip install scikit-learn==<sürüm>`

---

## Lisans ve Uyarılar
Bu proje eğitim amaçlıdır. Üçüncü taraf veri kaynaklarının (ör. Emlakjet) kullanım şartlarına uyum sağlamak kullanıcının sorumluluğundadır.

---
