import os
import subprocess
import re
import glob

# ==============================================================================
# 🔴 [REQUIRED] Paste your Playlist Link HERE between these Quotations:
# 🔴 [الزامی] لینک پلی‌لیست یا ویدیوی خود را اینجا، دقیقاً میان این کوتیشن‌ها قرار دهید:
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL4C4C8A7D06566F38"

# 🔴 [REQUIRED] Paste your Target Folder Address HERE between these Quotations:
# 🔴 [الزامی] آدرس پوشه مقصد (برای ذخیره فایل‌ها) را اینجا، میان این دو کوتیشن قرار دهید:
DESTINATION_FOLDER = r"E:\Hooty\0000-Uni\03-Term 3-40451\02-ریاضی عمومی 2"
# ==============================================================================

def download_subtitles(playlist_url, dest_folder):
    """
    Downloads all available subtitles (both manual and auto-generated) using yt-dlp.
    دانلود تمام زیرنویس‌های موجود (دستی و خودکار) با استفاده از ابزار yt-dlp.
    """
    print("⏳ Downloading all subtitles (manual and auto-generated)...")
    print("⏳ در حال دانلود تمامی زیرنویس‌ها (دستی و خودکار)...")
    
    command = [
        "yt-dlp",
        "-P", dest_folder,
        "--write-subs",
        "--write-auto-subs",
        "--skip-download",
        "--sub-langs", "en.*,fa.*",
        "--extractor-args", "youtube:player_client=mweb,android",
        playlist_url
    ]
    
    subprocess.run(command)
    print("✅ Subtitle download finished successfully.\n")
    print("✅ دانلود زیرنویس‌ها به پایان رسید.\n")

def clean_vtt_text(text):
    """
    Cleans VTT subtitle content by removing timestamps, HTML tags, and duplicate lines.
    پاکسازی محتوای زیرنویس VTT با حذف زمان‌بندی‌ها، تگ‌های HTML و خطوط تکراری.
    """
    # Remove standard VTT header metadata / حذف هدرهای استاندارد VTT
    text = re.sub(r'WEBVTT.*\n', '', text)
    text = re.sub(r'Kind: captions.*\n', '', text)
    text = re.sub(r'Language:.*\n', '', text)
    
    lines = text.split('\n')
    cleaned_lines = []
    last_line = ""
    
    for line in lines:
        # Skip timestamp lines / نادیده گرفتن خطوط زمان‌بندی
        if '-->' in line:
            continue
            
        # Remove HTML tags (e.g., <c>, </c>) / حذف تگ‌های HTML
        line = re.sub(r'<[^>]+>', '', line)
        line = line.strip()
        
        # Skip empty lines and numeric counters / نادیده گرفتن خطوط خالی و شماره‌ها
        if not line or line.isdigit():
            continue
            
        # Prevent repetitive sentences (common in YouTube auto-generated captions)
        # جلوگیری از تکرار جملات (مشکل رایج زیرنویس‌های اتوماتیک یوتیوب)
        if line != last_line:
            cleaned_lines.append(line)
            last_line = line

    return ' '.join(cleaned_lines)

def merge_subtitles_to_txt(dest_folder):
    """
    Merges all cleaned subtitle files into a single structured master text file.
    ادغام تمام فایل‌های زیرنویس پاکسازی‌شده در یک فایل متنی جامع و ساختاریافته.
    """
    print("⏳ Processing, stripping timestamps, and generating the master transcript file...")
    print("⏳ در حال پردازش، حذف تایم‌ستمپ‌ها و ساخت فایل متنی جامع...")
    
    # Search for all downloaded .vtt files in the destination folder
    # جستجوی تمام فایل‌های .vtt دانلود شده در پوشه مقصد
    search_pattern = os.path.join(dest_folder, "*.vtt")
    subtitle_files = glob.glob(search_pattern)
    
    if not subtitle_files:
        print("❌ No subtitle files found in the specified directory!")
        print("❌ هیچ فایل زیرنویسی پیدا نشد!")
        return
    
    master_txt_path = os.path.join(dest_folder, "00_All_Lectures_Transcript.txt")
    
    with open(master_txt_path, 'w', encoding='utf-8') as master_file:
        master_file.write("=== Master Lectures Transcript (For AI Tutoring & Analysis) ===\n\n")
        
        # Sort files to maintain lecture order / مرتب‌سازی فایل‌ها برای حفظ ترتیب جلسات
        for file_path in sorted(subtitle_files):
            file_name = os.path.basename(file_path)
            
            # Extract clean video title from filename / استخراج نام تمیز ویدیو از نام فایل
            title = re.sub(r' \[[a-zA-Z0-9_-]+\]\..*\.vtt', '', file_name)
            
            with open(file_path, 'r', encoding='utf-8') as sf:
                raw_text = sf.read()
                
            pure_text = clean_vtt_text(raw_text)
            
            master_file.write(f"{'='*50}\n")
            master_file.write(f"🎥 Lecture / ویدیو: {title}\n")
            master_file.write(f"{'='*50}\n\n")
            master_file.write(pure_text + "\n\n\n")
            
    print(f"✅ Master transcript file successfully created and ready for AI:\n{master_file_path}")
    print(f"✅ فایل نهایی یکپارچه با موفقیت ساخته شد و آماده ارسال به هوش مصنوعی است:\n{master_txt_path}")

if __name__ == "__main__":
    if not os.path.exists(DESTINATION_FOLDER):
        os.makedirs(DESTINATION_FOLDER)
        
    download_subtitles(PLAYLIST_URL, DESTINATION_FOLDER)
    merge_subtitles_to_txt(DESTINATION_FOLDER)
