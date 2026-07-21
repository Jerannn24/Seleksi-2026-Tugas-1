import json

import mysql.connector
from mysql.connector import Error
from database import create_database


conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123',
)

cursor = conn.cursor()

create_database(cursor)

loc = '../Data Scraping/data/'

# input data developers.json
with open(f'{loc}developers.json', 'r') as file:
    developers_data = json.load(file)
    
for developer in developers_data:
    dev_name = developer['name']
    dev_id = developer['dev_id']
    
    cursor.execute("""
        INSERT INTO Developers (dev_id, dev_name)
        VALUES (%s, %s)
    """, (dev_id, dev_name))

# input data publishers.json
with open(f'{loc}publishers.json', 'r') as file:
    publishers_data = json.load(file)

for publisher in publishers_data:
    pub_name = publisher['name']
    pub_id = publisher['pub_id']

    cursor.execute("""
        INSERT INTO Publishers (pub_id, pub_name)
        VALUES (%s, %s)
    """, (pub_id, pub_name))

# input data games_data.json
with open(f'{loc}games.json', 'r') as file:
    games_data = json.load(file)

for game in games_data:
    id = game['game_id']
    title = game['title']
    price = game['price']
   
    release_date = game['release_date']
    review_summary = game['review_summary']
    review_count = game['review_count']
    game_url = game['game_url']
    dev_id = game['dev_id']
    pub_id = game['pub_id']

    cursor.execute("""
        INSERT INTO Games (id, title, price, release_date, review_summary, review_count, game_url, dev_id, pub_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (id, title, price, release_date, review_summary, review_count, game_url, dev_id, pub_id))

# input data genres.json
with open(f'{loc}genres.json', 'r') as file:
    genres_data = json.load(file)
    
for genre in genres_data:
    genre_name = genre['name']
    genre_id = genre['genre_id']
    
    cursor.execute("""
        INSERT INTO Genres (genre_id, genre_name)
        VALUES (%s, %s)
    """, (genre_id, genre_name))

# input data game_genres.json
with open(f'{loc}game_genres.json', 'r') as file:
    game_genres_data = json.load(file)
    
for game_genre in game_genres_data:
    game_id = game_genre['game_id']
    genre_id = game_genre['genre_id']
    
    cursor.execute("""
        INSERT INTO GameGenres (game_id, genre_id)
        VALUES (%s, %s)
    """, (game_id, genre_id))
    
# input data tags.json
with open(f'{loc}tags.json', 'r') as file:
    tags_data = json.load(file)
    
for tag in tags_data:
    tag_name = tag['name']
    tag_id = tag['tag_id']
    
    cursor.execute("""
        INSERT INTO Tags (tag_id, tag_name)
        VALUES (%s, %s)
    """, (tag_id, tag_name))
    
# input data game_tags.json
with open(f'{loc}game_tags.json', 'r') as file:
    game_tags_data = json.load(file)
    
for game_tag in game_tags_data:
    game_id = game_tag['game_id']
    tag_id = game_tag['tag_id']
    
    cursor.execute("""
        INSERT INTO GameTags (game_id, tag_id)
        VALUES (%s, %s)
    """, (game_id, tag_id))

conn.commit()
cursor.close()
conn.close()