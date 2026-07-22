from scraper import scrape_steam
from exporter import save_json
from mapper import build_genres, build_game_genres, build_tags, build_game_tags, build_developers, build_game_developers, build_publishers, build_game_publishers, build_games

# Main Logic
def main():
    print("Starting the data scraping and warehouse creation process...")
    # Scrape data from Steam
    data_games, genres, game_genres, tags, game_tags, developers, game_developers, publishers, game_publishers = scrape_steam()

    # Map the scraped data to JSON format
    genres_json = build_genres(genres)
    game_genres_json = build_game_genres(game_genres, genres_json)
    tags_json = build_tags(tags)
    game_tags_json = build_game_tags(game_tags, tags_json)
    developers_json = build_developers(developers)
    game_developers_json = build_game_developers(game_developers, developers_json)
    publishers_json = build_publishers(publishers)
    game_publishers_json = build_game_publishers(game_publishers, publishers_json)
    games_json = build_games(data_games, game_developers_json, game_publishers_json)

    # Save the processed data to JSON files
    save_json("genres.json", genres_json)
    save_json("game_genres.json", game_genres_json)
    save_json("tags.json", tags_json)
    save_json("game_tags.json", game_tags_json)
    save_json("developers.json", developers_json)
    save_json("publishers.json", publishers_json)
    save_json("games.json", games_json)

if __name__ == "__main__":
    main()
