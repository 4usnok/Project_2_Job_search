import unittest
from src.working_with_vacancies import ToWorkWithVacancies


class TestMethod(unittest.TestCase):

    def test_it(self):
        self_obj_it = ToWorkWithVacancies(
            "SMM-менеджер",
            "https://api.hh.ru/areas/1",
            170000,
            "Опыт работы с личным брендом политических деятелей и лидеров общественного мнения будет преимуществом.",
        )
        other_obj_it = ToWorkWithVacancies(
            "Менеджер по развитию",
            "https://api.hh.ru/areas/1",
            150000,
            "Высшее образование. Релевантный опыт работы от 3 лет.",
        )
        self.assertTrue(self_obj_it > other_obj_it)

    def test_gt(self):
        self_obj_gt = ToWorkWithVacancies(
            "Менеджер по работе с клиентами",
            "https://api.hh.ru/areas/13",
            145000,
            "Активность, инициативность, мобильность, стрессоустойчивость и доброжелательность.",
        )
        other_obj_gt = ToWorkWithVacancies(
            "Старший менеджер",
            "https://api.hh.ru/areas/44",
            26300000,
            "Опыт работы в продажах. Развитые коммуникативные навыки. Знание документооборота.",
        )
        self.assertTrue(self_obj_gt < other_obj_gt)
