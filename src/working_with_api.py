import json

import requests

from src.base_api import BaseApi


class WorkingWithApi(BaseApi):
    """
    Класс для работы с API HeadHunter
    Класс WorkingWithApi обращается к api и работает с информацией о вакансиях
    """

    def __init__(self):
        """Конструктор"""
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.vacancies_api = "data/vacancies.json"
        self.vacancies = []
        super().__init__()

    def load_vacancies(self, keyword):
        """Приватный метод подключения к API hh.ru"""
        self.__params["text"] = keyword
        while self.__params.get("page") != 20:
            response = requests.get(
                self.__url, headers=self.__headers, params=self.__params
            )
            status_code_resp = response.status_code
            if status_code_resp == 200:
                vacancies = response.json()["items"]
                self.vacancies.extend(vacancies)
                self.__params["page"] += 1
        return self.__params

    def get_vacancies_json(self):
        """Создание json-файла с api-данными"""
        with open(self.vacancies_api, "w", encoding="utf-8") as file:  # Запись
            return json.dump(self.vacancies, file, ensure_ascii=False, indent=2)


api_class = WorkingWithApi()
api_class.load_vacancies("")  # Загружаем вакансии
api_class.get_vacancies_json()  # Сохраняем новый JSON-файл
