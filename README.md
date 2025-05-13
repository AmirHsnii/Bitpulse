# BitPulse - Persian Crypto RSS Aggregator

A lightweight, production-grade RSS aggregator for cryptocurrency news with a Persian-first web interface.

## Features

- 🔄 Hourly RSS feed updates
- 🌐 Persian-first UI with RTL support
- 📱 Responsive design with Tailwind CSS
- 🔍 Full-text search and filtering
- 📊 Real-time updates via WebSocket
- 🌍 Bilingual support (Persian/English)

## Quick Start

### Backend Setup

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
cryptopulse/
│  requirements.txt
│  README.md
├─ app/
│   ├─ core/          (config, logging)
│   ├─ db.py          (SQLModel, SQLite file)
│   ├─ models.py      (Feed, Article)
│   ├─ schemas.py     (Pydantic)
│   ├─ crud.py        (DB helpers)
│   ├─ rss.py         (feed‑parser logic)
│   ├─ scheduler.py   (APScheduler job)
│   └─ main.py        (FastAPI instance)
└─ tests/             (pytest)
```

## Development

- Backend: Python 3.11 + FastAPI
- Frontend: React 18 + Vite + Tailwind CSS
- Database: SQLite (SQLModel)
- Testing: pytest with >80% coverage

## License

MIT

---

# بیت‌پالس - تجمیع‌کننده خوراک‌های رمزارزی

یک تجمیع‌کننده خوراک RSS سبک و حرفه‌ای برای اخبار رمزارز با رابط کاربری فارسی‌محور.

## ویژگی‌ها

- 🔄 به‌روزرسانی ساعتی خوراک‌های RSS
- 🌐 رابط کاربری فارسی‌محور با پشتیبانی RTL
- 📱 طراحی واکنش‌گرا با Tailwind CSS
- 🔍 جستجوی متنی و فیلتر کردن
- 📊 به‌روزرسانی‌های زنده از طریق WebSocket
- 🌍 پشتیبانی دو زبانه (فارسی/انگلیسی)

## شروع سریع

### راه‌اندازی بک‌اند

```bash
# ایجاد و فعال‌سازی محیط مجازی
python -m venv .venv
source .venv/bin/activate  # در ویندوز: .venv\Scripts\activate

# نصب وابستگی‌ها
pip install -r requirements.txt

# اجرای سرور توسعه
uvicorn app.main:app --reload
```

### راه‌اندازی فرانت‌اند

```bash
cd frontend
npm install
npm run dev
```

## مستندات API

پس از اجرای بک‌اند، به آدرس‌های زیر مراجعه کنید:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 