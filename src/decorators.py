import functools
import sys


def log(filename=None):
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
        # Определяем, куда писать логи
        out = open(filename, "a", encoding="utf-8") if filename else sys.stdout

        try:
            out.write(f"--- Старт функции '{func.__name__}' ---\n")
            result = func(*args, **kwargs)
            out.write(f"Функция '{func.__name__}' успешно завершена. Результат: {result}\n")
            return result
        except Exception as e:
            out.write(f"Ошибка в функции '{func.__name__}'!\n")
            out.write(f"Ти  п ошибки: {type(e).__name__}\n")
            out.write(f"Входные параметры: args={args}, kwargs={kwargs}\n")
            raise  # Пробрасываем ошибку дальше
        finally:
            out.write(f"--- Конец функции '{func.__name__}' ---\n\n")
            if filename:
                out.close()  # Закрываем файл, если открывали его

    return wrapper