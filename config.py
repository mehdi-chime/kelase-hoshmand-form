# -*- coding: utf-8 -*-
"""config.py - تنظیمات پروژه"""

SCHOOLS = {
    "زارع": {
        "هفت الف": "https://eitaa.com/joinchat/44041983C3a3b1d9f08",
        "هفت ب":  "https://eitaa.com/joinchat/56493823C7d5eb3cb74",
        "هفت ج":  "https://eitaa.com/joinchat/63833855C64df43498e",
        "هفت د":  "https://eitaa.com/joinchat/86050559C015ffe2cd2",
    },
    "نوردانش": {
        "هشت الف": "https://eitaa.com/joinchat/117114623Cb7784ff8f1",
        "هشت ب":  "https://eitaa.com/joinchat/127796991C0d82c790b7",
        "هشت ج":  "https://eitaa.com/joinchat/138151679C767a8a78ea",
        "هفت ج":  "https://eitaa.com/joinchat/151652095C3f8053c1bd",
    },
}

FORM_TITLE = "ثبت نام کلاس علوم"
FORM_DESCRIPTION = "لطفا اطلاعات خود را با دقت وارد کنید"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "change-me-please"

DB_PATH = "data/students.db"


def get_schools():
    return list(SCHOOLS.keys())


def get_classes(school):
    if school not in SCHOOLS:
        return []
    return list(SCHOOLS[school].keys())


def get_channel_link(school, class_name):
    if school not in SCHOOLS:
        return None
    if class_name not in SCHOOLS[school]:
        return None
    return SCHOOLS[school][class_name]
