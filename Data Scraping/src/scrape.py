# Import library yang dibutuhkan
import json
import re
import requests
import time
from bs4 import BeautifulSoup
from utility import format_date 

# Headers untuk memperkenalkan diri
headers = {
    'user-agent' : 'Mozilla/5.0 (Xll; Linux x86_64) ; Basis Data/Seleksi Basis Data 2026/ 13524055@std.stei.itb.ac.id'
}

cookies = {
    'birthtime' : '0',
    'mature_content' : '1',
    'lastagecheckage' : '1-January-1988',
}
# List untuk menyimpan data game
data_games = []
games_id = set()
# List untuk menyimpan data developer 
developers = set()
game_developers = []

# List untuk menyimpan data publisher
game_publishers = []
publishers = set()

# List untuk menyimpan data genre dan tag
game_genres = []
genre = set()

# List untuk menyimpan data tag
game_tags = []
tags = set()

for start in range (0, 200, 50):
    # dynamic URL Website yang akan di scrape
    url = f"https://store.steampowered.com/search?start={start}&ndl=1"
    
    res = requests.get(url, headers=headers, cookies=cookies)

    # BeautifulSoup untuk parsing HTML
    soup = BeautifulSoup(res.content, 'html.parser')

    # Mengambil 50 game dari halaman pencarian
    games = soup.find_all('a', class_='search_result_row')
    
    
    for game in games:
        title = game.find('span', class_='title').text
        print(f"Sedang di proses... {title}")
        game_id = game.get("data-ds-appid")
        # Skip game jika sudah pernah di-scrape
        if game_id in games_id:
            continue
        
        games_id.add(game_id)
        
        newUrl = f"https://store.steampowered.com/app/{game_id}"
        
        # Mengambil data detail game dari halaman detail game
        try:
            res2 = requests.get(newUrl, headers=headers, cookies=cookies)
        except:
            print(f"Gagal mengambil data untuk game: {title}")
            continue

        soup2 = BeautifulSoup(res2.content, 'html.parser')

        # Mengambil data game seperti harga, release date, review summary, review count, image url, game_url, description
        price_tag = soup2.find("div", class_="game_purchase_price")
        price = price_tag.text.strip() if price_tag else "Free To Play"
        if 'Rp' in price:
            price = float(re.sub(r'[^\d.]', '', price))
        else:
            price = 0.00
        release_date_tag = soup2.find("div", class_="date")
        release_date = format_date(release_date_tag.text.strip()) if release_date_tag else None
        
        review_tag = soup2.find("span", class_="responsive_reviewdesc_short")
        
        if review_tag:
            text = review_tag.get_text(" ", strip=True)

            match = re.search(r'of\s+([\d,]+)', text)

            if match:
                review_count = int(match.group(1).replace(",", ""))
            else:
                review_count = 0
        else:
            review_count = 0

        review_summary_tag = soup2.find("span", class_="game_review_summary")
        review_summary = review_summary_tag.text.strip() if review_summary_tag else None
        
        
        # Mengambil genre dari halaman detail game dan membatasi hanya 5 genre
        temp_genres = [
            genre.text.strip()
            for genre in soup2.find_all("a", href=lambda href: href and "/genre/" in href)
        ][:5]
        
        # Menambahkan genre ke dalam game_genres
        game_genres.append({
            "game_id": game_id,
            "genres": temp_genres
        })
        
        # Menambahkan genre ke dalam set genre
        for temp in temp_genres:
            genre.add(temp)
        
        # Mengambil tag populer (berdasarkan user) dari halaman detail game dan membatasi hanya 10 tag
        temp_tags = [
            tag.text.strip()
            for tag in soup2.find_all("a", class_="app_tag")
        ][:10]  
          
        # Delay untuk menghindari terlalu banyak request dalam waktu singkat
        game_tags.append({
            "game_id": game_id,
            "tags": temp_tags
        })
        
        # Menambahkan tag ke dalam set tags
        for tag in temp_tags:
            tags.add(tag)
            
        # Mengambil developer dari halaman detail game, jika tidak ditemukan maka akan diisi dengan None
        dev_tag = soup2.find("a", href=lambda href: href and "/developer/" in href)
        dev = dev_tag.text.strip() if dev_tag else "Unknown"
        
        developers.add(dev)
        
        game_developers.append({
            "game_id": game_id,
            "developer": dev
        })
        
        # Mengambil publisher dari halaman detail game, jika tidak ditemukan maka akan diisi dengan None
        pub_tag = soup2.find("a", href=lambda href: href and "/publisher/" in href)
        pub = pub_tag.text.strip() if pub_tag else "Unknown"

        publishers.add(pub)
        
        game_publishers.append({
            "game_id": game_id,
            "publisher": pub
        })
        
        data_games.append({
            "game_id": game_id,
            "title": title,
            "price": price,
            "release_date": release_date,
            "review_summary": review_summary,
            "review_count": review_count,
            "game_url": newUrl,
        })
        
        time.sleep(0.5)
        # break
    # break

