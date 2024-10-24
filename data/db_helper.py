import aiosqlite
import os
import random


# Путь к базе данных
db_path = os.path.join("data", "data.db")

async def create_db():
    """Асинхронное создание базы данных и таблицы, если она еще не существует"""
    if not os.path.exists("data"):
        os.makedirs("data")
    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS usernames (
                id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL
            )
        ''')
        await db.commit()


    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
                CREATE TABLE IF NOT EXISTS emails (
                    id_email INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL
                )
            ''')
        await db.commit()

    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS hashtags (
                id_hash INTEGER PRIMARY KEY AUTOINCREMENT,
                hashtag TEXT NOT NULL
            )
        ''')
        await db.commit()
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bio (
                id_bio INTEGER PRIMARY KEY AUTOINCREMENT,
                bio TEXT
            )
        """)
        await db.commit()
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS descriptions (
                id_desc INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT
            )
        """)
        await db.commit()

    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS marks (
                id_mark INTEGER PRIMARY KEY AUTOINCREMENT,
                mark TEXT
            )
        """)
        await db.commit()
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS nicknames (
                id_nick INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT 
            )
        """)
        await db.commit()

    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS proxy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proxy TEXT 
            )
        """)
        await db.commit()

    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS proxy_mobile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proxy TEXT 
            )
        """)
        await db.commit()

    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                geo TEXT UNIQUE,
                proxy TEXT UNIQUE DEFAULT 'FALSE',
                accs_type TEXT DEFAULT 'FALSE',
                app_version TEXT DEFAULT '36.5.6',
                locale TEXT UNIQUE  
            )
        ''')
        await db.commit()
    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id_video INTEGER PRIMARY KEY AUTOINCREMENT,
                video_name TEXT NOT NULL,
                video_path TEXT NOT NULL,
                video_on_off INTEGER
            )
        ''')
    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS ordinary_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS cookie_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                x_device TEXT,
                x_cookie TEXT
            )
        ''')
        await db.commit()
    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS biz (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                biz_name TEXT NOT NULL UNIQUE,
                biz_url TEXT UNIQUE
            )
        ''')
        await db.commit()
    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS real_profile (
                token_api TEXT UNIQUE
            )
        ''')
        await db.commit()
    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS uniq_confetti (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                speed FLOAT UNIQUE,
                opacity FLOAT UNIQUE,
                scale FLOAT UNIQUE,
                duration FLOAT UNIQUE,
                fade FLOAT UNIQUE,
                light FLOAT UNIQUE,
                dark FLOAT UNIQUE,
                confetti FLOAT UNIQUE,
                confetti_amount INTEGER UNIQUE,
                confetti_speed FLOAT UNIQUE
            )
        ''')
        await db.commit()
    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS biz_category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                biz_cat TEXT NOT NULL UNIQUE,
                biz_name TEXT NOT NULL UNIQUE
            )
        ''')
        await db.commit()

    # Заполнение таблицы данными, если она пуста
    await insert_default_categories()
    await insert_setting_user()
    await insert_bizz_set()
    await insert_real_profile()

    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username INTEGER ,
                stream_count INTEGER,
                fill_type TEXT,
                description INTEGER,
                bio INTEGER,
                nickname INTEGER,
                marks INTEGER,
                ava INTEGER,
                bizz INTEGER,
                hashtags INTEGER,
                hashtag_count INTEGER,
                uniq_bool INTEGER
            )
        ''')
        await db.commit()

    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS carousel_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stickers INTEGER,
                size INTEGER,
                stripes INTEGER,
                angle INTEGER,
                transparency REAL,
                resize REAL,
                blur INTEGER
            )
        ''')
        await db.commit()
#АВТОЗАПОЛНЕНИЕ БД
async def insert_setting_user():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT * FROM settings')
        rows = await cursor.fetchall()
        if rows:
            print(123)
        else:
            await db.execute('INSERT INTO settings  (geo,proxy,accs_type, app_version, locale) VALUES (?, ?, ?, ?, ?)',('KZ', 'FALSE', 'FALSE','36.4.2', 'en-US'))
            await db.commit()

