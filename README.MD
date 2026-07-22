# Steam Games ETL Project

---

# Author

- Nama: <b>Junior Natra Situmorang</b>
- NIM: <b>13524055</b>


---

# Deskripsi Project

Project ini merupakan implementasi proses ETL untuk data permainan dari Steam Store. Data dikumpulkan melalui scraping halaman pencarian dan halaman detail game, lalu diproses menjadi beberapa file JSON. Hasil JSON tersebut kemudian dimasukkan ke dalam basis data relasional, dan sebagian datanya juga digunakan untuk membangun data warehouse.

Topik "Data 200 Game yang dipublikasikan berdasarkan relevansi pencarian di Steam" dipilih karena data yang tersedia cukup menarik untuk diproses dan dianalisis, misalnya harga game, tanggal rilis, ringkasan review, jumlah review, developer, publisher, genre, dan tag. Dari data tersebut dapat diperoleh informasi seperti distribusi game gratis dan berbayar, game dengan review tinggi, pola genre yang sering muncul, Genre game dengan review positif oleh player.

DBMS yang digunakan pada tahap storing dan warehouse adalah MySQL/MariaDB. Database operasional dipakai untuk menyimpan data hasil scraping, sedangkan warehouse dipakai untuk mempercepat proses analisis data.

---

# Struktur Folder Project

## `Data Scraping`

Folder ini berisi source code scraping dan hasil data yang sudah diproses menjadi JSON. Folder `src` menyimpan script Python, sedangkan folder `data` menyimpan file JSON hasil scraping.

## `Data Storing`

Folder ini berisi script untuk membuat database relasional dan memasukkan data JSON ke tabel MySQL/MariaDB. Folder `design` menyimpan ERD dan diagram relasional, folder `export` menyimpan dump SQL, dan folder `screenshot` menyimpan bukti isi tabel database.

## `Data Warehous`

Folder ini berisi script untuk membangun data warehouse dari database operasional. Folder `design` menyimpan diagram warehouse, folder `export` menyimpan dump SQL warehouse, dan folder `screenshot` menyimpan bukti isi tabel serta query analitik. Nama folder mengikuti repository asli, yaitu `Data Warehous`.

## `src`

Setiap bagian project memiliki folder `src` yang berisi script Python utama.

- `Data Scraping/src` berisi file yang di run saat ingin melakukan scraping data, `scraper.py` mendefinisikan fungsi utama web scraping, `mapper.py` membangun variable yang akan disimpan di JSON, `exporter.py` fungsi yang berguna untuk menyimpan data, `constant.py` menyimpan contanta yang digunakan di `src/`, `utility.py` fungsi helper untuk transformasi tanggal, harga, dan review.

- `Data Storing/src` berisi `script.py` file yang berfungsi untuk melakukan input data dari hasil scraping dan `database.py` file yang berfungsi untuk membangun struktur database awal.

- `Data Warehous/src` berisi `script.py` dan `warehouse.py`.`script.py` file yang berfungsi untuk melakukan input data ke warehouse dari pengambilan data di database `SteamHouse` dan `warehouse.py` file yang berfungsi untuk membangun struktur warehouse awal.

## `data`

Folder ini menyimpan output JSON hasil scraping.

## `export`

Folder ini menyimpan hasil export database dalam format `.sql`.

## `design`

Folder ini menyimpan diagram ERD, diagram relasional, dan diagram data warehouse.

## `screenshot`

Folder ini menyimpan tangkapan layar hasil eksekusi program, isi tabel database, dan query analitik.

---

# Teknologi dan Library

- Python: bahasa pemrograman utama untuk scraping, transformasi data, dan loading ke database.
- Requests: digunakan untuk mengambil HTML dari Steam Store.
- BeautifulSoup4: digunakan untuk parsing HTML.
- JSON: digunakan untuk menyimpan hasil scraping dalam format terstruktur.
- `mysql-connector-python`: digunakan untuk koneksi ke MySQL/MariaDB.
- MySQL / MariaDB: DBMS yang digunakan untuk database operasional dan warehouse.
- SQL: digunakan untuk definisi tabel, relasi, dan query analitik.
- pathlib: digunakan untuk pengelolaan path file yang lebih rapi.

