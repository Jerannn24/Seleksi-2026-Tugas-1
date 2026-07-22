# Function untuk membuat database dan tabel-tabel yang diperlukan
def create_warehouse(cursor):
    # Drop database jika sudah ada dan buat database baru
    cursor.execute("CREATE DATABASE IF NOT EXISTS WarehouseDB")

    # Gunakan database yang telah dibuat
    cursor.execute("USE WarehouseDB")

    # Buat tabel-tabel yang diperlukan
    
    # Tabel untuk menyimpan data dimensi game
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_game (
        game_id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        game_url VARCHAR(255) NOT NULL,
        is_Free Boolean NOT NULL
    )
    """)

    # Tabel untuk menyimpan data dimensi publisher
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_publisher (
        pub_id INT AUTO_INCREMENT PRIMARY KEY,
        pub_name VARCHAR(255) NOT NULL
    )
    """)
    
    # Tabel untuk menyimpan data dimensi developer
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_developer (
        dev_id INT AUTO_INCREMENT PRIMARY KEY,
        dev_name VARCHAR(255) NOT NULL
    )
    """)
    
    # Tabel untuk menyimpan data dimensi tanggal
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_date (
        release_date DATE PRIMARY KEY,
        day INT NOT NULL,
        month INT NOT NULL,
        year INT NOT NULL,
        quarter INT NOT NULL
    )
    """)
    
    # Tabel untuk menyimpan data game 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fact_game (
        fact_id INT AUTO_INCREMENT PRIMARY KEY,
        
        game_id INT NOT NULL,
        dev_id INT NOT NULL,
        pub_id INT NOT NULL,
        release_date DATE,
        
        review_count INT NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        
        FOREIGN KEY (dev_id) REFERENCES dim_developer(dev_id),
        FOREIGN KEY (pub_id) REFERENCES dim_publisher(pub_id),
        FOREIGN KEY (game_id) REFERENCES dim_game(game_id),
        FOREIGN KEY (release_date) REFERENCES dim_date(release_date)
    )
    """)

    # Tabel untuk menyimpan data genre dan relasinya dengan game
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_genre (
        genre_id INT AUTO_INCREMENT PRIMARY KEY,
        genre_name VARCHAR(255) NOT NULL
    )
    """)

    # Tabel untuk menyimpan relasi antara game dan genre
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_gamegenre (
        game_id INT NOT NULL,
        genre_id INT NOT NULL,
        
        PRIMARY KEY (game_id, genre_id),
        FOREIGN KEY (game_id) REFERENCES fact_game(game_id),
        FOREIGN KEY (genre_id) REFERENCES dim_genre(genre_id)
    )
    """)

    # Tabel untuk menyimpan data tag dan relasinya dengan game
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_tag (
        tag_id INT AUTO_INCREMENT PRIMARY KEY,
        tag_name VARCHAR(255) NOT NULL
    )
    """)

    # Tabel untuk menyimpan relasi antara game dan tag
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_gametag (
        game_id INT NOT NULL,
        tag_id INT NOT NULL,
        
        PRIMARY KEY (game_id, tag_id),
        FOREIGN KEY (game_id) REFERENCES fact_game(game_id),
        FOREIGN KEY (tag_id) REFERENCES dim_tag(tag_id)
    )""")