async def insert_bizz_set():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT * FROM biz')
        rows = await cursor.fetchall()
        if rows:
            print(123)
        else:
            await db.execute('INSERT INTO biz (biz_name, biz_url) VALUES (?, ?)',('None', 'None'))
            await db.commit()

async def insert_real_profile():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT * FROM real_profile')
        rows = await cursor.fetchall()
        if rows:
            pass
        else:
            await db.execute('INSERT INTO real_profile (token_api) VALUES (?)',('None',))
            await db.commit()
async def insert_default_categories():
    """Функция для автоматического заполнения таблицы категорий, если она пуста"""
    categories = [
        ("art_crafts", "Art & Crafts"),
        ("automotive_transportation", "Automotive & Transportation"),
        ("baby", "Baby"),
        ("beauty", "Beauty"),
        ("clothing_accessories", "Clothing & Accessories"),
        ("education_training", "Education & Training"),
        ("electronics", "Electronics"),
        ("finance_investing", "Finance & Investing"),
        ("food_beverage", "Food & Beverage"),
        ("gaming", "Gaming"),
        ("health_wellness", "Health & Wellness"),
        ("home_furniture_appliances", "Home, Furniture & Appliances"),
        ("machinery_equipment", "Machinery & Equipment"),
        ("media_entertainment", "Media & Entertainment"),
        ("personalblog", "Personal Blog"),
        ("pets", "Pets"),
        ("professional_services", "Professional Services"),
        ("public_administration", "Public Administration"),
        ("real_estate", "Real Estate"),
        ("restaurants_bars", "Restaurants & Bars"),
        ("shopping_retail", "Shopping & Retail"),
        ("software_apps", "Software & Apps"),
        ("sports_fitness_outdoors", "Sports, Fitness & Outdoors"),
        ("travel_tourism", "Travel & Tourism"),
        ("others", "Others")
    ]

    async with aiosqlite.connect(db_path) as db:
        # Проверка, пустая ли таблица
        cursor = await db.execute('SELECT COUNT(*) FROM biz_category')
        count = await cursor.fetchone()
        if count[0] == 0:
            await db.executemany('INSERT INTO biz_category (biz_cat, biz_name) VALUES (?, ?)', categories)
            await db.commit()
#USERNAMES

async def get_username_zaliv():
    async with aiosqlite.connect(db_path) as db:
        # Получаем значение geo из единственной строки
        cursor = await db.execute('SELECT username FROM usernames LIMIT 1')
        username = await cursor.fetchone()  # Получаем только одно значение
        await cursor.close()

    return username[0] if username else None  # Возвращаем строку или None, если ничего не найдено

async def delete_username(username):
    async with aiosqlite.connect(db_path) as db:
        # Удаляем имя пользователя из базы данных
        await db.execute('DELETE FROM usernames WHERE username = ?', (username,))
        await db.commit()  # Фиксируем изменения


async def insert_usernames(usernames):
    """Асинхронное добавление списка юзернеймов в базу данных"""
    async with aiosqlite.connect(db_path) as db:
        await db.executemany('INSERT INTO usernames (username) VALUES (?)', [(uname,) for uname in usernames])
        await db.commit()

async def get_usernames():
    """Асинхронное получение всех юзернеймов из базы данных"""
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT username FROM usernames')
        result = await cursor.fetchall()
        return [row[0] for row in result]  # Возвращаем список юзернеймов

async def get_random_hashtags( count):
    async with aiosqlite.connect(db_path) as db:
        # Получаем все хэштеги из таблицы
        cursor = await db.execute('SELECT hashtag FROM hashtags')
        hashtags = await cursor.fetchall()  # Получаем список всех хэштегов
        await cursor.close()

    # Преобразуем список кортежей в простой список строк
    hashtags = [hashtag[0] for hashtag in hashtags]

    # Если количество хэштегов меньше, чем запрашиваемое, выбираем сколько есть
    count = min(count, len(hashtags))

    # Выбираем случайные хэштеги
    random_hashtags = random.sample(hashtags, count)

    # Формируем строку в виде "#Hash1 #Hash2 #Hash3"
    hashtag_string = ' '.join([f'#{tag}' for tag in random_hashtags])

    return hashtag_string

async def delete_all_usernames():
    """Асинхронное удаление всех юзернеймов из базы данных"""
    async with aiosqlite.connect(db_path) as db:
        await db.execute('DELETE FROM usernames')
        await db.commit()

