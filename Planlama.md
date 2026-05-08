# Whisper Altyazı Ekleme Uygulaması

## Proje Özeti
OpenAI Whisper modelini lokal olarak kullanarak video dosyalarından otomatik altyazı oluşturan Windows uygulaması.

## Özellikler
- ✅ Whisper model seçimi (tiny, base, small, medium, large, large-v2, large-v3)
- ✅ Video/Ses dosyası yükleme
- ✅ SRT formatında zaman damgalı altyazı çıktısı
- ✅ DaVinci Resolve uyumlu dosya formatı
- ✅ Türkçe ve çoklu dil desteği
- ✅ Kullanıcı dostu GUI arayüzü

## Teknik Gereksinimler
- Python 3.10+
- openai-whisper
- tkinter (GUI için)
- ffmpeg (video işleme için)

## Dosya Yapısı
```
whisperAltyazıEkleme/
├── main.py              # Ana uygulama başlatıcı
├── gui.py               # GUI arayüzü
├── transcriber.py       # Whisper transkripsiyon modülü
├── srt_generator.py     # SRT dosya oluşturucu
├── requirements.txt     # Python bağımlılıkları
└── README.md            # Kullanım kılavuzu
```

## Whisper Modelleri
| Model    | Parametreler | VRAM   | Hız      | Kalite   |
|----------|-------------|--------|----------|----------|
| tiny     | 39M         | ~1GB   | En hızlı | Düşük    |
| base     | 74M         | ~1GB   | Hızlı    | Orta     |
| small    | 244M        | ~2GB   | Orta     | İyi      |
| medium   | 769M        | ~5GB   | Yavaş    | Çok İyi  |
| large    | 1550M       | ~10GB  | En yavaş | En İyi   |
| large-v2 | 1550M       | ~10GB  | En yavaş | En İyi   |
| large-v3 | 1550M       | ~10GB  | En yavaş | En İyi   |
