import json

from src.working_with_file import CreatedJson
from src.working_with_vacancies import ToWorkWithVacancies
from src.working_with_api import WorkingWithApi


def sorted_api():
    """Работа с информацией об вакансиях Апи"""
    api_class = WorkingWithApi()
    api_class.load_vacancies("")  # Загружаем вакансии
    return api_class.get_vacancies_json()  # Сохраняем новый JSON-файл


def sorted_vac():
    """Работа с сортировкой по вакансиям"""
    vacancy_processor = CreatedJson()
    return vacancy_processor.created_new_file()


def sorted_salary():
    """Сортировка по Зарплате"""
    with open("data/vacancies.json", "r", encoding="utf-8") as json_file:  # Загрузка
        data_json = json.load(json_file)
    vacancies = []
    for item in data_json:  # Раскрытие списка
        salary_data = item.get("salary")
        # Если зарплата не указана, пропускаем или ставим 0
        if salary_data is None:
            salary_value = 0  # или continue, если не хотим включать такие вакансии
        else:
            # Берём salary['to'], если его нет, то salary['from'], иначе 0
            salary_value = salary_data.get("to", salary_data.get("from", 0))
        # Если salary_value None (например, нет ни 'to', ни 'from'), ставим 0
        salary_value = salary_value if salary_value is not None else 0
        vacancy = ToWorkWithVacancies(
            job_title=item["name"],
            job_link=item["area"]["url"],
            salary=int(salary_value),  # Преобразуем в int
            requirements=item["snippet"]["requirement"],
        )
        vacancies.append(vacancy)
    salary_input = input("Отсортировать по возрастанию зарплату (да/нет) ?\n")
    result = []
    if salary_input.lower() == "да":
        sort_ascending = sorted(vacancies, reverse=False)  # Сортировка по возрастанию
        for vacancy in sort_ascending:
            result.append(
                {
                    "job_title": vacancy.job_title,
                    "salary": vacancy.salary,
                    "job_link": vacancy.job_link,
                    "requirements": vacancy.requirements,
                }
            )
    elif salary_input.lower() == "нет":
        sort_descending = sorted(vacancies, reverse=True)  # Сортировка по убыванию
        for vacancy in sort_descending:
            result.append(
                {
                    "name": vacancy.job_title,
                    "salary": vacancy.salary,
                    "requirements": vacancy.requirements,
                }
            )
    else:
        print("Сортировки не произошло")
    with open(
        "data/vacancies.json", "w", encoding="utf-8"
    ) as new_file:  # Сохранение в файл
        return json.dump(result, new_file, ensure_ascii=False, indent=4)


sorted_api()
sorted_vac()
sorted_salary()
