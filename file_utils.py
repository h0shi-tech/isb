import json
from typing import Dict, Any, Union

def read_text_file(file_path: str) -> str:
    """
    Чтение текстового файла.

    Args:
        file_path (str): Путь к файлу для чтения.

    Returns:
        str: Содержимое файла в виде строки.

    Raises:
        FileNotFoundError: Если файл не найден.
        IOError: При ошибках чтения файла.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except IOError as e:
        raise IOError(f"Ошибка при чтении файла {file_path}: {str(e)}")

def write_text_file(file_path: str, content: str) -> None:
    """
    Запись содержимого в текстовый файл.

    Args:
        file_path (str): Путь к файлу для записи.
        content (str): Содержимое для записи.

    Raises:
        IOError: При ошибках записи в файл.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except IOError as e:
        raise IOError(f"Ошибка при записи в файл {file_path}: {str(e)}")

def write_json_file(file_path: str, data: Union[Dict, list]) -> None:
    """
    Запись данных в JSON файл.

    Args:
        file_path (str): Путь к JSON файлу.
        data (Union[Dict, list]): Данные для записи в JSON.

    Raises:
        IOError: При ошибках записи в файл.
        TypeError: Если данные не могут быть сериализованы в JSON.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError as e:
        raise IOError(f"Ошибка при записи в JSON файл {file_path}: {str(e)}")
    except TypeError as e:
        raise TypeError(f"Ошибка сериализации данных в JSON: {str(e)}")

def read_json_file(file_path: str) -> Union[Dict, list]:
    """
    Чтение данных из JSON файла.

    Args:
        file_path (str): Путь к JSON файлу.

    Returns:
        Union[Dict, list]: Прочитанные данные.

    Raises:
        FileNotFoundError: Если файл не найден.
        json.JSONDecodeError: При ошибках парсинга JSON.
        IOError: При ошибках чтения файла.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON файл {file_path} не найден")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Ошибка парсинга JSON в файле {file_path}: {str(e)}", e.doc, e.pos)
    except IOError as e:
        raise IOError(f"Ошибка при чтении JSON файла {file_path}: {str(e)}") 