#HASHTAGS

async def insert_hashtags(hashtags):
    """Асинхронное добавление списка юзернеймов в базу данных"""
    async with aiosqlite.connect(db_path) as db:
        await db.executemany('INSERT INTO hashtags (hashtag) VALUES (?)', [(uname,) for uname in hashtags])
        await db.commit()

async def get_hashtags():
    """Асинхронное получение всех юзернеймов из базы данных"""
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT hashtag FROM hashtags')
        result = await cursor.fetchall()
        return [row[0] for row in result]  # Возвращаем список юзернеймов

async def delete_all_hashtags():
    """Асинхронное удаление всех юзернеймов из базы данных"""
    async with aiosqlite.connect(db_path) as db:
        await db.execute('DELETE FROM hashtags')
        await db.commit()
async def get_single_description():
    async with aiosqlite.connect(db_path) as db:
        # Получаем одно случайное описание
        cursor = await db.execute('SELECT description FROM descriptions ORDER BY RANDOM() LIMIT 1')
        description = await cursor.fetchone()  # Получаем только одно описание
        await cursor.close()

    return description[0] if description else None
#BIO
async def get_bio_zaliv():
    async with aiosqlite.connect(db_path) as db:
        # Выбираем случайное значение из столбца bio
        cursor = await db.execute('SELECT bio FROM bio ORDER BY RANDOM() LIMIT 1')
        bio = await cursor.fetchone()  # Получаем только одно случайное значение
        await cursor.close()

    return bio[0] if bio else None  # Возвращаем строку или None, если ничего не найдено


async def insert_bio(bio_entries):
    async with aiosqlite.connect(db_path) as db:
        for entry in bio_entries:
            await db.execute("""
                INSERT INTO bio (bio) 
                VALUES (?)
            """, (entry,))
        await db.commit()

# Функция для получения всех bio записей
async def get_bio():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM bio")
        rows = await cursor.fetchall()
        return rows

# Функция для удаления всех bio записей
async def delete_all_bio():
    async with aiosqlite.connect(db_path) as db:
        await db.execute("DELETE FROM bio")
        await db.commit()

# Функция для получения количества bio записей
async def get_bio_count():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM bio")
        count = await cursor.fetchone()
        return count[0]

#OPISANIE
async def insert_opi(opi_entries):
    async with aiosqlite.connect(db_path) as db:
        for entry in opi_entries:
            await db.execute("""
                INSERT INTO descriptions (description) 
                VALUES (?)
            """, (entry,))
        await db.commit()

# Функция для получения всех bio записей
async def get_opi():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM descriptions")
        rows = await cursor.fetchall()
        return rows

# Функция для удаления всех bio записей
async def delete_all_opi():
    async with aiosqlite.connect(db_path) as db:
        await db.execute("DELETE FROM descriptions")
        await db.commit()

# Функция для получения количества bio записей
async def get_opi_count():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM descriptions")
        count = await cursor.fetchone()
        return count[0]

#NICKNAMES
async def insert_nick(opi_entries):
    async with aiosqlite.connect(db_path) as db:
        for entry in opi_entries:
            await db.execute("""
                INSERT INTO nicknames (nickname) 
                VALUES (?)
            """, (entry,))
        await db.commit()


async def get_nick_zaliv():
    async with aiosqlite.connect(db_path) as db:
        # Выбираем случайное значение из столбца bio
        cursor = await db.execute('SELECT nickname FROM nicknames ORDER BY RANDOM() LIMIT 1')
        bio = await cursor.fetchone()  # Получаем только одно случайное значение
        await cursor.close()

    return bio[0] if bio else None  # Возвращаем строку или None, если ничего не найдено


async def get_nick():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM nicknames")
        rows = await cursor.fetchall()
        return rows

async def delete_all_nick():
    async with aiosqlite.connect(db_path) as db:
        await db.execute("DELETE FROM nicknames")
        await db.commit()


async def get_nick_count():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM nicknames")
        count = await cursor.fetchone()
        return count[0]

