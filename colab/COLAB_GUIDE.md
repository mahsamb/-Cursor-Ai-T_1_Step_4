# راهنمای اجرا در Google Colab

## مراحل سریع

1. پوشه پروژه `Cursor Ai-T_1` را **ZIP** کنید (باید داخل zip فایل `main.py` باشد).
2. برو به [Google Colab](https://colab.research.google.com/).
3. **File → Upload notebook** و فایل `colab/Telegram_Shop_Bot_Colab.ipynb` را آپلود کن.
4. سلول‌ها را از بالا به پایین اجرا کن (Shift+Enter).
5. در سلول توکن، `BOT_TOKEN` و `ADMIN_ID` را پر کن.
6. سلول آخر را اجرا کن → ربات آنلاین می‌شود.

## روش Google Drive

1. کل پوشه پروژه را در Drive بگذار، مثلاً:
   `MyDrive/TelegramShopBot/Cursor Ai-T_1`
2. در نوت‌بوک سلول آپلود:
   - `USE_DRIVE = True`
   - مسیر `DRIVE_PROJECT_PATH` را درست کن.

## نکات مهم

| موضوع | توضیح |
|--------|--------|
| قطع شدن | Colab بعد از بیکاری یا timeout ربات را می‌بندد |
| توکن | فقط یک جا ربات را اجرا کنید (اگر روی PC هم روشن باشد conflict می‌دهد) |
| دیتابیس | `shop.db` در Colab موقت است؛ با Drive می‌توانید `DATABASE_URL` را به مسیر Drive تغییر دهید |
| ادمین | شناسه عددی خودتان را در `ADMIN_ID` بگذارید |

## دیتابیس روی Drive (اختیاری)

بعد از mount کردن Drive در سلول تنظیمات:

```python
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:////content/drive/MyDrive/TelegramShopBot/shop.db"
```

## عیب‌یابی

- **`BOT_TOKEN در .env تنظیم نشده`**: سلول توکن را قبل از سلول اجرا اجرا کنید.
- **`main.py پیدا نشد`**: zip باید شامل `main.py`, `bot/`, `db/`, `services/` باشد.
- **ربات جواب نمی‌دهد**: توکن را چک کنید؛ ربات را جای دیگر خاموش کنید.
- **دسترسی ادمین ندارید**: `ADMIN_ID` باید همان عدد @userinfobot باشد.
