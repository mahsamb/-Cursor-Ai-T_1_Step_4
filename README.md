# Telegram Shop Bot (Sports Supplements & Vitamins)

ربات فروشگاهی تلگرام با `aiogram 3.x` و `Async SQLAlchemy` برای فروش مکمل‌های ورزشی و ویتامین‌ها.

## امکانات MVP

- ثبت کاربر با دستور `/start`
- منوی اصلی: فروشگاه، جستجو، سبد خرید، سفارش‌های من، پشتیبانی
- نمایش دسته‌بندی‌ها و محصولات با Inline Keyboard
- نمایش جزئیات محصول + افزودن به سبد (با بررسی موجودی)
- جستجوی محصول با FSM
- مدیریت سبد خرید (نمایش، حذف، مجموع قیمت)
- تغییر تعداد آیتم سبد با دکمه‌های `+` و `-`
- صفحه‌بندی لیست محصولات هر دسته‌بندی
- ثبت سفارش با FSM (دریافت شماره تماس و آدرس)
- پیام نهایی ثبت سفارش:
  - `سفارش ثبت شد. درگاه پرداخت در نسخه بعد فعال می‌شود.`
- Seed اولیه دیتابیس شامل دسته‌بندی، برند و محصول
- پنل ادمین با دستور `/admin`:
  - مدیریت موجودی محصولات
  - مدیریت وضعیت سفارش‌ها (paid / shipped / cancelled)

## ساختار پروژه

```text
bot/
  handlers/
  keyboards/
  states/
db/
  models.py
  session.py
  seed.py
services/
config.py
main.py
```

## راه‌اندازی

1) ساخت محیط مجازی:

```bash
python -m venv .venv
```

2) فعال‌سازی محیط مجازی:

- ویندوز (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

3) نصب وابستگی‌ها:

```bash
pip install -r requirements.txt
```

4) ساخت فایل `.env` در ریشه پروژه:

```env
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=sqlite+aiosqlite:///shop.db
ADMIN_IDS=123456789,987654321
```

5) اجرا:

```bash
python main.py
```

## تست سریع سلامت

برای اطمینان از ایجاد جدول‌ها و seed شدن داده‌ها:

```bash
python -m db.smoke_check
```

## اجرا در Google Colab

1. پوشه پروژه را ZIP کنید.
2. نوت‌بوک `colab/Telegram_Shop_Bot_Colab.ipynb` را در [Colab](https://colab.research.google.com/) باز کنید.
3. سلول‌ها را به ترتیب اجرا کنید و `BOT_TOKEN` و `ADMIN_ID` را وارد کنید.
4. راهنمای کامل: [`colab/COLAB_GUIDE.md`](colab/COLAB_GUIDE.md)

## نکات

- در اولین اجرا، جداول ساخته شده و داده اولیه seed می‌شود.
- همه پیام‌های کاربر در ربات فارسی هستند.
- فقط کاربرانی که شناسه آن‌ها در `ADMIN_IDS` باشد به پنل ادمین دسترسی دارند.
- Colab برای تست مناسب است؛ برای اجرای ۲۴/۷ از VPS یا PC استفاده کنید.