#MARKS
async def insert_mark(opi_entries):
    async with aiosqlite.connect(db_path) as db:
        for entry in opi_entries:
            await db.execute("""
                INSERT INTO marks (mark) 
                VALUES (?)
            """, (entry,))
        await db.commit()

async def get_mark():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM marks")
        rows = await cursor.fetchall()
        return rows

async def delete_all_mark():
    async with aiosqlite.connect(db_path) as db:
        await db.execute("DELETE FROM marks")
        await db.commit()


async def get_mark_count():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM marks")
        count = await cursor.fetchone()
        return count[0]

#GEO

async def get_geo_zaliv():
    async with aiosqlite.connect(db_path) as db:
        # Получаем значение geo из единственной строки
        cursor = await db.execute('SELECT geo FROM settings LIMIT 1')
        geo = await cursor.fetchone()  # Получаем только одно значение
        await cursor.close()

    return geo[0] if geo else None  # Возвращаем строку или None, если ничего не найдено


# Функция для вставки или обновления GEO кода в таблицу settings
async def insert_or_update_geo(geo_code):
    async with aiosqlite.connect(db_path) as db:
        # Проверяем, есть ли запись в таблице settings
        cursor = await db.execute("SELECT COUNT(*) FROM settings")
        count = await cursor.fetchone()

        if count[0] > 0:
            # Если запись существует, выполняем обновление
            await db.execute('''
                UPDATE settings SET geo = ?
            ''', (geo_code,))
        else:
            # Если запись не существует, выполняем вставку
            await db.execute('''
                INSERT INTO settings (geo) VALUES (?)
            ''', (geo_code,))
        await db.commit()


async def get_geo():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT geo FROM settings")
        rows = await cursor.fetchall()
        return rows

async def get_current_locale():
    """Retrieve the current locale from the database."""
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT locale FROM settings LIMIT 1")
        result = await cursor.fetchone()
        return result[0] if result else "en-US"

async def update_locale(new_locale):
    """Update the locale in the database."""
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE settings SET locale = ?", (new_locale,))
        await db.commit()

#video
# Функция для получения только одного video_name, где video_on_off = 0
async def get_single_video_to_update():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT video_name FROM videos WHERE video_on_off = 0 LIMIT 1')
        video_name = await cursor.fetchone()  # Получаем только одно видео
        await cursor.close()
    return video_name

# Функция для обновления video_on_off на 1 для одного video_name
async def update_single_video_status(video_name):
    async with aiosqlite.connect(db_path) as db:
        await db.execute('UPDATE videos SET video_on_off = 1 WHERE video_name = ?', (video_name,))
        await db.commit()
async def update_single_video_status_back(video_name):
    async with aiosqlite.connect(db_path) as db:
        await db.execute('UPDATE videos SET video_on_off = 0 WHERE video_name = ?', (video_name,))
        await db.commit()

async def update_single_video_status_back_all():
    async with aiosqlite.connect(db_path) as db:
        await db.execute('UPDATE videos SET video_on_off = 0 WHERE video_on_off = ?', (1,))
        await db.commit()

async def insert_video(unique_name, save_location):
    async with aiosqlite.connect(db_path) as db:
            await db.execute('''
                INSERT INTO videos (video_name, video_path, video_on_off) VALUES (?, ?, ?)
            ''', (unique_name, save_location, 0))
            await db.commit()

async def delete_all_videos():
    """Удаляет все видео из базы данных"""
    async with aiosqlite.connect(db_path) as db:
        await db.execute('DELETE FROM videos')
        await db.commit()

async def fetch_data():
    async with aiosqlite.connect(db_path) as db:
        # Выполняем запрос на получение всех данных из таблицы profile
        cursor = await db.execute('SELECT * FROM profile')
        # Извлекаем одну строку (если таблица содержит только одну строку)
        info = await cursor.fetchone()
        await cursor.close()
    return info

#proxy

async def get_confetti_info():
    async with aiosqlite.connect(db_path) as db:
        # Выполняем запрос на получение всех данных из таблицы uniq_confetti
        cursor = await db.execute('SELECT * FROM uniq_confetti LIMIT 1')
        u_info = await cursor.fetchone()  # Получаем только одну строку
        await cursor.close()

    return u_info
