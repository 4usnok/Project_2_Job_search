from unittest.mock import patch, Mock, call
import pytest
import json
from src.working_with_file import CreatedJson


def test_add_vac_to_file():
    # Создаем мок для ToWorkWithVacancies
    mock_vac = Mock()
    mock_vac.method_for_vac.return_value = {"test": "vacancy_data"}

    # Инициализируем класс с моком
    creator = CreatedJson(please_input="test_input")
    creator.vac = mock_vac

    # Создаем специальный mock для работы с контекстным менеджером
    mock_file = Mock()
    mock_file.__enter__ = Mock(return_value=mock_file)
    mock_file.__exit__ = Mock(return_value=None)

    # Тестируем запись в файл
    with patch("builtins.open", return_value=mock_file):
        result = creator.add_vac_to_file()

        # Проверяем вызовы
        mock_vac.method_for_vac.assert_called_once_with("test_input")
        open.assert_called_once_with("data/vacancies.json", "w", encoding="utf-8")
        # Проверяем что json.dump был вызван с правильными аргументами
        assert mock_file.method_calls[0] == call.write('{')  # Проверка записи


def test_get_vac_from_file_success():
    # Подготовка тестовых данных
    test_stop_words = ["стопслово"]
    test_vacancies = [
        {
            "title": "Python Developer",
            "salary": {"salary_from": 100000, "salary_to": 150000},
            "url": "http://example.com",
        }
    ]

    # Создаем моки для файловых операций
    mock_stop_words = Mock()
    mock_stop_words.__enter__ = Mock(return_value=mock_stop_words)
    mock_stop_words.__exit__ = Mock(return_value=None)
    mock_stop_words.read.return_value = json.dumps(test_stop_words)

    mock_vacancies = Mock()
    mock_vacancies.__enter__ = Mock(return_value=mock_vacancies)
    mock_vacancies.__exit__ = Mock(return_value=None)
    mock_vacancies.read.return_value = json.dumps(test_vacancies)

    mock_new_vac_read = Mock()
    mock_new_vac_read.__enter__ = Mock(return_value=mock_new_vac_read)
    mock_new_vac_read.__exit__ = Mock(return_value=None)
    mock_new_vac_read.read.return_value = json.dumps([])

    mock_new_vac_write = Mock()
    mock_new_vac_write.__enter__ = Mock(return_value=mock_new_vac_write)
    mock_new_vac_write.__exit__ = Mock(return_value=None)

    # Настраиваем side_effect для open
    open_mock = Mock()
    open_mock.side_effect = [
        mock_stop_words,  # stop_words.json
        mock_vacancies,  # vacancies.json
        mock_new_vac_read,  # new_vac.json (чтение)
        mock_new_vac_write  # new_vac.json (запись)
    ]

    # Инициализируем класс с тестовыми параметрами
    creator = CreatedJson(
        search_query="python",
        top_input=5,
        range_from=90000,
        range_to=160000
    )

    # Вызываем метод
    with patch("builtins.open", open_mock):
        result = creator.get_vac_from_file()

    # Проверяем что метод завершился успешно
    assert result is None
    assert open_mock.call_count == 4


def test_del_info_on_vac():
    # Подготовка тестовых данных
    test_data = [
        {
            "quantity": 2,
            "vacancies": [
                {"title": "Python Developer"},
                {"title": "Java Developer"}
            ]
        }
    ]

    # Инициализируем класс
    creator = CreatedJson(delete_query="java")

    with patch("builtins.open") as mock_open:
        # Настраиваем мок для чтения
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.read.return_value = json.dumps(test_data)

        # Вызываем метод
        creator.del_info_on_vac()

        # Проверяем что файл был прочитан и записан
        assert mock_open.call_count == 2
        # Первый вызов - чтение
        mock_open.assert_any_call("data/new_vac.json", "r", encoding="utf-8")
        # Второй вызов - запись
        mock_open.assert_any_call("data/new_vac.json", "w", encoding="utf-8")