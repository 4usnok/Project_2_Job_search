from typing import Any

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
        self.vacancies = []

    def get_vacancies(self, keyword: str):
        """Абстрактный метод для загрузки данных о вакансиях"""
        return self.__get_vacancies(keyword)

    def __get_vacancies(self, keyword: Any) -> Any:
        """Приватный метод получения данных о вакансиях через подключение к API hh.ru"""
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
            return self.vacancies
