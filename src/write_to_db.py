import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

TABLE_NAME = "krasnobaeva"
GOOGLE_FILE_ID = "1dX6yILMQCC0RqRz1_MkwxZQfNO9HRFiV"
CSV_URL = f"https://drive.google.com/uc?id={GOOGLE_FILE_ID}"

# типы данных
column_types = {
    "Age": "int64",
    "Gender": "category",
    "BMI": "float64",
    "Obesity_Status": "category",
    "Diet_Type": "category",
    "Disease_Class": "category"
}


print("Шаг 1: Загружаем таблицу с Google Drive")
try:
    data = pd.read_csv(CSV_URL, dtype=column_types, on_bad_lines="skip", encoding="latin1")
    data = data.head(100)
    print(f"Загружено строк: {len(data)}")
except Exception as error:
    print("Не удалось загрузить данные:", error)
    exit()

print("\nШаг 2: Подключаемся к базе данных")
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

print("\nШаг 3: Сохраняем данные в базу")
try:
    engine = create_engine(connection_url)
    data.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)
    print(f"Данные успешно загружены в таблицу '{TABLE_NAME}'!")
except Exception as error:
    print("Ошибка при загрузке в базу:", error)
