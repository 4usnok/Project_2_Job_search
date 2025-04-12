from abc import ABC, abstractmethod


class BaseApi(ABC):

    @abstractmethod
    def __init__(self):
        """Абстрактный метод инициализации"""
        pass

    @abstractmethod
    def get_vacancies(self):
        """Абстрактный метод получения вакансий"""
        pass
