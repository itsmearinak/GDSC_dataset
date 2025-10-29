import argparse
from extract import extract_data
from transform import transform_data
from load import load_data


def run_pipeline(limit_rows):
    """
    Запускает полный ETL-пайплайн.
    """
    print("Запуск ETL-пайплайна")

    # Шаг 1: Извлечение данных
    raw_df = extract_data()

    # Шаг 2: Трансформация данных
    transformed_df = transform_data(raw_df)

    if transformed_df is not None and limit_rows is not None:
        print(f"\nПрименяем ограничение: будут загружены первые {limit_rows} строк.")
        transformed_df = transformed_df.head(limit_rows)

    # Шаг 3: Загрузка данных
    load_data(transformed_df)

    print("\nПайплайн завершил работу.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Запуск ETL-пайплайна для обработки данных."
    )

    parser.add_argument(
        "--limit",
        type=int,
        nargs="?",
        default=None,
        const=100,
        help="Ограничить количество строк для загрузки. Если число не указано, по умолчанию 100.",
    )

    args = parser.parse_args()

    run_pipeline(limit_rows=args.limit)
