import streamlit as st
import cv2
import numpy as np


def web_icin_grid_olustur(img, kagit_eni_cm, kagit_boyu_cm, kare_boyutu_cm):
    # Çözünürlük ve RAM Koruması (Önceki mantık)
    uzun_kenar_cm = max(kagit_eni_cm, kagit_boyu_cm)
    maksimum_piksel = 8000
    teorik_piksel = (uzun_kenar_cm / 2.54) * 300

    if teorik_piksel > maksimum_piksel:
        DPI = (maksimum_piksel * 2.54) / uzun_kenar_cm
    else:
        DPI = 300

    PCM = DPI / 2.54

    kagit_w_px = int(kagit_eni_cm * PCM)
    kagit_h_px = int(kagit_boyu_cm * PCM)

    tuval = np.full((kagit_h_px, kagit_w_px, 3), 255, dtype=np.uint8)
    orig_h, orig_w = img.shape[:2]

    otomatik_bosluk_cm = min(kagit_eni_cm, kagit_boyu_cm) * 0.07
    guvenli_w_px = int((kagit_eni_cm - (2 * otomatik_bosluk_cm)) * PCM)
    guvenli_h_px = int((kagit_boyu_cm - (2 * otomatik_bosluk_cm)) * PCM)

    scale = min(guvenli_w_px / orig_w, guvenli_h_px / orig_h)
    new_w = max(1, int(orig_w * scale))
    new_h = max(1, int(orig_h * scale))
    resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

    offset_x = (kagit_w_px - new_w) // 2
    offset_y = (kagit_h_px - new_h) // 2
    tuval[offset_y:offset_y + new_h, offset_x:offset_x + new_w] = resized_img

    kare_px = max(1, int(kare_boyutu_cm * PCM))

    ana_renk = (0, 0, 255)
    golge_renk = (0, 0, 0)
    ana_kalinlik = max(1, int(DPI / 100))
    golge_kalinlik = ana_kalinlik * 2 + 1

    # Gridleri Çiz
    for y in range(0, kagit_h_px, kare_px):
        cv2.line(tuval, (0, y), (kagit_w_px, y), golge_renk, golge_kalinlik)
        cv2.line(tuval, (0, y), (kagit_w_px, y), ana_renk, ana_kalinlik)

    for x in range(0, kagit_w_px, kare_px):
        cv2.line(tuval, (x, 0), (x, kagit_h_px), golge_renk, golge_kalinlik)
        cv2.line(tuval, (x, 0), (x, kagit_h_px), ana_renk, ana_kalinlik)

    return tuval  # Dosyayı kaydetmiyoruz, web sitesine geri gönderiyoruz!


# --- WEB ARAYÜZÜ TASARIMI ---
st.set_page_config(page_title="Sanatçı Gridleyici", layout="centered")

st.title("🎨 Profesyonel Grid Aracı")
st.write("Görselinizi yükleyin, kağıt boyutunuzu girin ve anında çizim gridinizi indirin.")

# 1. Dosya Yükleme Alanı
yuklenen_dosya = st.file_uploader("Referans Görselinizi Yüleyin (JPG/PNG)", type=['jpg', 'jpeg', 'png'])

# 2. Kullanıcı Girdileri (Arayüz Elemanları)
col1, col2 = st.columns(2)
with col1:
    kenar_a = st.number_input("1. Kenar Uzunluğu (cm)", min_value=1.0, value=70.0, step=1.0)
with col2:
    kenar_b = st.number_input("2. Kenar Uzunluğu (cm)", min_value=1.0, value=100.0, step=1.0)

yonelim = st.radio("Kağıt Yönü", ("Dikey", "Yatay"), horizontal=True)
kare_boyutu = st.number_input("Grid Kare Boyutu (cm)", min_value=0.5, value=3.0, step=0.5)

# 3. İşleme Butonu
if yuklenen_dosya is not None:
    # Görseli web arayüzünde göster
    st.image(yuklenen_dosya, caption="Yüklenen Orijinal Görsel", use_container_width=True)

    if st.button("Grid Oluştur", type="primary"):
        with st.spinner("Görseliniz devasa bir tuvale işleniyor, lütfen bekleyin..."):

            # Yüklenen dosyayı OpenCV'nin okuyabileceği formata çevir (Dosya isminden bağımsızlaştık!)
            file_bytes = np.asarray(bytearray(yuklenen_dosya.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, 1)

            # Kağıt yönünü ayarla
            if yonelim == "Dikey":
                eni = min(kenar_a, kenar_b)
                boyu = max(kenar_a, kenar_b)
            else:
                eni = max(kenar_a, kenar_b)
                boyu = min(kenar_a, kenar_b)

            # Fonksiyona gönder ve sonucu al
            sonuc_gorseli = web_icin_grid_olustur(img, eni, boyu, kare_boyutu)

            # OpenCV formatını (BGR), Web formatına (RGB) çevir
            sonuc_rgb = cv2.cvtColor(sonuc_gorseli, cv2.COLOR_BGR2RGB)

            st.success("İşlem Başarılı! Aşağıdan indirebilirsiniz.")

            # Sonucu Ekranda Göster
            st.image(sonuc_rgb, caption="Gridli Çizim Referansı", use_container_width=True)

            # İndirme Butonu Oluştur
            is_success, buffer = cv2.imencode(".jpg", sonuc_gorseli)
            st.download_button(
                label="📥 Gridli Görseli İndir",
                data=buffer.tobytes(),
                file_name="gridli_referans.jpg",
                mime="image/jpeg"
            )