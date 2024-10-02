from datetime import datetime, timedelta

def excel_serial_to_datetime(serial):
    base_date = datetime(1899, 12, 30)
    return base_date + timedelta(days=int(serial))