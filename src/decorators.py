import functools
import sys


def log(filename=None):
    """Декоратор автоматически логирует начало и конец выполнения функций, их возвращаемые значения,
     а также перехватывает и записывает возникшие ошибки."""
    # Если декоратор вызван без скобок @log, filename будет самой функцией
    if callable(filename):
        func = filename
        return _make_wrapper(func, filename=None)

    # Если декоратор вызван со скобками @log(filename="...")
    def decorator(func):
        return _make_wrapper(func, filename)

    return decorator


def _make_wrapper(func, filename):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Открываем файл или направляем в стандартный вывод
        out = open(filename, "a", encoding="utf-8") if filename else sys.stdout

        try:
            out.write(f"--- Старт функции '{func.__name__}' ---\n")

            result = func(*args, **kwargs)

            # Лог успешного выполнения (если тесты его требуют)
            out.write(f"Функция '{func.__name__}' успешно завершена. Результат: {result}\n")

            # 2. Маркер конца для успешного случая
            out.write(f"--- Конец функции '{func.__name__}' ---\n\n")
            return result

        except Exception as e:
            # Логируем ошибку строго по шаблону теста (исправлены пробелы в "Тип ошибки")
            out.write(f"Ошибка в функции '{func.__name__}'!\n")
            out.write(f"Тип ошибки: {type(e).__name__}\n")
            out.write(f"Входные параметры: args={args}, kwargs={kwargs}\n")

            # 3. Маркер конца для случая с ошибкой (выносим из finally)
            out.write(f"--- Конец функции '{func.__name__}' ---\n\n")
            raise

        finally:
            # В finally оставляем только закрытие файла, чтобы маркеры не дублировались
            if filename:
                out.close()

    return wrapper
