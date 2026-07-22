# Function untuk membuat database dan tabel-tabel yang diperlukan
def create_database(cursor):
    # Drop database jika sudah ada dan buat database baru
    cursor.execute("CREATE DATABASE IF NOT EXISTS SteamGames")

    # Gunakan database yang telah dibuat
    cursor.execute("USE SteamGames")

    # Buat tabel-tabel yang diperlukan
    
    # Tabel untuk menyimpan data developer
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Developers (
        dev_id INT AUTO_INCREMENT PRIMARY KEY,
        dev_name VARCHAR(255) NOT NULL
    )
    """)

    # Tabel untuk menyimpan data publisher
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Publishers (
        pub_id INT AUTO_INCREMENT PRIMARY KEY,
        pub_name VARCHAR(255) NOT NULL
    )
    """)
    
    # Tabel untuk menyimpan data game 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Games (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        release_date DATE,
        review_summary VARCHAR(255),
        review_count INT NOT NULL,
        game_url VARCHAR(255) NOT NULL,
        dev_id INT NOT NULL,
        pub_id INT NOT NULL,
        
        FOREIGN KEY (dev_id) REFERENCES Developers(dev_id),
        FOREIGN KEY (pub_id) REFERENCES Publishers(pub_id)
    )
    """)

    # Tabel untuk menyimpan data genre dan relasinya dengan game
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Genres (
        genre_id INT AUTO_INCREMENT PRIMARY KEY,
        genre_name VARCHAR(255) NOT NULL
    )
    """)

    # Tabel untuk menyimpan relasi antara game dan genre
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS GameGenres (
        game_id INT NOT NULL,
        genre_id INT NOT NULL,
        
        PRIMARY KEY (game_id, genre_id),
        FOREIGN KEY (game_id) REFERENCES Games(id),
        FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
    )
    """)

    # Tabel untuk menyimpan data tag dan relasinya dengan game
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Tags(
        tag_id INT AUTO_INCREMENT PRIMARY KEY,
        tag_name VARCHAR(255) NOT NULL
    )
    """)

    # Tabel untuk menyimpan relasi antara game dan tag
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS GameTags (
        game_id INT NOT NULL,
        tag_id INT NOT NULL,
        
        PRIMARY KEY (game_id, tag_id),
        FOREIGN KEY (game_id) REFERENCES Games(id),
        FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
    )""")

    # Tambahan tabel yang tidak menyimpan data, hanya untuk relasi

    # Tabel untuk menyimpan data achievement dan relasinya dengan game
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Achievements (
        achievement_id INT AUTO_INCREMENT PRIMARY KEY,
        game_id INT NOT NULL,
        achievement_name VARCHAR(255) NOT NULL,
        badge_img VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        FOREIGN KEY (game_id) REFERENCES Games(id)
    )"""
    )

    # Tabel untuk menyimpan data user dan relasinya dengan game
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        country VARCHAR(255) NOT NULL,
        state VARCHAR(255) NOT NULL,
        profile_picture VARCHAR(255) NOT NULL,
        UNIQUE (username),
        UNIQUE (email)
    )"""
    )

    # Tabel untuk menyimpan data wallet user
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Wallet (
        user_id INT NOT NULL PRIMARY KEY,
        currency VARCHAR(10) NOT NULL,
        balance DECIMAL(10, 2) NOT NULL
    )"""
    )

    # Tabel untuk menyimpan data library user
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Library (
        game_id INT NOT NULL,
        user_id INT NOT NULL,
        purchase_date DATE NOT NULL,
        played_time INT NOT NULL,
        last_played_date DATE NOT NULL,
        installed BOOLEAN NOT NULL,
        
        PRIMARY KEY (game_id, user_id),
        FOREIGN KEY (game_id) REFERENCES Games(id),
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )"""
    )

    # Tabel untuk menyimpan data transaksi user
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Transactions (
        transaction_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        game_id INT NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        type ENUM('purchase', 'refund') NOT NULL,
        payment_method ENUM('credit_card', 'paypal', 'bank_transfer') NOT NULL,
        created_at DATE NOT NULL,
        
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (game_id) REFERENCES Games(id),

        CONSTRAINT unique_transaction UNIQUE (user_id, game_id, created_at) 
    )"""
    )



