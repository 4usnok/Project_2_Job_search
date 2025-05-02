from unittest.mock import patch, Mock, call
import json
from src.working_with_file import CreatedJson


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
        creator.del_info_vac()

        # Проверяем что файл был прочитан и записан
        assert mock_open.call_count == 2
        # Первый вызов - чтение
        mock_open.assert_any_call("data/sorted_vacancies.json", "r", encoding="utf-8")
        # Второй вызов - запись
        mock_open.assert_any_call("data/sorted_vacancies.json", "w", encoding="utf-8")