from abc import ABC, abstractmethod


class BaseFiles(ABC):

    @abstractmethod
    def __init__(self):
        """Абстрактный метод инициализации"""
        pass

    @abstractmethod
    def __add__(self, other):
        """Абстрактный метод получения добавления данных в файл."""
        pass

    @abstractmethod
    def criteria_data(self):
        """Абстрактный метод получения данных из файла по указанным критериям"""
        pass

    @abstractmethod
    def __del__(self):
        """Абстрактный метод удаления информации о вакансиях"""
        pass
