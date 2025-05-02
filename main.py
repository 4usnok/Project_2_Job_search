from src.working_with_file import CreatedJson
from src.working_with_vacancies import ToWorkWithVacancies


def user_interaction():
    """Точка входа для пользователя"""
    print("=== Парсер для работы с вакансиями ===")
    # Основные параметры поиска, которые будут переданы по умолчанию
    work_api = ToWorkWithVacancies(
        "Python",
        "http://",
        60000,
        230000,
        "RUR",
        "API"
    )

    # Поиск
    input_keyword = input("Введите ключевое слово: ")
    search_query = input("Введите поисковый запрос по вакансии: ")
    top_input = int(input("Введите количество вакансий для вывода в топ N: "))

    # вызов метода класса ToWorkWithVacancies для поиска вакансий по ключевому слову
    work_api.vac_for_module(input_keyword)

    # Ввод диапазона зарплат
    salary_range = input("Введите диапазон зарплат (например: 100000-250000): ").strip()
    if salary_range:
        if "-" in salary_range:
            range_from, range_to = map(int, salary_range.split("-"))
        else:
            range_from = int(salary_range)
            range_to = None
    else:
        range_from = range_to = None

    delete_query = input("Введите запрос для удаления вакансии (или 'нет'): ")

    # Создание объекта
    obj_vac = CreatedJson(
        search_query=search_query,
        delete_query=delete_query,
        top_input=top_input,
        range_from=range_from,
        range_to=range_to,
        input_keyword=input_keyword,
    )

    # Выполнение операций
    obj_vac.add_vac_to_file()
    obj_vac.get_vac_from_file()
    obj_vac.del_info_vac()


if __name__ == "__main__":
    user_interaction()
