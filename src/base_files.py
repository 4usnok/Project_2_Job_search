from abc import ABC, abstractmethod


class BaseFiles(ABC):

    @abstractmethod
    def add_vac_to_file(self):
        """Абстрактный метод добавления вакансий в файл"""
        pass

    @abstractmethod
    def get_vac_from_file(self):
        """Абстрактный метод получения вакансий из файла"""
        pass

    @abstractmethod
    def del_info_on_vac(self):
        """Абстрактный метод удаления информации по вакансиям"""
        pass
