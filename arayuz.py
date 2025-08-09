import streamlit as st
import pandas as pd
import joblib

# Modeli yükle
model_path = r"D:\ev_fiyat\ev_fiyat_tahmin_modeli.joblib"
model = joblib.load(model_path)

# Kategorik sütunlar için örnek seçenekler
district_options = [
    'Elazığ Merkez', 'Harput', 'Keban', 'Karakoçan'
]
heating_options = ['Kombi Dogalgaz', 'Merkezi Dogalgaz', 'Merkezi (Pay Olcer)', 'Soba', 'Isitma Yok']
building_age_options = ['0 (Yeni)', '1-5', '5-10', '11-15', '16-20', '21 Ve Uzeri']
usage_status_options = ['Boş', 'Mülk Sahibi Oturuyor', 'Kiracı Oturuyor']

# Sayfa başlığı
st.title("Ev Fiyat Tahmini Uygulaması")
st.write("Lütfen aşağıdaki bilgileri doldurun ve ev fiyatını tahmin edin.")

# Kullanıcıdan giriş al
with st.form("tahmin_formu"):
    st.header("Ev Özelliklerini Girin")
    
    # Sayısal girişler
    net_metrekare = st.number_input("Net Metrekare", min_value=50, max_value=500, value=100)
    brut_metrekare = st.number_input("Brut Metrekare", min_value=60, max_value=600, value=120)
    oda_sayisi = st.text_input("Oda Sayısı (Örn: 3+1)", "3+1")
    bulundugu_kat = st.text_input("Bulunduğu Kat (Örn: 3.Kat veya Düz Giriş)", "3.Kat")
    bina_kat_sayisi = st.number_input("Binanın Kat Sayısı", min_value=1, max_value=50, value=5)
    
    # Kategorik girişler
    bina_yasi = st.selectbox("Bina Yaşı", options=building_age_options)
    isinma_tipi = st.selectbox("Isınma Tipi", options=heating_options)
    kullanin_durumu = st.selectbox("Kullanım Durumu", options=usage_status_options)
    ilce = st.selectbox("İlçe Seçin", options=district_options)
    
    # Form butonu
    submitted = st.form_submit_button("Fiyat Tahmin Et")

# Tahmini Hesaplama
if submitted:
    # Giriş verilerini oluştur
    input_data = pd.DataFrame([{
    'Net Metrekare': net_metrekare,
    'Brut Metrekare': brut_metrekare,
    'Oda Sayisi': oda_sayisi,
    'Bulundugu Kat': bulundugu_kat,
    'Isitma Tipi': isinma_tipi,
    'Binanin Yasi': bina_yasi,
    'Binanin Kat Sayisi': bina_kat_sayisi,
    'Kullanim Durumu': kullanin_durumu,
    'Adres': ilce  # İlçeyi 'Adres' sütununa eşleştiriyoruz
}])

    
    # Tahmin yap
    try:
        prediction = model.predict(input_data)[0]
        st.success(f"Tahmini Ev Fiyatı: **{prediction:,.2f} TL**")
    except Exception as e:
        st.error("Bir hata oluştu. Model ve giriş verilerini kontrol edin!")
        st.text(f"Hata: {e}")
