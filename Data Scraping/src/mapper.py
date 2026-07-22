# Membuat fungsi untuk membangun genre_json
def build_genres(genres):
    genre_json = []
    for genre_id, genre_name in enumerate(sorted(genres), start=1):
        genre_json.append({
            "genre_id": genre_id,
            "name": genre_name
        })
    return genre_json   

# Membuat fungsi untuk membangun game_genres_json
def build_game_genres(game_genres, genre_json):
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
    return game_genres_json

# Membuat fungsi untuk membangun tags_list
def build_tags(tags):
    tags_list = []
    for tag_id, tag_name in enumerate(sorted(tags), start=1):
        tags_list.append({
            "tag_id": tag_id,
            "name": tag_name
        })
    return tags_list

# Membuat fungsi untuk membangun game_tags_json
def build_game_tags(game_tags, tags_list):
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
    return game_tags_json

# Membuat fungsi untuk membangun developers_json
def build_developers(developers):
    dev_json = []
    for dev_id, dev_name in enumerate(sorted(developers), start=1):
        dev_json.append({
            "dev_id": dev_id,
            "name": dev_name
        })
    return dev_json

# Membuat fungsi untuk membangun game_developers_json
def build_game_developers(game_developers, dev_json):
    game_developers_json = []
    for game_dev in game_developers:
        # Mencari dev_id dari dev_json
        dev_id = next((d["dev_id"] for d in dev_json if d["name"] == game_dev["developer"]), None)
        if dev_id is not None:
            game_developers_json.append({
                "game_id": game_dev["game_id"],
                "dev_id": dev_id
            })
    return game_developers_json

# Membuat fungsi untuk membangun publishers_json
def build_publishers(publishers):
    pub_json = []
    for pub_id, pub_name in enumerate(sorted(publishers), start=1):
        pub_json.append({
            "pub_id": pub_id,
            "name": pub_name
        })
    return pub_json

# Membuat fungsi untuk membangun game_publishers_json
def build_game_publishers(game_publishers, pub_json):
    game_publishers_json = []
    for game_pub in game_publishers:
        # Mencari pub_id dari pub_json
        pub_id = next((p["pub_id"] for p in pub_json if p["name"] == game_pub["publisher"]), None)
        if pub_id is not None:
            game_publishers_json.append({
                "game_id": game_pub["game_id"],
                "pub_id": pub_id
            })
    return game_publishers_json

# Membuat fungsi untuk membangun data_games dengan dev_id dan pub_id
def build_games(data_games, game_dev_json, game_pub_json):
    for game in data_games:
        # Mencari dev_id dari game_dev_json
        dev_id = next((gd["dev_id"] for gd in game_dev_json if gd["game_id"] == game["game_id"]), None)
        # Mencari pub_id dari game_pub_json
        pub_id = next((gp["pub_id"] for gp in game_pub_json if gp["game_id"] == game["game_id"]), None)
        
        game["dev_id"] = dev_id
        game["pub_id"] = pub_id
    return data_games

