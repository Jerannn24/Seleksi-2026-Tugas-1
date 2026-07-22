# Import library yang dibutuhkan
import requests
import time
from bs4 import BeautifulSoup
from utility import extract_price, extract_review, format_date 

from constant import MAIN_URL, GAME_URL, COOKIES, HEADERS
# Headers untuk memperkenalkan diri

def scrape_steam():
    headers = HEADERS
    cookies = COOKIES

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
        url = MAIN_URL.format(start=start)
        
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
            
            newUrl = GAME_URL.format(game_id=game_id)
            
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
            price = extract_price(price) 
            
            release_date_tag = soup2.find("div", class_="date")
            release_date = format_date(release_date_tag.text.strip()) if release_date_tag else None
            
            review_tag = soup2.find("span", class_="responsive_reviewdesc_short")
            
            review_count = extract_review(review_tag)

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
        #     break
        # break
    # Mengembalikan semua data yang telah di-scrape
    return data_games, genre, game_genres, tags, game_tags, developers, game_developers, publishers, game_publishers