async def delete_proxy_by_id(proxy_id):
    async with aiosqlite.connect(db_path) as db:
        # Удаляем строку по её id
        await db.execute('DELETE FROM proxy WHERE id = ?', (proxy_id,))
        await db.commit()

async def get_proxy():
    async with aiosqlite.connect(db_path) as db:
        # Получаем одну строку с полями id и proxy
        cursor = await db.execute('SELECT id, proxy FROM proxy LIMIT 1')
        result = await cursor.fetchone()  # Получаем только одну строку

        if result:
            proxy_id, proxy_value = result
            return proxy_id, proxy_value
        else:
            return None, None  # Если строки нет


async def delete_proxy_mobile_by_id(proxy_id):
    async with aiosqlite.connect(db_path) as db:
        # Удаляем строку по её id
        await db.execute('DELETE FROM proxy_mobile WHERE id = ?', (proxy_id,))
        await db.commit()

async def get_proxy_mobile():
    async with aiosqlite.connect(db_path) as db:
        # Получаем одну строку с полями id и proxy
        cursor = await db.execute('SELECT id, proxy FROM proxy_mobile LIMIT 1')
        result = await cursor.fetchone()  # Получаем только одну строку

        if result:
            proxy_id, proxy_value = result
            return proxy_id, proxy_value
        else:
            return None, None  # Если строки нет

async def get_current_proxy_type():
    """Получаем текущее значение прокси из таблицы settings"""
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT proxy FROM settings")
        row = await cursor.fetchone()
        if row:
            return row[0]  # Возвращаем текущее значение (TRUE/FALSE)
        else:
            return "FALSE"  # Возвращаем значение по умолчанию (обычные прокси)

async def get_proxy_value():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT proxy FROM settings')
        result = await cursor.fetchone()  # Получаем только одну строку
        return result[0] if result else None  # Возвращаем значение proxy или None, если записи нет




async def update_proxy_type(proxy_value):
    """Обновляем тип прокси в таблице settings (TRUE для мобильных, FALSE для обычных)"""
    async with aiosqlite.connect(db_path) as db:
        # Проверяем, существует ли запись
        cursor = await db.execute("SELECT COUNT(*) FROM settings")
        count = await cursor.fetchone()

        if count[0] == 0:
            # Вставляем запись, если не существует
            await db.execute('''
                INSERT INTO settings (proxy) VALUES (?)
            ''', (proxy_value,))
        else:
            # Обновляем существующую запись
            await db.execute('''
                UPDATE settings SET proxy = ?
            ''', (proxy_value,))
        await db.commit()



async def insert_proxies(proxies, is_mobile):
    """Insert proxies into the appropriate table"""
    async with aiosqlite.connect(db_path) as db:
        table = 'proxy_mobile' if is_mobile else 'proxy'
        await db.executemany(f'INSERT INTO {table} (proxy) VALUES (?)', [(proxy,) for proxy in proxies])
        await db.commit()

async def get_proxy_count(is_mobile):
    """Get count of proxies from the appropriate table"""
    async with aiosqlite.connect(db_path) as db:
        table = 'proxy_mobile' if is_mobile else 'proxy'
        cursor = await db.execute(f'SELECT COUNT(*) FROM {table}')
        count = await cursor.fetchone()
        return count[0]

async def delete_all_proxies(is_mobile):
    """Delete all proxies from the appropriate table"""
    async with aiosqlite.connect(db_path) as db:
        table = 'proxy_mobile' if is_mobile else 'proxy'
        await db.execute(f'DELETE FROM {table}')
        await db.commit()

#ACCS
# Вставка обычных аккаунтов
async def insert_ordinary_accounts(accounts):
    async with aiosqlite.connect(db_path) as db:
        await db.executemany('INSERT INTO ordinary_accounts (account) VALUES (?)', [(acc,) for acc in accounts])
        await db.commit()

# Вставка куки-аккаунтов
async def insert_cookie_accounts(accounts):
    async with aiosqlite.connect(db_path) as db:
        await db.executemany('INSERT INTO cookie_accounts (x_device, x_cookie) VALUES (?, ?)', accounts)
        await db.commit()


# Получение обычных аккаунтов
# Получение всех обычных аккаунтов
async def get_ordinary_accounts():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT account FROM ordinary_accounts')
        result = await cursor.fetchall()
        return [row[0] for row in result]  # Возвращаем список обычных аккаунтов


