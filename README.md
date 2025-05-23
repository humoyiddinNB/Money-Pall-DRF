# 💸 Money Pall – Moliyaviy Boshqaruv API Ilovasi (DRF versiyasi)

**Money Pall** — bu foydalanuvchilarga o‘z moliyaviy holatini boshqarishga yordam beruvchi RESTful API asosidagi web ilova. Foydalanuvchi daromad va harajatlarni kategoriya bo‘yicha boshqaradi, statistik diagrammalar orqali moliyaviy tahlil oladi. Ilova Django REST Framework (DRF) asosida yaratilgan.

---

## 🛠 Texnologiyalar

- Python 3
- Django
- Django REST Framework (DRF)
- SQLite (yoki boshqa DB)
- Swagger / Redoc (API hujjatlari uchun)
- Postman Collection
- Deploy: **Hozircha faqat GitHub’da mavjud**

---

## 🔐 Kirish va Ro‘yxatdan o‘tish

- Foydalanuvchi ro‘yxatdan o‘tgach, **OTP (tasdiqlovchi kod)** email orqali yuboriladi.
- Agar OTP xabari emailda ko‘rinmasa, **Spam yoki Promotions** bo‘limlarini tekshiring.
- Email orqali tasdiqlangandan keyingina tizimga kirish mumkin.

---

## 🚀 API funksiyalari

- 🟢 **Daromadlar (Income)** – CRUD
- 🔴 **Harajatlar (Expense)** – CRUD
- 🏷️ **Kategoriyalar** – Foydalanuvchiga xos CRUD
- 📊 **Statistik tahlillar**:
  - Haftalik / Oylik / Yillik daromad/harajatlar statistikasi
  - Diagramma formatida JSON responselar

---

## 📑 API Dokumentatsiyasi (local holatda)

- 🔵 Swagger: [`http://127.0.0.1:8000/swagger/`](http://127.0.0.1:8000/swagger/)
- 🔴 Redoc: [`http://127.0.0.1:8000/redoc/`](http://127.0.0.1:8000/redoc/)
- 🟠 Postman: [`postman_collection.json`](./postman_collection.json)


🌐 Onlayn hujjat:
[📎 Postman online hujjati bu yerda](https://documenter.getpostman.com/view/43380057/2sB2qUo53F)


---

## 📂 O‘rnatish yo‘riqnomasi (Local versiyada)


1. Loyihani klon qiling:
git clone cd money-pall

2.Virtual muhit yarating va faollashtiring:

python -m venv venv source venv/bin/activate

3.Kutubxonalarni o‘rnating: pip install -r requirements.txt

4.Migratsiyalarni bajaring: python manage.py makemigrations python manage.py migrate

5.Superuser yarating (admin panel uchun): python manage.py createsuperuser

6.Serverni ishga tushiring: python manage.py runserver