---

# Cara Menjalankan Program

## Prasyarat

Pastikan sudah tersedia:

- Python 3.x
- MySQL atau MariaDB server lokal
- Dependency Python yang dibutuhkan

Instal dependency dengan perintah berikut:

```bash
python -m pip install requests beautifulsoup4 mysql-connector-python
```

## Data Scraping

1. Buka terminal pada folder `Data Scraping/src`.
2. Jalankan script utama scraping.

```bash
python main.py
```

Script ini mengambil data dari Steam Store, memprosesnya, lalu menyimpan hasilnya ke folder `Data Scraping/data` dalam bentuk JSON.

File JSON yang dihasilkan adalah:

- `games.json`
- `developers.json`
- `publishers.json`
- `genres.json`
- `tags.json`
- `game_genres.json`
- `game_tags.json`

## Data Storing

1. Pastikan server MySQL/MariaDB sudah berjalan.
2. Buka terminal pada folder `Data Storing/src`.
3. Jalankan script storing.

```bash
python script.py
```

Script ini membaca file JSON dari folder `Data Scraping/data`, membuat database `SteamGames`, lalu memasukkan data ke tabel-tabel relasional.

Jika konfigurasi database lokal berbeda, sesuaikan pengaturan koneksi pada source code terlebih dahulu.

## Data Warehouse

1. Pastikan database `SteamGames` sudah terisi dari tahap storing.
2. Buka terminal pada folder `Data Warehous/src`.
3. Jalankan script warehouse.

```bash
python script.py
```

Script ini membuat database `WarehouseDB`, menyalin data yang relevan dari `SteamGames`, lalu mengisi tabel fact dan dimension untuk kebutuhan analitik.

---

# Penjelasan Struktur File JSON

## `games.json`

File ini menyimpan data utama hasil scraping untuk setiap game. Atribut pentingnya adalah `game_id`, `title`, `price`, `release_date`, `review_summary`, `review_count`, `game_url`, `dev_id`, dan `pub_id`.

File ini menjadi sumber utama pada proses storing karena datanya dimasukkan ke tabel `Games`. Field `dev_id` dan `pub_id` dipakai sebagai foreign key untuk menghubungkan game dengan developer dan publisher.
```bash
# Berikut Kutipan games.json:
{
    "game_id": "730",
    "title": "Counter-Strike 2",
    "price": 0.0,
    "release_date": "2012-08-21",
    "review_summary": "Very Positive",
    "review_count": 2578261,
    "game_url": "https://store.steampowered.com/app/730",
    "dev_id": 91,
    "pub_id": 86
},
```

## `developers.json`

File ini berisi daftar developer unik dengan atribut `dev_id` dan `name`.

Data ini digunakan untuk mengisi tabel `Developers` dan untuk memetakan developer pada data game.
```bash
# Berikut Kutipan developers.json:
{
    "dev_id": 1,
    "name": "ACE Team"
},
```
## `publishers.json`

File ini berisi daftar publisher unik dengan atribut `pub_id` dan `name`.

Data ini digunakan untuk mengisi tabel `Publishers` dan untuk memetakan publisher pada data game.

```bash
# Berikut Kutipan publishers.json:
{
    "pub_id": 1,
    "name": "2K"
},
```

## `genres.json`

File ini berisi daftar genre unik dengan atribut `genre_id` dan `name`.

Data ini digunakan untuk mengisi tabel `Genres` dan menjadi referensi relasi game ke genre.
```bash
# Berikut Kutipan genres.json:
{
    "genre_id": 1,
    "name": "Action"
},
```

## `tags.json`

File ini berisi daftar tag unik dengan atribut `tag_id` dan `name`.

Data ini digunakan untuk mengisi tabel `Tags` dan menjadi referensi relasi game ke tag.
```bash
# Berikut Kutipan tags.json:
{
    "tag_id": 1,
    "name": "2D"
},
```

## `game_genres.json`

File ini menyimpan relasi antara game dan genre dalam bentuk pasangan `game_id` dan `genre_id`.

