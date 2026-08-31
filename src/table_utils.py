import csv
import pandas as pd
from typing import List, Dict


def read_csv(file_path: str = "../data/transactions.csv") -> List[Dict[str, str]]:
    """Считывает финансовые операции из файла CSV.

    Args:
        file_path (str): Путь к файлу CSV.

    Returns:
        List[Dict[str, str]]: Список словарей с транзакциями.
    """
    transactions = []

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            # DictReader автоматически использует первую строку CSV как ключи для словарей
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                transactions.append(dict(row))

    except FileNotFoundError:
        print(f"Ошибка: Файл по пути '{file_path}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")

    return transactions


def read_excel(file_path: str = "../data/transactions_excel.xlsx") -> List[Dict[str, any]]:
    """Считывает финансовые операции из файла Excel.

    Args:
        file_path (str): Путь к файлу Excel (.xlsx).

    Returns:
        List[Dict[str, any]]: Список словарей с транзакциями.
    """
    try:
        df = pd.read_excel(file_path)
        df = df.where(pd.notnull(df), None)  # Заменяем пустые ячейки NaN на None
        return df.to_dict(orient="records")
    except FileNotFoundError:
        print(f"Ошибка: Файл по пути '{file_path}' не найден.")
        return []
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return []
