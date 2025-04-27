import json

from src.base_files import BaseFiles
from src.working_with_vacancies import ToWorkWithVacancies

class CreatedJson(BaseFiles):

    def __init__(
            self,
            search_query=None,
            delete_query=None,
            top_input=None,
            range_from=None,
            range_to=None,
            range_inp=None
    ):
        """Конструктор класса"""
        super().__init__()
        self.stop_words = "../data/stop_words.json"
        self.vacancies_file = "../data/vacancies.json"
        self.sorted_vacancy = search_query
        self.delete_vacancy = delete_query
        self.top_vacancy = top_input
        self.range_from = range_from
        self.range_to = range_to
        self.range_inp = range_inp
        self.vac = ToWorkWithVacancies(
            "Python",
            "http://",
            60000,
            230000,
            'RUR',
            "API"
        )


    def add_vac_to_file(self):
        """Метод для добавления вакансий в новый json-файл"""
        method_class = self.vac.method_for_vac()
        with open(self.vacancies_file, 'w', encoding="utf-8", ) as file:
            return json.dump(method_class, file, indent=4)


    def get_vac_from_file(self):
        """Метод для получения вакансий из файла по заданным критериям"""
        try:
            # Загрузка стоп-слов
            with open(self.stop_words, "r", encoding="utf-8") as f:
                stop_words = set(json.load(f))
            # Проверка на стоп-слово
            if self.sorted_vacancy.lower() in stop_words:
                print("Поиск отменён: стоп-слово.")
                return False

            # Получение и фильтрация вакансий
            matched_vacancies = []
            with open(self.vacancies_file, "r", encoding="utf-8") as f:
                api_vacancies = json.load(f)

            for vacancy in api_vacancies:
                if self.sorted_vacancy.lower() in vacancy["title"].lower():
                    matched_vacancies.append(vacancy)  # Сохраняем всю вакансию, а не только имя

            # Вывод результатов
            if matched_vacancies and (self.range_from is not None or self.range_to is not None):
                matched_vacancies = [
                    vac for vac in matched_vacancies
                    if (salary := vac.get("salary", {})) and  # Проверяем наличие данных о зарплате
                       (self.range_from is None or  # Если минимальная граница не задана - пропускаем проверку
                        (salary.get("salary_from") is not None and  # Проверяем что зарплата указана
                         int(salary["salary_from"]) >= self.range_from)) and  # Проверяем нижнюю границу
                       (self.range_to is None or  # Если максимальная граница не задана - пропускаем проверку
                        (salary.get("salary_to") is not None and  # Проверяем что зарплата указана
                         int(salary["salary_to"]) <= self.range_to))  # Проверяем верхнюю границу
                ]

                # Подготовка данных для записи
                vacancies_list = []
                for vac in matched_vacancies[:self.top_vacancy]:  # Берём N вакансий
                    vacancy_data = {
                        "title": vac.get("title"),
                        "url_json": vac.get("url"),
                        "salary": {
                            "from": vac.get("salary", {}).get("salary_from"),
                            "to": vac.get("salary", {}).get("salary_to"),
                            "currency": vac.get("salary", {}).get("currency"),
                        } if vac.get("salary") else None,
                        "requirement": vac.get("requirement"),
                    }
                    vacancies_list.append(vacancy_data)

                # Сортировка по salary_from (по убыванию)
                vacancies_list_sorted = sorted(
                    vacancies_list,
                    key=lambda x: (
                        x["salary"]["from"]
                        if x["salary"] and x["salary"]["from"] is not None
                        else -float("inf")  # Если salary нет или from=None, ставим в конец
                    ),
                    reverse=True,  # Сортировка по убыванию
                )

                # Запись в JSON-файл
                with open(self.vacancies_file, "w", encoding="utf-8") as file:
                    json.dump(
                        {
                            "quantity": len(matched_vacancies),
                            "vacancies": vacancies_list_sorted,  # Записываем отсортированный список
                        },
                        file,
                        ensure_ascii=False,
                        indent=4,
                    )
            else:
                print("Ничего не найдено.")

        except json.JSONDecodeError as e:
            print(f"Ошибка при обработке JSON: {e}")
            return False
        except KeyError as e:
            print(f"Ошибка в структуре данных вакансии: {e}")
            return False
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return False

    def del_info_on_vac(self):
        """Метод для удаления информации по вакансиям"""
        if self.delete_vacancy != "нет".lower():
            with open(self.vacancies_file, "r", encoding="utf-8") as f:  # Чтение
                list_with_dict = json.load(f)
            # Создаем новый список без удаляемой вакансии
            updated_list = [
                dict_w_vac
                for dict_w_vac in list_with_dict
                if self.delete_vacancy.lower() not in dict_w_vac["title"].lower()
            ]
            # Проверяем, действительно ли что-то было удалено
            if len(updated_list) == len(list_with_dict):
                print(f"Вакансия '{self.delete_vacancy}' не найдена.")
                return
            # Записываем обновленный список обратно в файл
            with open(self.vacancies_file, "w", encoding="utf-8") as f:
                json.dump(updated_list, f, ensure_ascii=False, indent=2)
                print(f"Информация успешно удалена по: '{self.delete_vacancy}'.")


def user_interaction():
    """Точка входа для пользователя"""
    # Основные параметры поиска
    search_query = input("Введите поисковый запрос: ")
    top_input = int(input("Введите количество вакансий для вывода в топ N: "))

    # Упрощенный ввод диапазона зарплат
    salary_range = input("Введите диапазон зарплат (например: 100000-250000): ").strip()
    if salary_range:
        if '-' in salary_range:
            range_from, range_to = map(int, salary_range.split('-'))
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
        range_to=range_to
    )

    # Выполнение операций
    obj_vac.add_vac_to_file()
    obj_vac.del_info_on_vac()
    obj_vac.get_vac_from_file()

if __name__ == "__main__":
    user_interaction()
