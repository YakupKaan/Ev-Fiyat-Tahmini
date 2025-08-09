import pandas as pd
import numpy as np

# Veri setini yükle
veri_dosyasi = r"D:\ev_fiyat\elazig_ev_fiyatlari.csv"
df = pd.read_csv(veri_dosyasi)

# 1. Fiyat sütunundaki hataları temizleme
# Önce virgülleri kaldır
df['Fiyat'] = df['Fiyat'].str.replace(',', '', regex=False)
# Ardından metnin başındaki ilk sayı dizisini al
df['Fiyat'] = df['Fiyat'].str.extract('(\d+)', expand=False)
# Sayısal formata çevir
df['Fiyat'] = pd.to_numeric(df['Fiyat'], errors='coerce')

# 2. Net ve Brüt Metrekare sütunlarını temizleme
# Hatalı değerleri NaN olarak işaretle ve "m²" birimini kaldır
df['Net Metrekare'] = df['Net Metrekare'].str.replace(' m²', '', regex=False).replace('Bilinmiyor', np.nan)
df['Brüt Metrekare'] = df['Brüt Metrekare'].str.replace(' m²', '', regex=False).replace('Bilinmiyor', np.nan)

# NaN olarak işaretlenen değerler sayısal formata dönüştürülüyor
df['Net Metrekare'] = pd.to_numeric(df['Net Metrekare'], errors='coerce')
df['Brüt Metrekare'] = pd.to_numeric(df['Brüt Metrekare'], errors='coerce')

# 3. Eksik verileri kontrol etme
eksik_veri = df.isnull().sum()
print("Eksik Veri Sayısı:")
print(eksik_veri)

# 4. Hatalı "Fiyat" ve "Metrekare" verilerini görüntüleme
hatali_fiyat = df[df['Fiyat'].isnull()]
hatali_metrekare = df[df['Brüt Metrekare'].isnull() | df['Net Metrekare'].isnull()]

print("\nHatalı Fiyat Verileri:")
print(hatali_fiyat)

print("\nHatalı Metrekare Verileri:")
print(hatali_metrekare)

# 5. Temizlenmiş veri setini kontrol etme
print("\nTemizlenmiş Veri Setinin İlk 5 Satırı:")
print(df.head())

# 6. Gerekirse temizlenmiş veri setini kaydetme
temiz_dosya = r"D:\ev_fiyat\_temizlenmis_elazig_ev_fiyatlari.csv"
df.to_csv(temiz_dosya, index=False)
print(f"\nTemizlenmiş veri seti '{temiz_dosya}' konumuna kaydedildi.")
