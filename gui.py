"""
Whisper Altyazı Ekleme - GUI Arayüzü
Modern ve kullanıcı dostu tkinter arayüzü
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path

from transcriber import (
    WhisperTranscriber,
    get_available_models,
    get_model_info,
    get_supported_languages,
    MODEL_INFO
)
from srt_generator import save_srt_file, get_srt_stats


def get_whisper_cache_dir() -> Path:
    """Whisper model cache dizinini döndürür"""
    return Path.home() / ".cache" / "whisper"


def get_cached_models() -> list:
    """İndirilmiş modellerin listesini döndürür"""
    cache_dir = get_whisper_cache_dir()
    if not cache_dir.exists():
        return []
    
    models = []
    for file in cache_dir.glob("*.pt"):
        size_mb = file.stat().st_size / (1024 * 1024)
        models.append({
            "name": file.stem,
            "size_mb": round(size_mb, 2),
            "path": str(file)
        })
    return models


class WhisperSubtitleApp:
    """Ana uygulama sınıfı"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Whisper Altyazı Oluşturucu")
        self.root.geometry("800x700")
        self.root.minsize(700, 600)
        
        # Uygulama durumu
        self.transcriber = WhisperTranscriber()
        self.selected_file = None
        self.is_processing = False
        self.last_result = None
        
        # Stil ayarları
        self.setup_styles()
        
        # Arayüzü oluştur
        self.create_widgets()
        
        # Pencere kapatma olayı
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Tema ve stil ayarları"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Özel stiller
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10))
        style.configure("Info.TLabel", font=("Segoe UI", 9))
        style.configure("Success.TLabel", foreground="green")
        style.configure("Error.TLabel", foreground="red")
        style.configure("Big.TButton", font=("Segoe UI", 11), padding=10)
    
    def create_widgets(self):
        """Ana arayüz bileşenlerini oluşturur"""
        
        # Ana container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        title_label = ttk.Label(
            main_frame, 
            text="🎬 Whisper Altyazı Oluşturucu",
            style="Title.TLabel"
        )
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(
            main_frame,
            text="OpenAI Whisper ile otomatik altyazı oluşturun",
            style="Subtitle.TLabel"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # ============ DOSYA SEÇİMİ ============
        file_frame = ttk.LabelFrame(main_frame, text="📁 Dosya Seçimi", padding="15")
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        file_inner = ttk.Frame(file_frame)
        file_inner.pack(fill=tk.X)
        
        self.file_path_var = tk.StringVar(value="Henüz dosya seçilmedi...")
        file_entry = ttk.Entry(file_inner, textvariable=self.file_path_var, state="readonly")
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(file_inner, text="Dosya Seç", command=self.browse_file)
        browse_btn.pack(side=tk.RIGHT)
        
        # Desteklenen formatlar bilgisi
        formats_label = ttk.Label(
            file_frame,
            text="Desteklenen formatlar: MP4, MKV, AVI, MOV, MP3, WAV, M4A, FLAC",
            style="Info.TLabel"
        )
        formats_label.pack(anchor=tk.W, pady=(10, 0))
        
        # ============ MODEL SEÇİMİ ============
        model_frame = ttk.LabelFrame(main_frame, text="🤖 Model Ayarları", padding="15")
        model_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Model seçimi
        model_row = ttk.Frame(model_frame)
        model_row.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(model_row, text="Whisper Modeli:").pack(side=tk.LEFT)
        
        self.model_var = tk.StringVar(value="base")
        model_combo = ttk.Combobox(
            model_row,
            textvariable=self.model_var,
            values=get_available_models(),
            state="readonly",
            width=20
        )
        model_combo.pack(side=tk.LEFT, padx=(10, 20))
        model_combo.bind("<<ComboboxSelected>>", self.on_model_selected)
        
        # Model bilgisi
        self.model_info_var = tk.StringVar()
        self.update_model_info()
        model_info_label = ttk.Label(model_row, textvariable=self.model_info_var, style="Info.TLabel")
        model_info_label.pack(side=tk.LEFT)
        
        # Dil seçimi
        lang_row = ttk.Frame(model_frame)
        lang_row.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(lang_row, text="Dil:").pack(side=tk.LEFT)
        
        languages = get_supported_languages()
        self.lang_var = tk.StringVar(value="auto")
        lang_combo = ttk.Combobox(
            lang_row,
            textvariable=self.lang_var,
            values=list(languages.keys()),
            state="readonly",
            width=20
        )
        lang_combo.pack(side=tk.LEFT, padx=(10, 20))
        
        # Dil açıklaması
        self.lang_desc_var = tk.StringVar(value="Otomatik Algıla")
        lang_desc_label = ttk.Label(lang_row, textvariable=self.lang_desc_var, style="Info.TLabel")
        lang_desc_label.pack(side=tk.LEFT)
        lang_combo.bind("<<ComboboxSelected>>", self.on_lang_selected)
        
        # Görev seçimi
        task_row = ttk.Frame(model_frame)
        task_row.pack(fill=tk.X)
        
        ttk.Label(task_row, text="Görev:").pack(side=tk.LEFT)
        
        self.task_var = tk.StringVar(value="transcribe")
        task_transcribe = ttk.Radiobutton(
            task_row, text="Transkripsiyon", 
            variable=self.task_var, value="transcribe"
        )
        task_transcribe.pack(side=tk.LEFT, padx=(10, 20))
        
        task_translate = ttk.Radiobutton(
            task_row, text="İngilizce'ye Çevir", 
            variable=self.task_var, value="translate"
        )
        task_translate.pack(side=tk.LEFT)
        
        # ============ ÇIKTI AYARLARI ============
        output_frame = ttk.LabelFrame(main_frame, text="💾 Çıktı Ayarları", padding="15")
        output_frame.pack(fill=tk.X, pady=(0, 15))
        
        output_row = ttk.Frame(output_frame)
        output_row.pack(fill=tk.X)
        
        ttk.Label(output_row, text="Çıktı Klasörü:").pack(side=tk.LEFT)
        
        self.output_dir_var = tk.StringVar(value=str(Path.home() / "Desktop"))
        output_entry = ttk.Entry(output_row, textvariable=self.output_dir_var, width=50)
        output_entry.pack(side=tk.LEFT, padx=(10, 10), fill=tk.X, expand=True)
        
        output_browse_btn = ttk.Button(output_row, text="Seç", command=self.browse_output_dir)
        output_browse_btn.pack(side=tk.RIGHT)
        
        # ============ İŞLEM BUTONLARI ============
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 15))
        
        self.process_btn = ttk.Button(
            btn_frame,
            text="🚀 Altyazı Oluştur",
            style="Big.TButton",
            command=self.start_processing
        )
        self.process_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        self.cancel_btn = ttk.Button(
            btn_frame,
            text="İptal",
            command=self.cancel_processing,
            state=tk.DISABLED
        )
        self.cancel_btn.pack(side=tk.RIGHT)
        
        # ============ İLERLEME ============
        progress_frame = ttk.LabelFrame(main_frame, text="📊 İlerleme", padding="15")
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            mode="indeterminate"
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        self.status_var = tk.StringVar(value="Hazır")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        status_label.pack(anchor=tk.W)
        
        # ============ LOG ALANI ============
        log_frame = ttk.LabelFrame(main_frame, text="📝 İşlem Günlüğü", padding="15")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar ile text widget
        log_scroll = ttk.Scrollbar(log_frame)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(
            log_frame,
            height=8,
            wrap=tk.WORD,
            yscrollcommand=log_scroll.set,
            state=tk.DISABLED,
            font=("Consolas", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        log_scroll.config(command=self.log_text.yview)
        
        # Başlangıç logu ve cache bilgisi
        self.log("Uygulama başlatıldı. Bir video veya ses dosyası seçin.")
        self.show_cached_models_info()
    
    def log(self, message: str):
        """Log alanına mesaj ekler"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"• {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def show_cached_models_info(self):
        """İndirilmiş modeller hakkında bilgi gösterir"""
        cached = get_cached_models()
        cache_dir = get_whisper_cache_dir()
        
        if cached:
            self.log(f"📦 Model cache konumu: {cache_dir}")
            self.log(f"   İndirilmiş modeller ({len(cached)} adet):")
            for model in cached:
                self.log(f"   • {model['name']}: {model['size_mb']} MB")
        else:
            self.log(f"📦 Model cache konumu: {cache_dir}")
            self.log("   Henüz indirilmiş model yok. İlk kullanımda indirilecek.")
    
    def browse_file(self):
        """Dosya seçme dialogu"""
        filetypes = [
            ("Tüm Desteklenen", "*.mp4;*.mkv;*.avi;*.mov;*.wmv;*.flv;*.webm;*.mp3;*.wav;*.m4a;*.flac;*.ogg;*.wma;*.aac"),
            ("Video Dosyaları", "*.mp4;*.mkv;*.avi;*.mov;*.wmv;*.flv;*.webm"),
            ("Ses Dosyaları", "*.mp3;*.wav;*.m4a;*.flac;*.ogg;*.wma;*.aac"),
            ("WAV Dosyaları", "*.wav"),
            ("MP3 Dosyaları", "*.mp3"),
            ("Tüm Dosyalar", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(
            title="Video veya Ses Dosyası Seçin",
            filetypes=filetypes,
            initialdir=os.path.expanduser("~")
        )
        
        if filepath:
            self.selected_file = filepath
            self.file_path_var.set(filepath)
            self.log(f"Dosya seçildi: {os.path.basename(filepath)}")
    
    def browse_output_dir(self):
        """Çıktı klasörü seçme dialogu"""
        directory = filedialog.askdirectory(title="Çıktı Klasörü Seçin")
        if directory:
            self.output_dir_var.set(directory)
            self.log(f"Çıktı klasörü: {directory}")
    
    def on_model_selected(self, event=None):
        """Model seçildiğinde bilgiyi güncelle"""
        self.update_model_info()
    
    def update_model_info(self):
        """Model bilgisini günceller"""
        model = self.model_var.get()
        info = get_model_info(model)
        if info:
            self.model_info_var.set(
                f"({info['params']} parametre, {info['vram']} VRAM, {info['speed']})"
            )
    
    def on_lang_selected(self, event=None):
        """Dil seçildiğinde açıklamayı güncelle"""
        lang = self.lang_var.get()
        languages = get_supported_languages()
        self.lang_desc_var.set(languages.get(lang, ""))
    
    def start_processing(self):
        """Transkripsiyon işlemini başlatır"""
        # Validasyon
        if not self.selected_file:
            messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin!")
            return
        
        if not os.path.exists(self.selected_file):
            messagebox.showerror("Hata", "Seçilen dosya bulunamadı!")
            return
        
        output_dir = self.output_dir_var.get()
        if not os.path.isdir(output_dir):
            messagebox.showerror("Hata", "Geçersiz çıktı klasörü!")
            return
        
        # İşlemi başlat
        self.is_processing = True
        self.process_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.progress_bar.start(10)
        
        # Arka planda çalıştır
        thread = threading.Thread(target=self.process_file, daemon=True)
        thread.start()
    
    def process_file(self):
        """Dosyayı işler (arka plan thread'i)"""
        try:
            model_name = self.model_var.get()
            language = self.lang_var.get()
            task = self.task_var.get()
            
            # Model yükle
            self.update_status(f"'{model_name}' modeli yükleniyor...")
            self.log(f"Model yükleniyor: {model_name}")
            
            if not self.transcriber.is_model_loaded() or \
               self.transcriber.current_model_name != model_name:
                success = self.transcriber.load_model(
                    model_name,
                    progress_callback=self.log
                )
                if not success:
                    raise RuntimeError("Model yüklenemedi!")
            
            # Transkripsiyon
            self.update_status("Transkripsiyon yapılıyor... (Bu biraz sürebilir)")
            self.log("Transkripsiyon başladı...")
            
            result = self.transcriber.transcribe(
                self.selected_file,
                language=language if language != "auto" else "auto",
                task=task,
                progress_callback=self.log
            )
            
            self.last_result = result
            
            # SRT dosyası oluştur
            self.update_status("SRT dosyası oluşturuluyor...")
            
            # Dosya adını al
            base_name = os.path.splitext(os.path.basename(self.selected_file))[0]
            output_path = os.path.join(self.output_dir_var.get(), f"{base_name}.srt")
            
            saved_path = save_srt_file(result["segments"], output_path)
            
            # İstatistikler
            stats = get_srt_stats(result["segments"])
            
            # Başarılı
            self.update_status("Tamamlandı!")
            self.log(f"✅ SRT dosyası kaydedildi: {saved_path}")
            self.log(f"   Segment sayısı: {stats['segment_count']}")
            self.log(f"   Toplam süre: {stats['total_duration']:.1f} saniye")
            self.log(f"   Toplam karakter: {stats['total_characters']}")
            
            # Algılanan dil
            if "language" in result:
                self.log(f"   Algılanan dil: {result['language']}")
            
            self.root.after(0, lambda: messagebox.showinfo(
                "Başarılı",
                f"Altyazı dosyası oluşturuldu!\n\n{saved_path}"
            ))
            
        except Exception as e:
            self.log(f"❌ Hata: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Hata", str(e)))
        
        finally:
            self.root.after(0, self.finish_processing)
    
    def update_status(self, message: str):
        """Durum mesajını günceller (thread-safe)"""
        self.root.after(0, lambda: self.status_var.set(message))
    
    def finish_processing(self):
        """İşlem bittiğinde UI'ı günceller"""
        self.is_processing = False
        self.process_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        self.progress_bar.stop()
        self.progress_var.set(0)
    
    def cancel_processing(self):
        """İşlemi iptal eder"""
        if self.is_processing:
            self.is_processing = False
            self.log("İşlem iptal edildi.")
            self.finish_processing()
    
    def on_closing(self):
        """Pencere kapatılırken"""
        if self.is_processing:
            if messagebox.askyesno("Onay", "İşlem devam ediyor. Çıkmak istediğinizden emin misiniz?"):
                self.root.destroy()
        else:
            self.root.destroy()


def run_app():
    """Uygulamayı başlatır"""
    root = tk.Tk()
    app = WhisperSubtitleApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()
