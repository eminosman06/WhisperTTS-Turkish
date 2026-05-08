"""
SRT Dosya Oluşturucu
DaVinci Resolve uyumlu SRT formatında altyazı dosyası oluşturur.
"""

def format_timestamp(seconds: float) -> str:
    """
    Saniye cinsinden süreyi SRT zaman damgası formatına çevirir.
    Format: HH:MM:SS,mmm
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def create_srt_content(segments: list) -> str:
    """
    Whisper segmentlerinden SRT içeriği oluşturur.
    
    Args:
        segments: Whisper transkripsiyon segmentleri
                  Her segment: {"start": float, "end": float, "text": str}
    
    Returns:
        SRT formatında string
    """
    srt_lines = []
    
    for i, segment in enumerate(segments, start=1):
        start_time = format_timestamp(segment["start"])
        end_time = format_timestamp(segment["end"])
        text = segment["text"].strip()
        
        # SRT formatı:
        # 1
        # 00:00:01,000 --> 00:00:04,000
        # Altyazı metni
        #
        srt_lines.append(f"{i}")
        srt_lines.append(f"{start_time} --> {end_time}")
        srt_lines.append(text)
        srt_lines.append("")  # Boş satır
    
    return "\n".join(srt_lines)


def save_srt_file(segments: list, output_path: str, encoding: str = "utf-8-sig") -> str:
    """
    SRT dosyasını diske kaydeder.
    
    Args:
        segments: Whisper transkripsiyon segmentleri
        output_path: Çıktı dosya yolu
        encoding: Dosya kodlaması (utf-8-sig BOM ile, DaVinci Resolve uyumlu)
    
    Returns:
        Kaydedilen dosya yolu
    """
    srt_content = create_srt_content(segments)
    
    # .srt uzantısı yoksa ekle
    if not output_path.lower().endswith(".srt"):
        output_path += ".srt"
    
    with open(output_path, "w", encoding=encoding) as f:
        f.write(srt_content)
    
    return output_path


def get_srt_stats(segments: list) -> dict:
    """
    SRT dosyası için istatistikler döndürür.
    """
    if not segments:
        return {
            "segment_count": 0,
            "total_duration": 0,
            "total_characters": 0
        }
    
    total_chars = sum(len(seg["text"].strip()) for seg in segments)
    total_duration = segments[-1]["end"] if segments else 0
    
    return {
        "segment_count": len(segments),
        "total_duration": total_duration,
        "total_characters": total_chars
    }
