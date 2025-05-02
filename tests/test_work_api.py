import pytest
from src.working_with_api import WorkingWithApi


# Фикстура для экземпляра класса (чтобы не создавать его в каждом тесте)
@pytest.fixture
def api_client():
    return WorkingWithApi()


# Тест: проверяем, что запрос к API возвращает 200
def test_get_vacancies_status_code(api_client, mocker):
    # Мокаем requests.get, чтобы не делать реальные запросы
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [{"id": "1", "name": "Python Developer"}]
    }

    mocker.patch("requests.get", return_value=mock_response)

    vacancies = api_client.get_vacancies("Python")
    assert isinstance(vacancies, list)
    assert len(vacancies) > 0
    assert vacancies[0]["id"] == "1"


# Тест: проверяем параметры запроса
def test_api_request_params(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": []}

    mock_get = mocker.patch("requests.get", return_value=mock_response)

    api_client.get_vacancies("Java")

    # Проверяем, что запрос отправлен с правильными параметрами
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert kwargs["params"]["text"] == "Java"
    assert kwargs["params"]["page"] == 1
    assert kwargs["params"]["per_page"] == 100


# Тест: проверяем обработку ошибки (например, 404)
def test_api_error_handling(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404

    mocker.patch("requests.get", return_value=mock_response)

    vacancies = api_client.get_vacancies("C++")
    assert vacancies == []  # или другой ожидаемый результат при ошибке


# Тест: проверяем пагинацию (если API возвращает несколько страниц)
def test_pagination_logic(api_client, mocker):
    mock_responses = [{"items": [{"id": "1"}]}, {"items": [{"id": "2"}]}, {"items": []}]

    mock_get = mocker.patch("requests.get")
    mock_get.side_effect = [
        mocker.Mock(status_code=200, json=lambda: mock_responses[0]),
        mocker.Mock(status_code=200, json=lambda: mock_responses[1]),
        mocker.Mock(status_code=200, json=lambda: mock_responses[2]),
    ]

    vacancies = api_client.get_vacancies("Go")
    assert len(vacancies) == 1  # вакансии с двух страниц