# Функция для получения одного случайного значения mark из таблицы
async def get_single_mark():
    async with aiosqlite.connect(db_path) as db:
        # Получаем одно случайное значение из колонки mark
        cursor = await db.execute('SELECT mark FROM marks ORDER BY RANDOM() LIMIT 1')
        mark = await cursor.fetchone()  # Получаем только одно значение
        await cursor.close()

    return mark[0] if mark else None  # Возвращаем строку или None, если ничего не найдено


async def get_single_ordinary_account():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT account FROM ordinary_accounts LIMIT 1')
        result = await cursor.fetchone()  # Получаем только одну строку
        return result[0] if result else None  # Возвращаем аккаунт или None, если записей нет

async def delete_ordinary_account(account):
    async with aiosqlite.connect(db_path) as db:
        await db.execute('DELETE FROM ordinary_accounts WHERE account = ?', (account,))
        await db.commit()


# Получение всех куки-аккаунтов
async def get_cookie_accounts():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT x_device, x_cookie FROM cookie_accounts')
        result = await cursor.fetchall()
        return [f"Device: {row[0]}, Cookie: {row[1]}" for row in result]  # Возвращаем список куки-аккаунтов

# Удаление всех обычных аккаунтов
async def delete_all_ordinary_accounts():
    async with aiosqlite.connect(db_path) as db:
        await db.execute('DELETE FROM ordinary_accounts')
        await db.commit()

# Удаление всех куки-аккаунтов
async def delete_all_cookie_accounts():
    async with aiosqlite.connect(db_path) as db:
        await db.execute('DELETE FROM cookie_accounts')
        await db.commit()

async def update_accs_type(accs_type_value):
    """Update the account type (ordinary or cookie) in the settings table."""
    async with aiosqlite.connect(db_path) as db:
        # Check if the settings entry exists
        cursor = await db.execute("SELECT COUNT(*) FROM settings")
        count = await cursor.fetchone()

        if count[0] == 0:
            # Insert a new entry if it doesn't exist
            await db.execute('''
                INSERT INTO settings (accs_type) VALUES (?)
            ''', (accs_type_value,))
        else:
            # Update the existing entry
            await db.execute('''
                UPDATE settings SET accs_type = ?
            ''', (accs_type_value,))
        await db.commit()

# Функция для получения x_device и x_cookie по id
async def get_first_device_and_cookie():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('''
            SELECT id, x_device, x_cookie FROM cookie_accounts LIMIT 1
        ''')
        result = await cursor.fetchone()
        if result:
            row_id, x_device, x_cookie = result
            return row_id, x_device, x_cookie
        else:
            return None

# Функция для удаления строки по id
async def delete_row_cookie(row_id):
    async with aiosqlite.connect(db_path) as db:
        await db.execute('''
            DELETE FROM cookie_accounts WHERE id = ?
        ''', (row_id,))
        await db.commit()


#biz
'''async def insert_or_update_biz_link(biz_name):
    async with aiosqlite.connect(db_path) as db:
        await db.execute(''
            INSERT INTO biz (biz_name)
            VALUES (?)
            ON CONFLICT(biz_name) DO NOTHING
        '', (biz_name,))
        await db.commit()'''


async def get_biz_cat_by_name(biz_name_value):
    async with aiosqlite.connect(db_path) as db:
        # Выполняем запрос на выбор biz_cat, где biz_name соответствует заданному значению
        cursor = await db.execute('SELECT biz_cat FROM biz_category WHERE biz_name = ?', (biz_name_value,))
        biz_cat = await cursor.fetchone()  # Получаем только одно значение
        await cursor.close()

    return biz_cat[0] if biz_cat else None

async def get_random_biz_name():
    async with aiosqlite.connect(db_path) as db:
        # Получаем случайное значение из столбца biz_name
        cursor = await db.execute('SELECT biz_name FROM biz LIMIT 1')
        biz_name = await cursor.fetchone()  # Получаем только одно случайное значение
        await cursor.close()

    return biz_name[0] if biz_name else None  # Возвращаем строку или None, если ничего не найдено


