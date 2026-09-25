# کلاس هوشمند - فرم ثبت نام

فرم ثبت نام دانش آموزان با هدایت خودکار به کانال ایتا کلاس.

## ویژگی ها

- فرم پویا (انتخاب مدرسه باعث نمایش کلاس های همان مدرسه می شود)
- ذخیره داده ها در SQLite
- هدایت به کانال ایتا کلاس مربوطه
- پنل ادمین با خروجی CSV
- بدون نیاز به Google یا فیلترشکن

## نصب و اجرا (محلی)

    pip install -r requirements.txt
    python app.py

سپس در مرورگر باز کنید: http://localhost:5000

## دسترسی ادمین

    آدرس: /admin/login
    نام کاربری: admin
    رمز عبور: change-me-please

هشدار: رمز عبور را در config.py عوض کنید.

## Deploy روی Render

1. کد را در GitHub آپلود کنید
2. در render.com حساب بسازید
3. New - Web Service - انتخاب repo
4. Render خودکار deploy می کند

## ساختار پروژه

    app.py              Flask app
    config.py           تنظیمات و لیست کانال ها
    templates/          قالب های HTML
    static/             CSS
    data/               دیتابیس SQLite
    requirements.txt    کتابخانه ها
    render.yaml         تنظیمات Render

## سازنده

سید مهدی جلالی
GitHub: mehdi-chime
