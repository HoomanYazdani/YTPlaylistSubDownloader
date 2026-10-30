# YouTube Playlist Transcript Extractor for AI Tutoring

[English](#english) | [فارسی](#farsi)

---

<a name="english"></a>
## English

> **Important Note on Network & IP Blocking:**  
> If you encounter `HTTP Error 429: Too Many Requests` or connection errors, your IP or shared VPN/proxy address has likely been temporarily rate-limited or blocked by YouTube. To resolve this, switch your VPN server, use a clean residential IP, or configure a proxy directly.

### Why Use This Tool?
Watching long educational videos takes too much time. However, asking an AI about video content without providing the actual transcript often causes the AI to hallucinate and give inaccurate answers. 

This tool converts YouTube playlists into a clean, unified text file, allowing you to feed exact sources into your AI prompts. This grounds the AI model so you can learn efficiently without watching every full video.

### Features:
- Downloads both manual and auto-generated subtitles.
- Removes timestamps, HTML tags, and repetitive auto-caption noise.
- Merges all lecture subtitles into a single text file.

---

<a name="farsi"></a>
## فارسی

> **توجه مهم درباره آی‌پی و شبکه:**  
> در صورت مواجهه با خطای `HTTP Error 429: Too Many Requests` یا خطاهای اتصال، احتمالاً آی‌پی شما یا سرور اشتراکی فیلترشکن / پروکسی توسط یوتیوب محدود (Rate-limit) یا بلاک شده است. برای رفع مشکل، لوکیشن/سرور را تغییر دهید یا از آی‌پی خلوت‌تری استفاده کنید.

### چرا از این ابزار استفاده کنیم؟
تماشای ویدیوهای آموزشی طولانی، زمان زیادی از شما می‌گیرد. از طرفی، پرسیدن از هوش مصنوعی درباره ویدیوها بدون ارائه متن اصلی، باعث تولید پاسخ‌های نادرست و حدسی می‌شود.

این ابزار، لیست پخش‌های آموزشی را به فایل‌های متنی تمیز و یکپارچه تبدیل می‌کند. با این کار می‌توانید منبع دقیق را مستقیماً به عنوان پرامپت به هوش مصنوعی بدهید تا بدون نیاز به تماشای کامل ویدیوها، به کمک هوش مصنوعی محتوا را یاد بگیرید و از خطاهای محاسباتی و پاسخ‌های تخیلی جلوگیری کنید.

این ابزار از این تکنیک پشتیبانی می‌کند:
- Grounding (تزریق منبع واقعی به هوش مصنوعی)

برای جلوگیری از این مشکل:
- Hallucination (توهم و پاسخ نادرست هوش مصنوعی)

### امکانات کلیدی:
- دانلود زیرنویس‌های دستی و خودکار
- Manual and Auto-generated Subtitles

- حذف زمان‌بندی‌ها، کدهای اضافی و خطوط تکراری

- ادغام تمام قسمت‌های یک دوره آموزشی در یک فایل متنی واحد

### نحوه استفاده:
۱. ابتدا ابزار مورد نیاز را نصب کنید:
`pip install yt-dlp`

۲. لینک لیست پخش و مسیر ذخیره فایل‌ها را در اسکریپت پایتون تنظیم کنید.

۳. اسکریپت را اجرا کرده و فایل خروجی نهایی را به عنوان منبع مرجع به پرامپت هوش مصنوعی بدهید.