async def get_random_biz_url():
    async with aiosqlite.connect(db_path) as db:
        # Получаем случайное значение из столбца biz_url
        cursor = await db.execute('SELECT biz_url FROM biz LIMIT 1')
        biz_url = await cursor.fetchone()  # Получаем только одно случайное значение
        await cursor.close()

    return biz_url[0] if biz_url else None  # Возвращаем строку или None, если ничего не найдено


# Возвращаем строку или None, если ничего не найдено


async def update_biz_link(biz_url):
    async with aiosqlite.connect(db_path) as db:
        await db.execute('UPDATE biz SET biz_url = ?', (biz_url,))
        await db.commit()

async def update_biz_name(biz_name):
    async with aiosqlite.connect(db_path) as db:
        await db.execute('UPDATE biz SET biz_name = ?', (biz_name,))
        await db.commit()

async def delete_biz_url():
    async with aiosqlite.connect(db_path) as db:
        await db.execute('DELETE biz_url FROM biz')
        await db.commit()

async def get_biz_links():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT biz_name, biz_cat FROM biz_category')
        result = await cursor.fetchall()
        return result

async def get_biz_lins():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT biz_name, biz_url FROM biz')
        result = await cursor.fetchall()
        return result

async def delete_biz_link(biz_name):
    async with aiosqlite.connect(db_path) as db:
        await db.execute('DELETE FROM biz WHERE biz_name = ?', (biz_name,))
        await db.commit()

async def get_biz_categories():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT biz_name FROM biz_category')
        return await cursor.fetchall()
#get_current_account_type()
async def get_current_account_type():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT accs_type FROM settings')
        return await cursor.fetchall()
async def insert_or_update_biz_url(biz_url):
    async with aiosqlite.connect(db_path) as db:
        # Update the URL for the existing biz_name
        await db.execute('''
            UPDATE biz
            SET biz_url = ?
        ''', (biz_url,))
        await db.commit()
#profile

async def save_or_update_profile(stream_count, fill_type, description, bio, username, nickname, marks, ava, bizz, hashtags, hashtag_count, uniq_bool):
    async with aiosqlite.connect(db_path) as db:
        # Проверка, существует ли запись с таким username
        cursor = await db.execute('SELECT COUNT(*) FROM profile WHERE username = ?', (username,))
        result = await cursor.fetchone()

        if result[0] > 0:
            # Если запись существует, выполняем обновление
            await db.execute('''
                UPDATE profile
                SET stream_count = ?, fill_type = ?, description = ?, bio = ?, nickname = ?, marks = ?, ava = ?, bizz = ?, hashtags = ?, hashtag_count = ?, username = ?, uniq_bool = ?
            ''', (stream_count, fill_type, description, bio, nickname, marks, ava, bizz, hashtags, hashtag_count, username, uniq_bool))
        else:
            # Если записи нет, выполняем вставку
            await db.execute('''
                INSERT INTO profile (username, stream_count, fill_type, description, bio, nickname, marks, ava, bizz, hashtags, hashtag_count, uniq_bool)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, stream_count, fill_type, description, bio, nickname, marks, ava, bizz, hashtags, hashtag_count, uniq_bool))
        await db.commit()

async def get_token():
    """Retrieve the current token from the database."""
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT token_api FROM real_profile LIMIT 1")
        result = await cursor.fetchone()
        return result[0] if result else None

async def update_token(new_token):
    """Update the token in the database."""
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE real_profile SET token_api = ?", (new_token,))
        await db.commit()

async def get_profile_data():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT * FROM profile')
        result = await cursor.fetchone()
        return result

#Версия
async def get_current_version():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT app_version FROM settings LIMIT 1")
        row = await cursor.fetchone()
        return row[0] if row else None

async def get_app_version():
    async with aiosqlite.connect(db_path) as db:
        # Получаем значение app_version из таблицы settings
        cursor = await db.execute('SELECT app_version FROM settings LIMIT 1')
        result = await cursor.fetchone()  # Получаем только одну строку

        if result:
            return result[0]  # Возвращаем значение app_version
        else:
            result = '36.4.2'
            return result  # Если строка не найдена



async def update_version(new_version):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE settings SET app_version = ?", (new_version,))
        await db.commit()

#Uniq
async def insert_uniq_confetti(speed, opacity, scale, duration, fade, light, dark, confetti, confetti_amount, confetti_speed):
    try:
        # Форматируем числа, чтобы оставить только две цифры после запятой
        speed = round(float(speed), 2)
        opacity = round(float(opacity), 2)
        scale = round(float(scale), 2)
        duration = round(float(duration), 2)
        confetti_speed = round(float(confetti_speed), 2)

        async with aiosqlite.connect(db_path) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM uniq_confetti")
            count = await cursor.fetchone()
            if count[0] > 0:  # Проверяем, что есть записи
                await db.execute('UPDATE uniq_confetti SET speed = ?, opacity = ?, scale = ?, duration = ?, fade = ?, light = ?, dark = ?, confetti = ?, confetti_amount = ?, confetti_speed = ?',
                                 (speed, opacity, scale, duration, fade, light, dark, confetti, confetti_amount, confetti_speed))
            else:
                await db.execute('''
                    INSERT INTO uniq_confetti (speed, opacity, scale, duration, fade, light, dark, confetti, confetti_amount, confetti_speed)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (speed, opacity, scale, duration, fade, light, dark, confetti, confetti_amount, confetti_speed))
            await db.commit()
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")


