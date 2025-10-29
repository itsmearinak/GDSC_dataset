import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

PROCESSED_DATA_PATH = "data/processed/processed_data.parquet"
TABLE_NAME = "krasnobaeva"


def load_data(df):

    print("─" * 30)
    print("Начало этапа LOAD.")

    if df is None:
        print("Нет данных для загрузки. Пропускаем этап.")
        return

    try:
        os.makedirs("data/processed", exist_ok=True)
        df.to_parquet(PROCESSED_DATA_PATH)
        print(f"Данные успешно сохранены в: {PROCESSED_DATA_PATH}")

        load_dotenv()
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_URL")
        port = os.getenv("DB_PORT")
        database = os.getenv("DB_ROOT_BASE")

        if not all([user, password, host, port, database]):
            print("Ошибка: не найдены все переменные окружения (.env)!")
            return

        connection_url = (
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        )
        engine = create_engine(connection_url)

        print(f"Загрузка данных в таблицу '{TABLE_NAME}' (максимум 100 строк)...")
        df_to_load = df.head(100)

        df_to_load.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)
        print("Данные успешно загружены в PostgreSQL.")

        with engine.connect() as conn:
            count_query = text(f'SELECT COUNT(*) FROM public."{TABLE_NAME}";')
            count_result = conn.execute(count_query).scalar()
            print(f"Проверка: в таблице '{TABLE_NAME}' теперь {count_result} строк.")

        print("Этап LOAD завершен успешно.")
        print("─" * 30)

    except Exception as e:
        print(f"Произошла ошибка на этапе LOAD: {e}")


if __name__ == "__main__":
    example_df = pd.DataFrame(
        {"id": range(150), "value": [i * 1.1 for i in range(150)]}
    )
    load_data(example_df)
