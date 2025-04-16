from abc import ABC, abstractmethod


class BaseFiles(ABC):

    @abstractmethod
    def __init__(self):
        """Абстрактный метод инициализации"""
        pass

    @abstractmethod
    def created_new_file(self):
        """Абстрактный метод получения добавления данных в файл."""
        pass

    @abstractmethod
    def removal_of_vacancies(self):
        """Абстрактный метод удаления информации о вакансиях"""
        pass
