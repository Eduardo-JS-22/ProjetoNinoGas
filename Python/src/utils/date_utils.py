from datetime import datetime, timedelta

def get_current_date():
    return datetime.now().date()

def get_custom_date(date):
    return datetime.strptime(date, "%Y-%m-%d")

def get_date_after_days(days):
    return datetime.now().date() + timedelta(days=days)

def get_custom_date_after_days(date, days):
    return date + timedelta(days=days)