import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import requests
import tempfile

TABLE_NAME = "krasnobaeva"
GOOGLE_FILE_ID = "1dX6yILMQCC0RqRz1_MkwxZQfNO9HRFiV"

print("Шаг 1: Загружаем SQLite базу с Google Drive")
try:
    # Скачиваем файл
    download_url = f"https://drive.google.com/uc?export=download&id={GOOGLE_FILE_ID}"
    
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp_file:
        response = requests.get(download_url)
        response.raise_for_status()
        tmp_file.write(response.content)
        temp_db_path = tmp_file.name
    
    print(f"Файл скачан во временное расположение: {temp_db_path}")
    
    # Подключаемся к SQLite базе
    sqlite_engine = create_engine(f'sqlite:///{temp_db_path}')
    
    # Получаем список таблиц в SQLite базе
    with sqlite_engine.connect() as conn:
        tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
        print(f"Таблицы в SQLite базе: {tables['name'].tolist()}")
        
        table_name_sqlite = 'cred' if 'cred' in tables['name'].tolist() else tables['name'].iloc[0]
        print(f"Используем таблицу: {table_name_sqlite}")
        
        # Читаем данные из SQLite
        data = pd.read_sql_query(f"SELECT * FROM {table_name_sqlite}", conn)
        
    # Удаляем временный файл
    os.unlink(temp_db_path)
    
    print(f"Загружено строк: {len(data)}")
    print(f"Столбцы: {list(data.columns)}")
    print("Первые 5 строк:")
    print(data.head())
    
    if len(data) == 0:
        print("Ошибка: данные не загружены!")
        exit()
        
except Exception as error:
    print("Не удалось загрузить данные:", error)
    exit()

print("\nШаг 2: Подключаемся к PostgreSQL базе данных")
load_dotenv()  

# достаем логин, пароль и адрес из .env
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_URL")
port = os.getenv("DB_PORT")
database = os.getenv("DB_ROOT_BASE")

if not all([user, password, host, port, database]):
    print("Ошибка: не найдены все переменные окружения (.env)!")
    exit()

# создаём строку подключения
connection_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
print("Строка подключения создана")

print("\nШаг 3: Сохраняем данные в PostgreSQL базу")
try:
    engine = create_engine(connection_url)

    print("\nШаг 3.1: Проверяем существование таблицы и удаляем старую (если есть)")
    try:
        with engine.connect() as conn:
            check_query = text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_name = :table_name
                );
            """)
            result = conn.execute(check_query, {"table_name": TABLE_NAME}).scalar()
            
            if result:
                print(f"Таблица '{TABLE_NAME}' уже существует — удаляем...")
                conn.execute(text(f'DROP TABLE IF EXISTS public."{TABLE_NAME}" CASCADE;'))
                conn.commit()
                print("Старая таблица удалена.")
            else:
                print(f"Таблицы '{TABLE_NAME}' нет — создаём новую.")
    except Exception as error:
        print("Ошибка при проверке или удалении таблицы:", error)

    # Сохраняем данные в PostgreSQL
    data.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)
    print(f"Данные успешно загружены в таблицу '{TABLE_NAME}'!")

except Exception as error:
    print("Ошибка при загрузке в базу:", error)
    exit()

print("\nШаг 4: Проверяем, что таблица записалась в базу")
try:
    with engine.connect() as conn:
        # Проверяем структуру таблицы
        check_structure = text(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = :table_name 
            ORDER BY ordinal_position;
        """)
        structure = conn.execute(check_structure, {"table_name": TABLE_NAME}).fetchall()
        print("Структура таблицы:")
        for col in structure:
            print(f"  {col[0]}: {col[1]}")
        
        # Проверяем данные
        query = text(f'SELECT * FROM public."{TABLE_NAME}" LIMIT 5;')
        df_check = pd.read_sql_query(query, conn)
        print("\nПервые 5 строк из базы данных:")
        print(df_check)
        
        # Проверяем количество строк
        count_query = text(f'SELECT COUNT(*) as count FROM public."{TABLE_NAME}";')
        count_result = conn.execute(count_query).scalar()
        print(f"\nВсего строк в таблице: {count_result}")
        
except Exception as error:
    print("Ошибка при проверке таблицы:", error)