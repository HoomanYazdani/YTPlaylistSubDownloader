import os
import sys
import subprocess
import re
import glob

# ==============================================================================
# ! ############################################################################
# ! 🔴 CRITICAL / REQUIRED CONFIGURATION: SET YOUR URL & PATH HERE
# ! 🔴 بخش حیاتی و اجباری: لینک پلی‌لیست و مسیر پوشه را در این قسمت وارد کنید
# ! ############################################################################
#
# [Step 1] Enter target YouTube playlist URL:
# [گام اول] آدرس کامل پلی‌لیست یوتیوب را وارد کنید:
PLAYLIST_URL = "https://www.youtube.com/playlist?list=********"

# [Step 2] Enter the target directory where files should be saved:
# [گام دوم] مسیر پوشه‌ای که زیرنویس‌ها و فایل نهایی باید در آن ذخیره شوند:
DESTINATION_FOLDER = r"C:\Users\Default\Downloads"
# ==============================================================================


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


def natural_sort_key(s):
    """
    Sort strings containing numbers in natural human order (e.g., Lecture 2 before Lecture 10).
    مرتب‌سازی طبیعی رشته‌های حاوی عدد به گونه‌ای که درس ۲ قبل از درس ۱۰ قرار گیرد.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]


def download_subtitles(playlist_url, dest_folder):
    """
    Download a single clean English subtitle per lecture while bypassing HTTP 429 rate limits.
    دانلود یک نسخه یکتا از زیرنویس انگلیسی برای هر جلسه با دور زدن محدودیت‌های درخواست یوتیوب.
    """
    print("⏳ Downloading subtitles cleanly (bypassing 429 rate limits)...")
    print("⏳ در حال دانلود مطمئن زیرنویس‌ها...")

    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    )

    command = [
        sys.executable, "-m", "yt_dlp",
        "-P", dest_folder,
        "--write-subs",
        "--write-auto-subs",
        "--skip-download",
        "--sub-langs", "en",          # Fetch a single English subtitle track to avoid duplicate dialect files
        "--user-agent", user_agent,
        "--sleep-subtitles", "2",     # Delay between subtitles to prevent HTTP 429
        "--retries", "10",
        "--fragment-retries", "10",
        "-i",                         # Continue downloading subsequent lectures on error
        playlist_url
    ]

    subprocess.run(command)
    print("✅ Subtitle download process finished.\n")
    print("✅ فرآیند دانلود زیرنویس‌ها به پایان رسید.\n")


def clean_vtt_text(text):
    """
    Strip WebVTT headers, timecodes, styling blocks, and HTML tags.
    حذف هدرهای وب‌وی‌تی‌تی، تایم‌استمپ‌ها، کدهای زمانی و تگ‌های HTML.
    """
    text = re.sub(r'WEBVTT.*?\n', '', text, flags=re.DOTALL)
    text = re.sub(r'Kind:.*?\n', '', text)
    text = re.sub(r'Language:.*?\n', '', text)

    lines = text.splitlines()
    cleaned_lines = []
    last_line = ""

    for line in lines:
        if '-->' in line or line.strip().startswith('NOTE') or line.strip().startswith('STYLE'):
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
    Filter duplicate subtitle files, sort naturally, and compile into a single master document.
    ادغام هوشمند و یکتای تمام فایل‌های زیرنویس به ترتیب طبیعی در یک فایل متنی جامع.
    """
    print("⏳ Processing, stripping duplicates, and generating master transcript...")
    print("⏳ در حال پردازش، حذف نسخه‌های تکراری و ساخت فایل جامع...")

    search_pattern_vtt = os.path.join(dest_folder, "*.vtt")
    search_pattern_srt = os.path.join(dest_folder, "*.srt")
    raw_files = glob.glob(search_pattern_vtt) + glob.glob(search_pattern_srt)

    if not raw_files:
        print("❌ No subtitle files found in this folder!")
        print("❌ هیچ فایل زیرنویسی در این پوشه یافت نشد!")
        return

    video_map = {}
    for f in raw_files:
        filename = os.path.basename(f)
        base_id = re.sub(r'(\.[a-z]{2}(-[A-Za-z]+)?)?\.(vtt|srt)$', '', filename)
        if base_id not in video_map:
            video_map[base_id] = f

    sorted_unique_files = sorted(video_map.values(), key=natural_sort_key)

    master_txt_path = os.path.join(dest_folder, "00_All_Lectures_Transcript.txt")

    with open(master_txt_path, 'w', encoding='utf-8') as master_file:
        master_file.write("=== Master Lectures Transcript (For AI Tutoring & Grounding) ===\n\n")

        for file_path in sorted_unique_files:
            file_name = os.path.basename(file_path)
            clean_title = re.sub(r'(\.[a-z]{2}(-[A-Za-z]+)?)?\.(vtt|srt)$', '', file_name)
            clean_title = re.sub(r' \[[a-zA-Z0-9_-]+\]$', '', clean_title)

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as sf:
                raw_text = sf.read()

            pure_text = clean_vtt_text(raw_text)

            if not pure_text.strip():
                continue

            master_file.write(f"{'='*60}\n")
            master_file.write(f"🎥 Lecture / ویدیو: {clean_title}\n")
            master_file.write(f"{'='*60}\n\n")
            master_file.write(pure_text + "\n\n\n")

    print(f"✅ Master transcript generated successfully with {len(sorted_unique_files)} unique lectures:")
    print(f"✅ فایل نهایی کامل با {len(sorted_unique_files)} جلسه یکتا و مرتب ساخته شد:\n{master_txt_path}")


if __name__ == "__main__":
    if not os.path.exists(DESTINATION_FOLDER):
        os.makedirs(DESTINATION_FOLDER, exist_ok=True)

    download_subtitles(PLAYLIST_URL, DESTINATION_FOLDER)
    merge_subtitles_to_txt(DESTINATION_FOLDER)
