import os
import sys
import subprocess
import re
import glob

# ==============================================================================
# Auto-install yt-dlp if not installed
# بررسی و نصب خودکار yt-dlp در صورت عدم وجود
# ==============================================================================
try:
    import yt_dlp
except ImportError:
    print("[*] yt-dlp is not installed. Installing it automatically via pip...")
    print("[*] ابزار yt-dlp نصب نیست. در حال نصب خودکار از طریق pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
        print("[+] yt-dlp installed successfully!\n")
        print("[+] ابزار yt-dlp با موفقیت نصب شد!\n")
    except Exception as e:
        print(f"[-] Installation failed / خطا در نصب خودکار yt-dlp: {e}")
        sys.exit(1)

# ==============================================================================
# 🔴 [REQUIRED] Paste your Playlist Link HERE between these Quotations:
# 🔴 [الزامی] لینک پلی‌لیست یا ویدیوی خود را اینجا، دقیقاً میان این کوتیشن‌ها قرار دهید:
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLB7540DEDD482705B"

# 🔴 [REQUIRED] Paste your Target Folder Address HERE between these Quotations:
# 🔴 [الزامی] آدرس پوشه مقصد (برای ذخیره فایل‌ها) را اینجا، میان این دو کوتیشن قرار دهید:
DESTINATION_FOLDER = r"E:\Hooty\0000-Uni\03-Term 3-40451\01-گسسته\Course & Subtitles"
# ==============================================================================

def download_subtitles(playlist_url, dest_folder):
    """
    Downloads English subtitles cleanly bypassing 429 rate-limits using desktop headers and delay.
    دانلود مطمئن زیرنویس‌های انگلیسی با هدر استاندارد مرورگر و مکث ۲ ثانیه‌ای برای جلوگیری از ارور ۴۲۹.
    """
    print("⏳ Downloading subtitles cleanly (bypassing 429 rate limits)...")
    print("⏳ در حال دانلود مطمئن زیرنویس‌ها با دور زدن محدودیت نرخ درخواست...")
    
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    
    command = [
        sys.executable, "-m", "yt_dlp",
        "-P", dest_folder,
        "--write-subs",
        "--write-auto-subs",
        "--skip-download",
        "--sub-langs", "en.*,en",
        "--user-agent", user_agent,
        "--sleep-subtitles", "2",
        "--retries", "10",
        "--fragment-retries", "10",
        "-i",
        playlist_url
    ]
    
    subprocess.run(command)
    print("✅ Subtitle download process finished.\n")
    print("✅ فرایند دانلود زیرنویس‌ها به پایان رسید.\n")

def clean_vtt_text(text):
    """
    Cleans subtitle content by removing timestamps, headers, HTML tags, and duplicate lines.
    پاکسازی متن زیرنویس با حذف هدرها، تایم‌استمپ‌ها، تگ‌ها و خطوط تکراری یوتیوب.
    """
    text = re.sub(r'WEBVTT.*\n', '', text)
    text = re.sub(r'Kind: captions.*\n', '', text)
    text = re.sub(r'Language:.*\n', '', text)
    
    lines = text.split('\n')
    cleaned_lines = []
    last_line = ""
    
    for line in lines:
        if '-->' in line:
            continue
            
        line = re.sub(r'<[^>]+>', '', line)
        line = line.strip()
        
        if not line or line.isdigit():
            continue
            
        if line != last_line:
            cleaned_lines.append(line)
            last_line = line

    return ' '.join(cleaned_lines)

def merge_subtitles_to_txt(dest_folder):
    """
    Merges all cleaned subtitle files into a single structured master text file.
    ادغام تمام فایل‌های زیرنویس پاکسازی‌شده در یک فایل متنی جامع و تمیز.
    """
    print("⏳ Processing, stripping timestamps, and generating the master transcript file...")
    print("⏳ در حال پردازش، حذف تایم‌ستمپ‌ها و ساخت فایل متنی جامع...")
    
    search_pattern_vtt = os.path.join(dest_folder, "*.vtt")
    search_pattern_srt = os.path.join(dest_folder, "*.srt")
    subtitle_files = glob.glob(search_pattern_vtt) + glob.glob(search_pattern_srt)
    
    if not subtitle_files:
        print("❌ No subtitle files found in the specified directory!")
        print("❌ هیچ فایل زیرنویسی پیدا نشد!")
        return
    
    master_txt_path = os.path.join(dest_folder, "00_All_Lectures_Transcript.txt")
    
    with open(master_txt_path, 'w', encoding='utf-8') as master_file:
        master_file.write("=== Master Lectures Transcript (For AI Tutoring & Grounding) ===\n\n")
        
        for file_path in sorted(subtitle_files):
            file_name = os.path.basename(file_path)
            title = re.sub(r' \[[a-zA-Z0-9_-]+\]\..*$', '', file_name)
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as sf:
                raw_text = sf.read()
                
            pure_text = clean_vtt_text(raw_text)
            
            master_file.write(f"{'='*60}\n")
            master_file.write(f"🎥 Lecture / ویدیو: {title}\n")
            master_file.write(f"{'='*60}\n\n")
            master_file.write(pure_text + "\n\n\n")
            
    print(f"✅ Master transcript file successfully created and ready for AI:\n{master_txt_path}")
    print(f"✅ فایل نهایی یکپارچه با موفقیت ساخته شد و آماده ارسال به هوش مصنوعی است:\n{master_txt_path}")

if __name__ == "__main__":
    if not os.path.exists(DESTINATION_FOLDER):
        os.makedirs(DESTINATION_FOLDER, exist_ok=True)
        
    download_subtitles(PLAYLIST_URL, DESTINATION_FOLDER)
    merge_subtitles_to_txt(DESTINATION_FOLDER)
