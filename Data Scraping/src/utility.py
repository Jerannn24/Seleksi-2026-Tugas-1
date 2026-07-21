from datetime import datetime

def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d %b, %Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return None