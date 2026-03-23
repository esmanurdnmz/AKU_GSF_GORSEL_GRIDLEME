# 🎨 AKÜ GSF - Profesyonel Grid Aracı (Artist's Grid Assistant)

**Afyon Kocatepe Üniversitesi Güzel Sanatlar Fakültesi** öğrencileri ve hocaları için özel olarak geliştirilmiş, dijital görselleri fiziksel kağıt/tuval boyutlarına göre oranlayan, hassas kenar boşlukları (paspartu) bırakan ve üzerine özelleştirilebilir gridler (ızgara) ekleyen bir dijital çizim asistanıdır.

> *"Bir yazılım mühendisi adayı olarak, AKÜ GSF stüdyolarındaki sanatçıların gerçek bir problemini teknolojiyle çözmekten gurur duyuyorum. Proje, fakülte hocalarından tam not almıştır."* — Esmanur Dönmez

## 🚀 Canlı Siteye Git / Go to Live App
[https://gsf-cizim-asistani.streamlit.app/](https://gsf-cizim-asistani.streamlit.app/)

## ✨ Özellikler (Key Features)

* **Fiziksel Boyut Desteği:** 35x50, 50x70, 70x100 gibi tüm kağıt/tuval boyutlarını dikey veya yatay olarak destekler.
* **Hassas Marj Kontrolü:** Üst, alt, sağ ve sol kenar boşluklarını (Paspartu) cm cinsinden milimetrik olarak ayarlayabilme.
* **Akıllı Ortalama (Kusursuz Simetri):** Resim, belirlenen marjlar içindeki güvenli alanın tam merkezine simetrik olarak oturtulur (Eski kodlardaki asimetri sorunu giderilmiştir).
* **Renk Seçici (Color Picker):** Grid çizgilerini resmin tonuna göre istediğiniz renkte (kırmızı, siyah, beyaz vb.) ayarlayabilirsiniz.
* **RAM Koruması (DPI Optim):** Çok büyük kağıt boyutları girildiğinde sunucunun çökmesini önleyen otomatik çözünürlük optimizasyonu.

## 🛠 Kullanılan Teknolojiler (Tech Stack)

* **Dil:** Python 3.11
* **Görüntü İşleme:** OpenCV (`cv2`) & NumPy
* **Web Framework:** Streamlit
* **Dağıtım (Deployment):** Streamlit Cloud

---
*Hazırlayan: [Esmanur Dönmez]*
