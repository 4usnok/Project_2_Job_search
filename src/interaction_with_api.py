from src.base_api import BaseApi
import requests


class ForWorkingWithApi(BaseApi):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом, который вам необходимо реализовать
    """

    def __init__(self):
        """Конструктор"""
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []
        super().__init__()

    def __load_vacancies(self, keyword):
        """Приватный метод подключения к API hh.ru"""
        self.__params['text'] = keyword
        while self.__params.get('page') != 20:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            status_code_resp = response.status_code
            if status_code_resp == 200:
                vacancies = response.json()['items']
                self.vacancies.extend(vacancies)
                self.__params['page'] += 1
        return self.__params
