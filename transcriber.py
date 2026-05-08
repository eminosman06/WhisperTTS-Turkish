"""
Whisper Transkripsiyon Modülü
OpenAI Whisper modelini kullanarak ses/video dosyalarından metin çıkarır.
"""

import whisper
import os
from typing import Optional, Callable


# Kullanılabilir Whisper modelleri
AVAILABLE_MODELS = [
    "tiny",
    "tiny.en",
    "base",
    "base.en",
    "small",
    "small.en",
    "medium",
    "medium.en",
    "large",
    "large-v2",
    "large-v3"
]

# Model bilgileri
MODEL_INFO = {
    "tiny": {"params": "39M", "vram": "~1GB", "speed": "En Hızlı", "quality": "Düşük"},
    "tiny.en": {"params": "39M", "vram": "~1GB", "speed": "En Hızlı", "quality": "Düşük (Sadece İngilizce)"},
    "base": {"params": "74M", "vram": "~1GB", "speed": "Hızlı", "quality": "Orta"},
    "base.en": {"params": "74M", "vram": "~1GB", "speed": "Hızlı", "quality": "Orta (Sadece İngilizce)"},
    "small": {"params": "244M", "vram": "~2GB", "speed": "Orta", "quality": "İyi"},
    "small.en": {"params": "244M", "vram": "~2GB", "speed": "Orta", "quality": "İyi (Sadece İngilizce)"},
    "medium": {"params": "769M", "vram": "~5GB", "speed": "Yavaş", "quality": "Çok İyi"},
    "medium.en": {"params": "769M", "vram": "~5GB", "speed": "Yavaş", "quality": "Çok İyi (Sadece İngilizce)"},
    "large": {"params": "1550M", "vram": "~10GB", "speed": "En Yavaş", "quality": "En İyi"},
    "large-v2": {"params": "1550M", "vram": "~10GB", "speed": "En Yavaş", "quality": "En İyi (v2)"},
    "large-v3": {"params": "1550M", "vram": "~10GB", "speed": "En Yavaş", "quality": "En İyi (v3)"},
}

# Desteklenen diller
SUPPORTED_LANGUAGES = {
    "auto": "Otomatik Algıla",
    "tr": "Türkçe",
    "en": "İngilizce",
    "de": "Almanca",
    "fr": "Fransızca",
    "es": "İspanyolca",
    "it": "İtalyanca",
    "pt": "Portekizce",
    "ru": "Rusça",
    "ja": "Japonca",
    "ko": "Korece",
    "zh": "Çince",
    "ar": "Arapça",
}


class WhisperTranscriber:
    """Whisper transkripsiyon sınıfı"""
    
    def __init__(self):
        self.model = None
        self.current_model_name = None
    
    def load_model(self, model_name: str, progress_callback: Optional[Callable] = None) -> bool:
        """
        Whisper modelini yükler.
        
        Args:
            model_name: Yüklenecek model adı
            progress_callback: İlerleme bildirimi için callback fonksiyonu
        
        Returns:
            Başarılı ise True
        """
        try:
            if progress_callback:
                progress_callback(f"'{model_name}' modeli yükleniyor...")
            
            self.model = whisper.load_model(model_name)
            self.current_model_name = model_name
            
            if progress_callback:
                progress_callback(f"'{model_name}' modeli başarıyla yüklendi!")
            
            return True
        except Exception as e:
            if progress_callback:
                progress_callback(f"Model yükleme hatası: {str(e)}")
            return False
    
    def transcribe(
        self,
        audio_path: str,
        language: str = "auto",
        task: str = "transcribe",
        progress_callback: Optional[Callable] = None
    ) -> dict:
        """
        Ses/video dosyasını transkribe eder.
        
        Args:
            audio_path: Ses veya video dosyası yolu
            language: Dil kodu ("auto" otomatik algılama için)
            task: "transcribe" veya "translate" (İngilizce'ye çeviri)
            progress_callback: İlerleme bildirimi için callback
        
        Returns:
            Transkripsiyon sonucu (segments içerir)
        """
        if self.model is None:
            raise RuntimeError("Model yüklenmedi! Önce load_model() çağırın.")
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Dosya bulunamadı: {audio_path}")
        
        if progress_callback:
            progress_callback("Transkripsiyon başlıyor...")
        
        # Transkripsiyon parametreleri
        options = {
            "task": task,
            "verbose": False
        }
        
        # Dil belirtilmişse ekle
        if language != "auto":
            options["language"] = language
        
        try:
            result = self.model.transcribe(audio_path, **options)
            
            if progress_callback:
                progress_callback("Transkripsiyon tamamlandı!")
            
            return result
        except Exception as e:
            if progress_callback:
                progress_callback(f"Transkripsiyon hatası: {str(e)}")
            raise
    
    def get_model_info(self) -> Optional[dict]:
        """Yüklü model hakkında bilgi döndürür."""
        if self.current_model_name and self.current_model_name in MODEL_INFO:
            return MODEL_INFO[self.current_model_name]
        return None
    
    def is_model_loaded(self) -> bool:
        """Model yüklü mü kontrol eder."""
        return self.model is not None


def get_available_models() -> list:
    """Kullanılabilir model listesini döndürür."""
    return AVAILABLE_MODELS.copy()


def get_model_info(model_name: str) -> Optional[dict]:
    """Belirtilen model hakkında bilgi döndürür."""
    return MODEL_INFO.get(model_name)


def get_supported_languages() -> dict:
    """Desteklenen dilleri döndürür."""
    return SUPPORTED_LANGUAGES.copy()
