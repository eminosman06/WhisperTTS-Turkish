"""
Whisper Altyazı Oluşturucu
========================
OpenAI Whisper modelini kullanarak video/ses dosyalarından 
otomatik SRT altyazı oluşturan Windows uygulaması.

Kullanım:
    python main.py

Gereksinimler:
    - Python 3.10+
    - openai-whisper
    - ffmpeg (sistem PATH'inde olmalı)
"""

import sys
import os

# Modül yolunu ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import run_app


def check_dependencies():
    """Gerekli bağımlılıkları kontrol eder"""
    missing = []
    
    try:
        import whisper
    except ImportError:
        missing.append("openai-whisper")
    
    try:
        import torch
    except ImportError:
        missing.append("torch")
    
    if missing:
        print("❌ Eksik bağımlılıklar:")
        for dep in missing:
            print(f"   - {dep}")
        print("\nYüklemek için:")
        print("   pip install -r requirements.txt")
        return False
    
    return True


def check_ffmpeg():
    """FFmpeg yüklü mü kontrol eder"""
    import subprocess
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def main():
    """Ana giriş noktası"""
    print("=" * 50)
    print("🎬 Whisper Altyazı Oluşturucu")
    print("=" * 50)
    
    # Bağımlılık kontrolü
    print("\n📦 Bağımlılıklar kontrol ediliyor...")
    if not check_dependencies():
        input("\nDevam etmek için Enter'a basın...")
        sys.exit(1)
    print("   ✅ Python bağımlılıkları tamam")
    
    # FFmpeg kontrolü
    if not check_ffmpeg():
        print("   ⚠️  FFmpeg bulunamadı!")
        print("      Video dosyaları için FFmpeg gereklidir.")
        print("      https://ffmpeg.org/download.html adresinden indirin.")
        print("      Veya: winget install FFmpeg")
    else:
        print("   ✅ FFmpeg yüklü")
    
    print("\n🚀 Uygulama başlatılıyor...\n")
    
    # GUI'yi başlat
    run_app()


if __name__ == "__main__":
    main()
