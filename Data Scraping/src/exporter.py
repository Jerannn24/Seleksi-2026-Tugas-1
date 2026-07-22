
import json
from constant import DATA_DIR

# Function to save data to JSON files
def save_json(filename, data):
    with open(DATA_DIR / filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)