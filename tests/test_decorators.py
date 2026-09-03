import pytest

from decorators import log


def test_console_success(capsys):
    """Тест успешного выполнения функции с выводом в консоль."""

    @log
    def sample_add(a, b):
        return a + b

    result = sample_add(3, 7)

    assert result == 10

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()

    assert "--- Старт функции 'sample_add' ---" in captured.out
    assert "Функция 'sample_add' успешно завершена. Результат: 10" in captured.out
    assert "--- Конец функции 'sample_add' ---" in captured.out


def test_console_error(capsys):
    """Тест перехвата ошибки с выводом в консоль."""

    @log
    def sample_div(a, b):
        return a / b

    # Проверяем, что ошибка пробрасывается дальше
    with pytest.raises(ZeroDivisionError):
        sample_div(10, 0)

    captured = capsys.readouterr()

    assert "--- Старт функции 'sample_div' ---" in captured.out
    assert "Ошибка в функции 'sample_div'!" in captured.out
    assert "Тип ошибки: ZeroDivisionError" in captured.out
    assert "Входные параметры: args=(10, 0), kwargs={}" in captured.out
    assert "--- Конец функции 'sample_div' ---" in captured.out


# --- ТЕСТЫ ДЛЯ ЗАПИСИ В ФАЙЛ ---

def test_file_success(tmp_path):
    """Тест успешного выполнения функции с записью в файл."""
    # Создаем временный файл во временной папке pytest
    log_file = tmp_path / "success.log"

    @log(filename=str(log_file))
    def sample_concat(s1, s2):
        return s1 + s2

    result = sample_concat("Hello", "World")

    assert result == "HelloWorld"

    # Читаем содержимое созданного файла
    log_content = log_file.read_text(encoding="utf-8")

    assert "--- Старт функции 'sample_concat' ---" in log_content
    assert "Функция 'sample_concat' успешно завершена. Результат: HelloWorld" in log_content
    assert "--- Конец функции 'sample_concat' ---" in log_content


def test_file_error(tmp_path):
    """Тест перехвата ошибки с записью в файл."""
    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def sample_key_error(d, key):
        return d[key]

    with pytest.raises(KeyError):
        sample_key_error({"a": 1}, "b")

    log_content = log_file.read_text(encoding="utf-8")

    assert "--- Старт функции 'sample_key_error' ---" in log_content
    assert "Ошибка в функции 'sample_key_error'!" in log_content
    assert "Тип ошибки: KeyError" in log_content
    assert "Входные параметры: args=({'a': 1}, 'b'), kwargs={}" in log_content
    assert "--- Конец функции 'sample_key_error' ---" in log_content
