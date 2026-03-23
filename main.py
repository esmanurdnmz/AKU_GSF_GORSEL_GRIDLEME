import streamlit as st
import cv2
import numpy as np


def web_icin_grid_olustur(img, kagit_eni_cm, kagit_boyu_cm, kare_boyutu_cm, m_ust, m_alt, m_sol, m_sag,
                          cizgi_rengi_bgr):
    # Çözünürlük ve RAM Koruması
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

    # Marginleri piksel cinsinden hesapla
    px_sol = int(m_sol * PCM)
    px_sag = int(m_sag * PCM)
    px_ust = int(m_ust * PCM)
    px_alt = int(m_alt * PCM)

    # Kullanıcı marginlerine göre çizim (güvenli) alanı
    guvenli_w_px = kagit_w_px - (px_sol + px_sag)
    guvenli_h_px = kagit_h_px - (px_ust + px_alt)

    # Hata Kontrolü
    if guvenli_w_px <= 0 or guvenli_h_px <= 0:
        st.error("Hata: Kenar boşluklarının toplamı kağıt/tuval boyutundan büyük olamaz!")
        return None

    # Resmi bozmadan küçült/büyült
    scale = min(guvenli_w_px / orig_w, guvenli_h_px / orig_h)
    new_w = max(1, int(orig_w * scale))
    new_h = max(1, int(orig_h * scale))

    resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

    # Artan boşluğu hesapla ve sağa/sola eşit dağıt (Kusursuz Ortalama)
    bosluk_x = (guvenli_w_px - new_w) // 2
    bosluk_y = (guvenli_h_px - new_h) // 2

    offset_x = px_sol + bosluk_x
    offset_y = px_ust + bosluk_y

    # Resmi kağıda yapıştır
    tuval[offset_y:offset_y + new_h, offset_x:offset_x + new_w] = resized_img

    kare_px = max(1, int(kare_boyutu_cm * PCM))

    ana_renk = cizgi_rengi_bgr  # Kullanıcının seçtiği renk
    golge_renk = (0, 0, 0) if ana_renk != (0, 0, 0) else (255, 255, 255)  # Siyah seçilirse gölge beyaz olsun
    ana_kalinlik = max(1, int(DPI / 100))
    golge_kalinlik = ana_kalinlik * 2 + 1

    # Grid çizimi
    for y in range(0, kagit_h_px, kare_px):
        cv2.line(tuval, (0, y), (kagit_w_px, y), golge_renk, golge_kalinlik)
        cv2.line(tuval, (0, y), (kagit_w_px, y), ana_renk, ana_kalinlik)

    for x in range(0, kagit_w_px, kare_px):
        cv2.line(tuval, (x, 0), (x, kagit_h_px), golge_renk, golge_kalinlik)
        cv2.line(tuval, (x, 0), (x, kagit_h_px), ana_renk, ana_kalinlik)

    return tuval


# --- WEB ARAYÜZÜ ---
st.set_page_config(page_title="Sanatçı Gridleyici", layout="centered")

st.title("🎨 Profesyonel Grid Aracı")
st.write("Görselinizi yükleyin, kağıt/tuval boyutunuzu girin ve gridli halini indirin.")

# Görsel yükleme
yuklenen_dosya = st.file_uploader("Referans Görselinizi Yükleyin (JPG/PNG)", type=['jpg', 'jpeg', 'png'])

# Kağıt/Tuval boyutları
col1, col2 = st.columns(2)
with col1:
    kenar_a = st.number_input("1. Kağıt/Tuval Kenarı (cm)", min_value=1.0, value=70.0, step=1.0)
with col2:
    kenar_b = st.number_input("2. Kağıt/Tuval Kenarı (cm)", min_value=1.0, value=100.0, step=1.0)

yonelim = st.radio("Kağıt/Tuval Yönü", ("Dikey", "Yatay"), horizontal=True)

# Grid Ayarları (Boyut ve Renk)
col_grid1, col_grid2 = st.columns(2)
with col_grid1:
    kare_boyutu = st.number_input("Grid Kare Boyutu (cm)", min_value=0.5, value=3.0, step=0.5)
with col_grid2:
    # Kullanıcıdan HEX formatında renk alıp OpenCV'nin istediği BGR formatına çeviriyoruz
    secilen_renk_hex = st.color_picker(" Grid Çizgi Rengi", "#FF0000")
    hex_kodu = secilen_renk_hex.lstrip('#')
    rgb = tuple(int(hex_kodu[i:i + 2], 16) for i in (0, 2, 4))
    cizgi_rengi_bgr = (rgb[2], rgb[1], rgb[0])  # OpenCV için BGR sıralaması

# Margin inputları
st.subheader(" Kenar Boşlukları (cm)")

col3, col4 = st.columns(2)
with col3:
    m_ust = st.number_input("Üst Boşluk", min_value=0.0, value=5.0, step=0.5)
    m_alt = st.number_input("Alt Boşluk", min_value=0.0, value=5.0, step=0.5)
with col4:
    m_sol = st.number_input("Sol Boşluk", min_value=0.0, value=10.0, step=0.5)
    m_sag = st.number_input("Sağ Boşluk", min_value=0.0, value=10.0, step=0.5)

# İşlem
if yuklenen_dosya is not None:
    st.image(yuklenen_dosya, caption="Orijinal Görsel", use_container_width=True)

    if st.button("Grid Oluştur", type="primary"):
        with st.spinner("İşleniyor..."):

            file_bytes = np.asarray(bytearray(yuklenen_dosya.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, 1)

            if yonelim == "Dikey":
                eni = min(kenar_a, kenar_b)
                boyu = max(kenar_a, kenar_b)
            else:
                eni = max(kenar_a, kenar_b)
                boyu = min(kenar_a, kenar_b)

            sonuc = web_icin_grid_olustur(
                img, eni, boyu, kare_boyutu,
                m_ust, m_alt, m_sol, m_sag, cizgi_rengi_bgr
            )

            if sonuc is not None:
                sonuc_rgb = cv2.cvtColor(sonuc, cv2.COLOR_BGR2RGB)

                st.success("Hazır!")
                st.image(sonuc_rgb, caption="Gridli Görsel", use_container_width=True)

                is_success, buffer = cv2.imencode(".jpg", sonuc)
                st.download_button(
                    label="📥 Görseli İndir",
                    data=buffer.tobytes(),
                    file_name="gridli_sanat_referansi.jpg",
                    mime="image/jpeg"
                )

# --- GELİŞTİRİCİ KARTI (FOOTER) ---
st.markdown("---")
col_img, col_text = st.columns([1, 6])

with col_img:
    # GitHub profil resmini otomatik çeker
    st.image("https://github.com/esmanurdnmz.png", width=70)

with col_text:
    st.markdown("**Geliştirici:** Esmanur Dönmez")
    st.markdown(
        "[🔗 LinkedIn Profilim](https://linkedin.com/in/esmanurdonmez) | [💻 GitHub Profilim](https://github.com/esmanurdnmz)")
    st.caption("Bu araç AKÜ GSF öğrencileri için hazırlanmıştır.")