File ini digunakan untuk mengisi tabel junction `GameGenres`.
```bash
# Berikut Kutipan game_genres.json:
{
    "game_id": "730",
    "genre_id": 12
},
```

## `game_tags.json`

File ini menyimpan relasi antara game dan tag dalam bentuk pasangan `game_id` dan `tag_id`.

File ini digunakan untuk mengisi tabel junction `GameTags`.
```bash
# Berikut Kutipan game_tags.json:
{
    "game_id": "730",
    "tag_id": 85
},
```

---

# Perancangan Database

Project ini memiliki dua skema database utama: database operasional untuk hasil scraping dan database warehouse untuk analisis.

## Database Operasional: `SteamGames`

Tabel yang dibuat pada tahap storing adalah:

- `Developers`
- `Publishers`
- `Games`
- `Genres`
- `Tags`
- `GameGenres`
- `GameTags`
- `Achievements`
- `Users`
- `Wallet`
- `Library`
- `Transactions`

Tabel `Developers` dan `Publishers` menyimpan data master. Tabel `Games` menyimpan data utama game dan mereferensikan developer serta publisher. Tabel `Genres` dan `Tags` menyimpan data referensi untuk atribut kategori. Tabel `GameGenres` dan `GameTags` menjadi tabel penghubung untuk relasi many-to-many. Tabel `Achievements`, `Users`, `Wallet`, `Library`, dan `Transactions` merupakan tabel tambahan yang sudah didefinisikan pada skema (Berwarna Merah).

Diagram ERD dan diagram relasional dapat dilihat berikut ini.

![ERD](Data%20Storing/design/ERD.drawio.png)

![Diagram Relasional](Data%20Storing/design/Diagram%20Relasional.drawio.png)

## Database Warehouse: `WarehouseDB`

Tabel utama pada warehouse adalah:

- `dim_game`
- `dim_publisher`
- `dim_developer`
- `dim_date`
- `fact_game`
- `dim_genre`
- `dim_tag`
- `dim_gamegenre`
- `dim_gametag`

Struktur yang digunakan adalah star schema, dengan `fact_game` sebagai pusat. `dim_gamegenre` dan `dim_gametag` berperan sebagai tabel jembatan untuk relasi many-to-many.

Diagram warehouse tersedia di bawah ini.

![Data Warehouse](Data%20Warehous/design/DataWarehouse.drawio.png)

---

# Translasi ERD ke Diagram Relasional

## One-to-Many

Relasi one-to-many pada project ini muncul pada hubungan:

- `Developers` <-- `Games`
- `Publishers` <-- `Games`
- `Games` <-- `Achievements`
- `Games` <-- `Transactions`
- `Users` <-- `Wallet`
- `Users` <-- `Library`
- `Users` <-- `Transactions`

Foreign key ditempatkan di sisi tabel yang berada pada sisi many.

## Many-to-Many

Relasi many-to-many muncul pada hubungan:

- `Games` --- `Genres`
- `Games` --- `Tags`

Relasi tersebut tidak disimpan langsung, tetapi dipisahkan melalui tabel junction.

## Junction Table (Tabel Antara)

Tabel junction yang digunakan adalah:

- `GameGenres` (`Games` --- `Genres`)
- `GameTags` (`Games` --- `Tags`)

Kedua tabel ini menyimpan pasangan identifier untuk merepresentasikan relasi many-to-many.

## Primary Key dan Foreign Key

Primary key digunakan untuk identifikasi unik, sedangkan foreign key digunakan untuk menjaga integritas antar tabel.

Contoh implementasi pada database operasional:

- `Developers(dev_id)` direferensikan oleh `Games(dev_id)`
- `Publishers(pub_id)` direferensikan oleh `Games(pub_id)`
- `Games(id)` direferensikan oleh `GameGenres(game_id)` dan `GameTags(game_id)`
- `Genres(genre_id)` direferensikan oleh `GameGenres(genre_id)`
- `Tags(tag_id)` direferensikan oleh `GameTags(tag_id)`

---

# Data Warehouse

Data warehouse pada project ini dibangun untuk mendukung analisis terhadap data game Steam. `fact_game` menyimpan metrik utama seperti `review_count` dan `price`, sedangkan tabel dimensi menyimpan atribut pendukung seperti developer, publisher, tanggal rilis, genre, dan tag.

