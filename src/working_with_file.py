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
            range_inp=None,
            please_input=None
    ):
        """Конструктор класса"""
        super().__init__()
        self.stop_words = "data/stop_words.json"
        self.vacancies_file = "data/vacancies.json"
        self.new_vac = "data/new_vac.json"
        self.sorted_vacancy = search_query
        self.delete_vacancy = delete_query
        self.top_vacancy = top_input
        self.range_from = range_from
        self.range_to = range_to
        self.range_inp = range_inp
        self.please_input = please_input
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
        method_class = self.vac.method_for_vac(self.please_input)
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
                        "title": vac.get("title", {}), # название вакансии
                        "url_json": vac.get("url", {}), # json-ссылка
                        "alternate_url": vac.get("alternate_url", {}), # frontend-ссылка
                        "experience": vac.get("experience", {}).get("name")
                        if vac.get("experience") else None, # опыт работы
                        "employment": vac.get("employment", {}).get("name")
                        if vac.get("employment") else None, # занятость
                        "address": vac.get("address", {}).get("city")
                        if vac.get("address") else None, # город
                        "salary": {
                            "from": vac.get("salary", {}).get("salary_from")
                            if vac.get("salary") else None, # минимальная зарплата
                            "to": vac.get("salary", {}).get("salary_to")
                            if vac.get("salary") else None, # максимальная зарплата
                            "currency": vac.get("salary", {}).get("currency"), # валюта
                        } if vac.get("salary", {}) else None,
                        "requirement": vac.get("requirement", {}), # пожелания
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
                try:
                    with open(self.new_vac, "r", encoding="utf-8") as file:
                        data = json.load(file)
                except (FileNotFoundError, json.JSONDecodeError):
                    data = []

                # Добавление новых данных
                data.append({
                    "quantity": len(vacancies_list_sorted),
                    "vacancies": vacancies_list_sorted,
                })

                # Перезапись файла
                with open(self.new_vac, "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

        except json.JSONDecodeError as e:
            print(f"Ошибка при обработке JSON: {e}")
            return False
        except KeyError as e:
            print(f"Ошибка в структуре данных вакансии: {e}")
            return False

    def del_info_on_vac(self):
        """Метод для удаления информации по вакансиям"""
        if self.delete_vacancy.lower() != "нет":
            # Чтение данных из файла
            with open(self.new_vac, "r", encoding="utf-8") as f:  # Чтение
                list_with_dict = json.load(f)
            removed = False # Флаг для отслеживания изменений
            # Проходим по всем блокам данных
            for block in list_with_dict:
                # Сохраняем исходное количество вакансий
                original_count = len(block["vacancies"])
                # Фильтруем вакансии, оставляя только те, в названии которых нет искомой строки
                block["vacancies"] = [
                    vac for vac in block["vacancies"]
                    if self.delete_vacancy.lower() not in vac["title"].lower()
                ]
                # Обновляем количество вакансий в блоке
                block["quantity"] = len(block["vacancies"])
                # Проверяем, были ли удалены вакансии
                if len(block["vacancies"]) != original_count:
                    removed = True

            if not removed:
                print(f"Вакансии с названием '{self.delete_vacancy}' не найдены.")
                return

            # Записываем обновленный список обратно в файл
            with open(self.new_vac, "w", encoding="utf-8") as f:
                json.dump(list_with_dict, f, ensure_ascii=False, indent=2)
                print(f"Информация успешно удалена по: '{self.delete_vacancy}'.")
