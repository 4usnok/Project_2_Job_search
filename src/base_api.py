from abc import ABC, abstractmethod


class BaseApi(ABC):

    @abstractmethod
    def get_vacancies(self, keyword: str):
        """Абстрактный метод для загрузки вакансий"""
        pass
