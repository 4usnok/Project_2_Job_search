import json
import tempfile

from src.working_with_files import CreatedJson
from unittest.mock import patch


test_path = "data/test_stop_words.json"
def test_created_new_file():
    """Тестирование основной логики работы метода created_new_file()"""
    with patch("builtins.input", return_value="python"):  # мокаем input
        obj = CreatedJson()
        obj.stop_words = test_path  # подменяем путь

        # Создаём тестовый файл
        with open(test_path, "w") as f:
            json.dump(["python"], f)  # "python" — стоп-слово

        result = obj.created_new_file()  # вызываем метод
        assert result is False  # проверяем

def test_removal_of_vacancies():
        # 1. Создаём временный файл с вакансиями
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", encoding="utf-8", delete=False) as f:
            json.dump(
                [
                    {"name": "Python Developer"},
                    {"name": "Java Developer"},
                ],
                f,
            )
            file_path = f.name

        # 2. Мокаем input (чтобы delete_vacancy = "python")
        with patch("builtins.input", return_value="python"):
            obj = CreatedJson()
            obj.vacancies_api = file_path  # Подменяем путь на временный файл

            # 3. Вызываем метод
            obj.removal_of_vacancies()

            # 4. Проверяем, что вакансия удалилась
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert len(data) == 1  # Осталась только Java
                assert "Python" not in [d["name"] for d in data]  # Python удалён

        # 5. Удаляем временный файл
        import os
        os.unlink(file_path)