# Menyimpan data ke dalam file JSON
with open('data/games.json', 'w', encoding='utf-8') as f:
    json.dump(data_games, f, ensure_ascii=False, indent=4)
   
   
# Menyimpan data genre ke dalam file JSON
genre_json = []
for genre_id, genre_name in enumerate(sorted(genre), start=1):
    genre_json.append({
        "genre_id": genre_id,
        "name": genre_name
    })

with open('data/genres.json', 'w', encoding='utf-8') as f:
    json.dump(genre_json, f, ensure_ascii=False, indent=4)
    
# Menyimpan data game_genres ke dalam file JSON
game_genres_json = []
for game_genre in game_genres:
    for genre in game_genre["genres"]:
        # Mencari genre_id dari genre_json
        genre_id = next((g["genre_id"] for g in genre_json if g["name"] == genre), None)
        if genre_id is not None:
            game_genres_json.append({
                "game_id": game_genre["game_id"],
                "genre_id": genre_id
            })

with open('data/game_genres.json', 'w', encoding='utf-8') as f:
    json.dump(game_genres_json, f, ensure_ascii=False, indent=4)
    
# Mengubah set tags menjadi list of dictionary dengan tag_id dan name
tags_list = []
for tag_id, tag_name in enumerate(sorted(tags), start=1):
    tags_list.append({
        "tag_id": tag_id,
        "name": tag_name
    })
    
with open('data/tags.json', 'w', encoding='utf-8') as f:
    json.dump(list(tags_list), f, ensure_ascii=False, indent=4)
    
# mengubah game_tags menjadi list of dictionary dengan game_id dan tag_id
game_tags_json = []

for game_tag in game_tags:
    for tag in game_tag["tags"]:
        # Mencari tag_id dari tags_list
        tag_id = next((t["tag_id"] for t in tags_list if t["name"] == tag), None)
        if tag_id is not None:
            game_tags_json.append({
                "game_id": game_tag["game_id"],
                "tag_id": tag_id
            })

# Menyimpan game_tags ke dalam file JSON
with open('data/game_tags.json', 'w', encoding='utf-8') as f:
    json.dump(game_tags_json, f, ensure_ascii=False, indent=4)
     
# Menyimpan data developer ke dalam file JSON
dev_json = []
for dev_id, dev_name in enumerate(sorted(developers), start=1):
    dev_json.append({
        "dev_id": dev_id,
        "name": dev_name
    })

with open('data/developers.json', 'w', encoding='utf-8') as f:
    json.dump(dev_json, f, ensure_ascii=False, indent=4)

# Menyimpan data id developer dan game_id ke list of dictionary dengan game_id dan dev_id
game_dev_dict = []
for game_dev in game_developers:
    # Mencari dev_id dari dev_json
    dev_id = next((d["dev_id"] for d in dev_json if d["name"] == game_dev["developer"]), None)
    if dev_id is not None:
        game_dev_dict.append({
            "game_id": game_dev["game_id"],
            "dev_id": dev_id
        })

# Menyimpan publisher ke dalam file JSON
pub_json = []
for pub_id, pub_name in enumerate(sorted(publishers), start=1):
    pub_json.append({
        "pub_id": pub_id,
        "name": pub_name
    })

with open('data/publishers.json', 'w', encoding='utf-8') as f:
    json.dump(pub_json, f, ensure_ascii=False, indent=4)

# Menyimpan data id publisher dan game_id ke list of dictionary dengan game_id dan pub_id
game_pub_dict = []
for game_pub in game_publishers:
    # Mencari pub_id dari pub_json
    pub_id = next((p["pub_id"] for p in pub_json if p["name"] == game_pub["publisher"]), None)

    if pub_id is not None:
        game_pub_dict.append({
            "game_id": game_pub["game_id"],
            "pub_id": pub_id
        })
        
# Menambah ID dev dan ID pub ke dalam data_games
for game in data_games:
    # Mencari dev_id dari game_dev_dict
    dev_id = next((gd["dev_id"] for gd in game_dev_dict if gd["game_id"] == game["game_id"]), None)
    if dev_id is not None:
        game["dev_id"] = dev_id
    
    # Mencari pub_id dari game_pub_dict
    pub_id = next((gp["pub_id"] for gp in game_pub_dict if gp["game_id"] == game["game_id"]), None)
    if pub_id is not None:
        game["pub_id"] = pub_id

with open('data/games.json', 'w', encoding='utf-8') as f:
    json.dump(data_games, f, ensure_ascii=False, indent=4)
    
print(f"Data {len(data_games)} games berhasil disimpan ke dalam file games.json")