# -*- coding: utf-8 -*-
"""app.py - Flask app اصلی"""

import os
import sqlite3
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, send_file,
)

import config


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")


def get_db():
    db_path = config.DB_PATH
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            national_id TEXT NOT NULL,
            eitaa_number TEXT NOT NULL,
            school TEXT NOT NULL,
            class_name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    return render_template(
        "index.html",
        form_title=config.FORM_TITLE,
        form_description=config.FORM_DESCRIPTION,
        schools=config.SCHOOLS,
    )


@app.route("/submit", methods=["POST"])
def submit():
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    national_id = request.form.get("national_id", "").strip()
    eitaa_number = request.form.get("eitaa_number", "").strip()
    school = request.form.get("school", "").strip()
    class_name = request.form.get("class_name", "").strip()

    if not all([first_name, last_name, national_id, eitaa_number, school, class_name]):
        flash("لطفا همه فیلدها را پر کنید", "error")
        return redirect(url_for("index"))

    if school not in config.SCHOOLS:
        flash("مدرسه انتخاب شده معتبر نیست", "error")
        return redirect(url_for("index"))

    if class_name not in config.SCHOOLS[school]:
        flash("کلاس انتخاب شده معتبر نیست", "error")
        return redirect(url_for("index"))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students
        (first_name, last_name, national_id, eitaa_number, school, class_name, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (first_name, last_name, national_id, eitaa_number, school, class_name, datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return redirect(url_for("success", school=school, class_name=class_name))


@app.route("/success")
def success():
    school = request.args.get("school", "")
    class_name = request.args.get("class_name", "")
    channel_link = config.get_channel_link(school, class_name)
    return render_template(
        "success.html",
        school=school,
        class_name=class_name,
        channel_link=channel_link,
    )


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("نام کاربری یا رمز عبور اشتباه است", "error")

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))


@app.route("/admin")
@login_required
def admin_dashboard():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY created_at DESC")
    students = cursor.fetchall()
    conn.close()
    return render_template("admin.html", students=students, schools=config.SCHOOLS)


@app.route("/admin/export")
@login_required
def admin_export():
    import csv
    import io

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY created_at DESC")
    students = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "نام", "فامیل", "کد ملی", "شماره ایتا", "مدرسه", "کلاس", "زمان ثبت"])

    for s in students:
        writer.writerow([s["id"], s["first_name"], s["last_name"], s["national_id"],
                        s["eitaa_number"], s["school"], s["class_name"], s["created_at"]])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8-sig")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="students.csv",
    )


init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