async def get_uniq_confetti():
    async with aiosqlite.connect(db_path) as db:
        # Предполагаем, что в таблице uniq_confetti есть столбцы: speed, opacity, scale, duration, confetti_amount, confetti_speed
        query = """
        SELECT speed, opacity, scale, duration, fade, light, dark, confetti, confetti_amount, confetti_speed 
        FROM uniq_confetti
        """  # Допустим, мы работаем с первой записью настроек (можно изменить ID)

        cursor = await db.execute(query)
        result = await cursor.fetchone()

        if result:
            settings = {
                "speed": result[0],
                "opacity": result[1],
                "scale": result[2],
                "duration": result[3],
                "fade": result[4],
                "light": result[5],
                "dark": result[6],
                "confetti": result[7],
                "confetti_amount": result[8],
                "confetti_speed": result[9],
            }
            return settings
        else:
            return None  # Если запись не найдена

async def insert_carousel_settings(stickers, size, stripes, angle, transparency, resize, blur):
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM carousel_settings")
        count = await cursor.fetchone()
        if count:
            await db.execute('UPDATE carousel_settings SET stickers = ?, size = ?, stripes = ?, angle = ?, transparency = ?, resize = ?, blur = ?', (stickers, size, stripes, angle, transparency, resize, blur))
        else:
            await db.execute('''
                INSERT INTO carousel_settings (stickers, size, stripes, angle, transparency, resize, blur)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (stickers, size, stripes, angle, transparency, resize, blur))
        await db.commit()

async def get_carousel_settings():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT stickers, size, stripes, angle, transparency, resize, blur FROM carousel_settings')
        row = await cursor.fetchone()
        if row:
            return {
                "stickers": row[0],
                "size": row[1],
                "stripes": row[2],
                "angle": row[3],
                "transparency": row[4],
                "resize": row[5],
                "blur": row[6],
            }
        return None

#Почта
# Функция для вставки почт в базу данных
async def insert_emails(emails):
    async with aiosqlite.connect(db_path) as db:
        await db.executemany('INSERT INTO emails (email) VALUES (?)', [(email,) for email in emails])
        await db.commit()

# Функция для получения всех почт
async def get_emails():
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute('SELECT email FROM emails')
        result = await cursor.fetchall()
        return [row[0] for row in result]

# Функция для удаления всех почт
async def delete_all_emails():
    async with aiosqlite.connect(db_path) as db:
        await db.execute('DELETE FROM emails')
        await db.commit()

async def get_one_email():
    async with aiosqlite.connect(db_path) as db:
        async with db.execute('SELECT email FROM emails LIMIT 1') as cursor:
            email_row = await cursor.fetchone()
            if email_row:
                email = email_row[0]
                print(f"Получена почта: {email}")
                return email
            else:
                print("В таблице нет записей.")
                return None

async def delete_email(email):
    async with aiosqlite.connect(db_path) as db:
        await db.execute('DELETE FROM emails WHERE email = ?', (email,))
        await db.commit()
        print(f"Строка с почтой {email} удалена.")