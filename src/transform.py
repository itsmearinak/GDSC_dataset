import pandas as pd


def transform_data(df):

    print("─" * 30)
    print("Начало этапа TRANSFORM.")

    if df is None:
        print("Нет данных для трансформации. Пропускаем этап.")
        return None

    try:
        transformed_df = df.copy()

        print("Исходные типы данных (первые 5 столбцов):")
        print(transformed_df.dtypes.head())

        for col in transformed_df.columns:
            transformed_df[col] = pd.to_numeric(transformed_df[col], errors="coerce")

        transformed_df.dropna(axis=1, how="all", inplace=True)

        print("\nТипы данных после трансформации:")
        print(transformed_df.dtypes)

        print("Этап TRANSFORM завершен успешно.")

        return transformed_df

    except Exception as e:
        print(f"Произошла ошибка на этапе TRANSFORM: {e}")
        return None
