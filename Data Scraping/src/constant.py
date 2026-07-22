from pathlib import Path

MAIN_URL = "https://store.steampowered.com/search?start={start}&ndl=1"
GAME_URL = "https://store.steampowered.com/app/{game_id}"

COOKIES = {
    'birthtime' : '0',
    'mature_content' : '1',
    'lastagecheckage' : '1-January-1988',
}

HEADERS = {
    'user-agent' : 'Mozilla/5.0 (Xll; Linux x86_64) ; Basis Data/Seleksi Basis Data 2026/ 13524055@std.stei.itb.ac.id'
}

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data' 