import pytest
from unittest.mock import patch
from src.working_with_api import WorkingWithApi
from src.working_with_vacancies import ToWorkWithVacancies  # замените your_module на реальный модуль


def test_init_valid():
    vac = ToWorkWithVacancies(
        job_title="Python Developer",
        job_link="https://example.com/job/1",
        salary_from=1000,
        salary_to=2000,
        currency="USD",
        requirements="Django"
    )
    assert vac.job_title == "Python Developer"
    assert vac.salary_from == 1000


@pytest.mark.parametrize("job_title,job_link,requirements,error_msg", [
    ("", "https://example.com", "req", "Название вакансии не может быть пустым"),
    ("Job", "", "req", "Ссылка на вакансию не может быть пустой"),
    ("Job", "https://example.com", "", "Требования не могут быть пустыми"),
])
def test_init_empty_fields(job_title, job_link, requirements, error_msg):
    with pytest.raises(ValueError) as e:
        ToWorkWithVacancies(job_title, job_link, 1000, 2000, "USD", requirements)
    assert error_msg in str(e.value)


def test_init_invalid_link():
    with pytest.raises(ValueError):
        ToWorkWithVacancies("Job", "ftp://badlink.com", 1000, 2000, "USD", "req")


@pytest.mark.parametrize("salary_from,salary_to,error_msg", [
    (0, 2000, "Минимальная зарплата должна быть целым числом больше 0"),
    (1000, -1, "Максимальная зарплата должна быть целым числом больше 0"),
    ("1000", 2000, "Минимальная зарплата должна быть целым числом больше 0"),
])
def test_init_invalid_salary(salary_from, salary_to, error_msg):
    with pytest.raises(ValueError) as e:
        ToWorkWithVacancies("Job", "https://example.com", salary_from, salary_to, "USD", "req")
    assert error_msg in str(e.value)


def test_comparison_operators():
    vac1 = ToWorkWithVacancies("Job1", "https://example.com/1", 1000, 1500, "USD", "req")
    vac2 = ToWorkWithVacancies("Job2", "https://example.com/2", 2000, 2500, "USD", "req")

    assert (vac1 < vac2) is True
    assert (vac2 > vac1) is True

    with pytest.raises(TypeError):
        _ = vac1 < 123


@patch.object(WorkingWithApi, 'get_vacancies')
def test_method_for_vac(mock_get_vacancies):
    # Мокаем возвращаемые вакансии
    mock_get_vacancies.return_value = [
        {
            "name": "Python Developer",
            "url": "https://example.com/job/1",
            "alternate_url": "",
            "experience": {},
            "employment": {},
            "address": {},
            "salary": {"from": 1000, "to": 2000, "currency": "USD"},
            "snippet": {"requirement": "Django"},
        },
        {
            # Вакансия без совпадений
            "name": "Java Developer",
            "url": "",
            "alternate_url": "",
            "experience": {},
            "employment": {},
            "address": {},
            "salary": None,
            "snippet": {"requirement": None},
        },
    ]

    vac = ToWorkWithVacancies(
        job_title="Python Developer",
        job_link="https://example.com/job/1",
        salary_from=1000,
        salary_to=2000,
        currency="USD",
        requirements="Django"
    )

    results = vac.vac_for_module("python")

    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0]["title"] == "Python Developer"