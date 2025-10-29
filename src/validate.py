import pandas as pd


def validate_non_empty(df: pd.DataFrame) -> bool:

    if df.empty:
        print("Ошибка валидации: DataFrame пустой.")
        return False
    print("Валидация: DataFrame не пустой.")
    return True


def validate_columns(df: pd.DataFrame, expected_columns: list) -> bool:

    if not all(col in df.columns for col in expected_columns):
        print(
            f"Ошибка валидации: Отсутствуют необходимые колонки. Ожидались: {expected_columns}"
        )
        return False
    print("Валидация: Все необходимые колонки на месте.")
    return True
