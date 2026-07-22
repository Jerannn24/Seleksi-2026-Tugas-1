import mysql.connector
from mysql.connector import Error
from warehouse import create_warehouse

# Utility function to Help



# Main Logic
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123',
    database='SteamGames'
)

dw_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123',
)


cursor = conn.cursor(dictionary=True)
dw_cursor = dw_conn.cursor()

create_warehouse(dw_cursor)

# Ambil data dari tabel-tabel di database SteamGames
cursor.execute("SELECT * FROM Games")
games = cursor.fetchall()

cursor.execute("SELECT * FROM Developers")
developers = cursor.fetchall()

cursor.execute("SELECT * FROM Publishers")
publishers = cursor.fetchall()

cursor.execute("SELECT * FROM Tags")
tags = cursor.fetchall()

cursor.execute("SELECT * FROM GameTags")
game_tags = cursor.fetchall()

cursor.execute("SELECT * FROM Genres")
genres = cursor.fetchall()

cursor.execute("SELECT * FROM GameGenres")
game_genres = cursor.fetchall()

cursor.execute("SELECT DISTINCT release_date FROM Games WHERE release_date IS NOT NULL")
release_dates = cursor.fetchall()

dw_cursor.execute("""USE WarehouseDB""")

# Masukkan data ke dalam tabel-tabel di data warehouse
for developer in developers:
    # Insert data into dim_developer
    dw_cursor.execute("""
    INSERT INTO dim_developer (dev_id, dev_name)
        VALUES (%s, %s)
    """, (developer['dev_id'], developer['dev_name']))

for publisher in publishers:
    # Insert data into dim_publisher
    dw_cursor.execute("""
    INSERT INTO dim_publisher (pub_id, pub_name)
        VALUES (%s, %s)
    """, (publisher['pub_id'], publisher['pub_name']))
    
for genre in genres:
    # Insert data into dim_genre
    dw_cursor.execute("""
    INSERT INTO dim_genre (genre_id, genre_name)
        VALUES (%s, %s)
    """, (genre['genre_id'], genre['genre_name']))

for tag in tags:
    # Insert data into dim_tag
    dw_cursor.execute("""
    INSERT INTO dim_tag (tag_id, tag_name)
        VALUES (%s, %s)
    """, (tag['tag_id'], tag['tag_name']))

for release_date in release_dates:
    # Insert data into dim_date
    d = release_date['release_date']
    
    dw_cursor.execute("""
    INSERT INTO dim_date (release_date, day, month, year, quarter)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        d, 
        d.day, 
        d.month, 
        d.year, 
        (d.month - 1)// 3 + 1  
    ))

for game in games:
    is_free = True if game['price'] == 0.0 else False
    
    # Insert data into dim_game
    dw_cursor.execute("""
    INSERT INTO dim_game (game_id, title, game_url, is_Free)
        VALUES (%s, %s, %s, %s)
    """, (game['id'], game['title'], game['game_url'], is_free))
    
    # Insert data into fact_game           
    dw_cursor.execute("""
    INSERT INTO fact_game (game_id, dev_id, pub_id, release_date, review_count, price)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (game['id'], game['dev_id'], game['pub_id'], game['release_date'], game['review_count'], game['price']))


for game_genre in game_genres:
    # Insert data into dim_gamegenre
    dw_cursor.execute("""
    INSERT INTO dim_gamegenre (game_id, genre_id)
        VALUES (%s, %s)
    """, (game_genre['game_id'], game_genre['genre_id']))

for game_tag in game_tags:
    # Insert data into dim_gametag
    dw_cursor.execute("""
    INSERT INTO dim_gametag (game_id, tag_id)
        VALUES (%s, %s)
    """, (game_tag['game_id'], game_tag['tag_id']))

print("Data warehouse created and populated successfully.")

conn.commit()
cursor.close()
conn.close()
dw_conn.commit()
dw_cursor.close()
dw_conn.close()