Pendekatan yang digunakan mendekati star schema karena fact table ditempatkan di tengah dan tabel dimensi berada di sekelilingnya. Struktur ini memudahkan query analitik, misalnya untuk melihat harga rata-rata per publisher, distribusi review berdasarkan tanggal rilis, atau hubungan antara genre dan popularitas game.

Proses ETL pada warehouse dilakukan dengan mengambil data dari database `SteamGames`, lalu memasukkan data ke tabel dimensi, fact table, dan tabel relasi jembatan.Pengembangan struktur warehouse juga bisa dilakukan apabila ingin membuat fact_table lainnya.
 
---

# Screenshot Program

## Data Storing

![Developers Table](Data%20Storing/screenshot/Developers_Table.png)

![Games Table](Data%20Storing/screenshot/Games_Table.png)

![Genres Table](Data%20Storing/screenshot/Genres_Table.png)

![Publishers Table](Data%20Storing/screenshot/Publishers_Table.png)

![Tags Table](Data%20Storing/screenshot/Tags_Table.png)

![GameGenres Table](Data%20Storing/screenshot/GameGenres_Table.png)

![GameTags Table](Data%20Storing/screenshot/GameTags_Table.png)

## Data Warehouse

![Dim Game Table](Data%20Warehous/screenshot/dim_game_table.png)

![Dim Publisher Table](Data%20Warehous/screenshot/dim_publisher_table.png)

![Dim Developer Table](Data%20Warehous/screenshot/dim_developer_table.png)

![Dim Date Table](Data%20Warehous/screenshot/dim_date_table.png)

![Fact Game Table](Data%20Warehous/screenshot/fact_game_table.png)

![Dim Genre Table](Data%20Warehous/screenshot/dim_genre_table.png)

![Dim Tag Table](Data%20Warehous/screenshot/dim_tag_table.png)

![Dim GameGenre Table](Data%20Warehous/screenshot/dim_gamegenre_table.png)

![Dim GameTag Table](Data%20Warehous/screenshot/dim_gametag_table.png)

![Complex Query 1](Data%20Warehous/screenshot/complex_query_1.png)

![Complex Query 2](Data%20Warehous/screenshot/complex_query_2.png)

![Complex Query 3](Data%20Warehous/screenshot/complex_query_3.png)

Pada repository ini tidak ditemukan folder screenshot khusus untuk tahap Data Scraping.

---

# Referensi

- Steam Store: sumber data yang di-scrape ([Steam Web](https://store.steampowered.com/)) .
- Dokumentasi Python: referensi bahasa pemrograman dan library standar.
- Dokumentasi Requests: referensi HTTP request.
- Dokumentasi BeautifulSoup4: referensi parsing HTML.
- Dokumentasi `mysql-connector-python`: referensi koneksi MySQL/MariaDB dari Python .
- Dokumentasi MySQL / MariaDB: referensi pembuatan database, tabel, dan export SQL ([MariaDB](https://mariadb.com/docs/server/mariadb-quickstart-guides/installing-mariadb-server-guide)).

---

# Penggunaan AI
- Saat memikirkan struktur file pada folder `src/` untuk memastikan penamaan file menggambarkan isi dari filenya dan melakukan modularitas saat scrape sehingga dipecah ke beberapa file, proses debuggin, command terminal.

- Semua proses alur berpikir, pembuatan diagram, SQL, dan code pada data scraping, data storing, dan data warehous masih dikerjakan sendiri. 

- Penggunaan boleh dilakukan dengan bijak, penggunaan AI tidak lebih sebagai alat bantu bukan sebagai Super System yang mengganti seluruh proses pengerjaan tugas.

- File pada folder `data scraping/src/` adalah hasil rekomendasi AI untuk memecah ke beberapa file, namun isi dari file diketik. Proses debuggin seperti error kode SQL, typo, dan pesan error terminal penyelesainnya dibantu oleh AI.  Command terminal yang sering terlupa seperti `source .venv`, `mysqldump -u ...`, etc. masih bertanya kepada AI command gimana. 