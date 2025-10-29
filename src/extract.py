import pandas as pd
import os

FILE_ID = "1NmsM2-TKO-lf6jX2R_V68bG05shkZ2On"
RAW_DATA_PATH = "data/raw/raw_data.csv"


def extract_data():

    print("─" * 30)
    print("Начало этапа EXTRACT.")

    os.makedirs("data/raw", exist_ok=True)
    file_url = f"https://drive.google.com/uc?id={FILE_ID}"

    try:
        print(f"Загрузка данных из Google Drive (ID: {FILE_ID})")
        raw_data = pd.read_csv(file_url)
        print("Данные успешно загружены.")

        if raw_data.empty:
            print("Ошибка: Загруженный файл пуст!")
            return None

        print(f"Загружено {raw_data.shape[0]} строк и {raw_data.shape[1]} столбцов.")

        raw_data.to_csv(RAW_DATA_PATH, index=False)
        print(f"Сырые данные сохранены в: {RAW_DATA_PATH}")
        print("Этап EXTRACT завершен успешно.")

        return raw_data

    except Exception as e:
        print(f"Произошла ошибка на этапе EXTRACT: {e}")
        return None
