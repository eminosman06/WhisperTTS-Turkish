# Whisper Altyazı Oluşturucu

OpenAI Whisper modelini kullanarak video ve ses dosyalarından otomatik SRT altyazı oluşturan Windows uygulaması.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Özellikler

- ✅ **Whisper Model Seçimi**: tiny, base, small, medium, large, large-v2, large-v3
- ✅ **Çoklu Dil Desteği**: Türkçe, İngilizce ve 10+ dil
- ✅ **Otomatik Dil Algılama**: Dili otomatik algılayabilir
- ✅ **SRT Çıktısı**: DaVinci Resolve uyumlu zaman damgalı altyazı
- ✅ **Kullanıcı Dostu GUI**: Modern tkinter arayüzü
- ✅ **Video & Ses Desteği**: MP4, MKV, AVI, MP3, WAV ve daha fazlası

## 📋 Gereksinimler

- Python 3.10 veya üzeri
- FFmpeg (video işleme için)
- CUDA destekli GPU (opsiyonel, hızlı işlem için)

## 🚀 Kurulum

### 1. Depoyu klonlayın veya indirin

```bash
cd whisperAltyazıEkleme
```

### 2. Sanal ortam oluşturun (önerilir)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

### 4. FFmpeg yükleyin

**Windows (winget ile):**
```bash
winget install FFmpeg
```

**Manuel yükleme:**
1. https://ffmpeg.org/download.html adresinden indirin
2. Bir klasöre çıkarın (örn: `C:\ffmpeg`)
3. `C:\ffmpeg\bin` klasörünü sistem PATH'ine ekleyin

## 💻 Kullanım

### GUI Uygulaması

```bash
python main.py
```

### Programatik Kullanım

```python
from transcriber import WhisperTranscriber
from srt_generator import save_srt_file

# Transcriber oluştur
transcriber = WhisperTranscriber()

# Model yükle
transcriber.load_model("base")

# Transkripsiyon yap
result = transcriber.transcribe("video.mp4", language="tr")

# SRT dosyası kaydet
save_srt_file(result["segments"], "video.srt")
```

## 📊 Model Karşılaştırması

| Model     | Parametre | VRAM   | Hız       | Kalite    |
|-----------|-----------|--------|-----------|-----------|
| tiny      | 39M       | ~1GB   | En hızlı  | Düşük     |
| base      | 74M       | ~1GB   | Hızlı     | Orta      |
| small     | 244M      | ~2GB   | Orta      | İyi       |
| medium    | 769M      | ~5GB   | Yavaş     | Çok İyi   |
| large     | 1550M     | ~10GB  | En yavaş  | En İyi    |
| large-v2  | 1550M     | ~10GB  | En yavaş  | En İyi    |
| large-v3  | 1550M     | ~10GB  | En yavaş  | En İyi    |

> **Not**: `.en` sonekli modeller sadece İngilizce için optimize edilmiştir.

## 🎬 DaVinci Resolve'da Kullanım

1. Uygulamayı çalıştırın ve SRT dosyası oluşturun
2. DaVinci Resolve'u açın
3. File → Import → Subtitle seçin
4. Oluşturulan .srt dosyasını seçin
5. Timeline'a sürükleyin

## 📁 Proje Yapısı

```
whisperAltyazıEkleme/
├── main.py              # Ana uygulama başlatıcı
├── gui.py               # GUI arayüzü
├── transcriber.py       # Whisper transkripsiyon modülü
├── srt_generator.py     # SRT dosya oluşturucu
├── requirements.txt     # Python bağımlılıkları
├── Planlama.md          # Proje planı
└── README.md            # Bu dosya
```

## ⚠️ Bilinen Sorunlar

- İlk model yüklemesi internet bağlantısı gerektirir
- Large modeller yüksek VRAM gerektirir
- Çok uzun videolarda bellek sorunu olabilir

## � Model Cache Bilgisi

Whisper modelleri ilk kullanımda indirilir ve şu konumda önbelleğe alınır:

```
C:\Users\<KullanıcıAdı>\.cache\whisper\
```

| Model     | Dosya Boyutu |
|-----------|--------------|
| tiny.pt   | ~75 MB       |
| base.pt   | ~145 MB      |
| small.pt  | ~465 MB      |
| medium.pt | ~1.5 GB      |
| large.pt  | ~3 GB        |

> **Not**: Modeller bir kez indirilir ve sonraki kullanımlarda cache'den yüklenir. Tekrar indirme yapılmaz.

## 🖥️ Masaüstü Uygulaması Olarak Kullanım

Uygulamayı her seferinde terminal açmadan başlatmak için:

### Kısayol Oluşturma (Windows)
1. Masaüstünde sağ tık → Yeni → Kısayol
2. Konum olarak şunu girin:
   ```
   C:\Users\<KullanıcıAdı>\whisperAltyazıEkleme\.venv\Scripts\pythonw.exe C:\Users\<KullanıcıAdı>\whisperAltyazıEkleme\main.py
   ```
3. İsim verin: "Whisper Altyazı"

### Batch Dosyası ile Başlatma
`baslat.bat` dosyası oluşturun:
```batch
@echo off
cd /d "C:\Users\<KullanıcıAdı>\whisperAltyazıEkleme"
call .venv\Scripts\activate
pythonw main.py
```

## �📝 Lisans

MIT License

## 🙏 Teşekkürler

- [OpenAI Whisper](https://github.com/openai/whisper)
- [FFmpeg](https://ffmpeg.org/)
