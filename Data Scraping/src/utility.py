from datetime import datetime
import re

def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d %b, %Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return None
    
def extract_price(price_str):
    if 'Rp' in price_str:
        return float(re.sub(r'[^\d.]', '', price_str))
    else:
        return 0.00
    
def extract_review(review_tag):
    if review_tag:
        text = review_tag.get_text(" ", strip=True)
        match = re.search(r'of\s+([\d,]+)', text)
        if match:
            return int(match.group(1).replace(",", ""))
    return 0