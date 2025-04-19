import unittest
from src.working_with_vacancies import ToWorkWithVacancies


class TestMethod(unittest.TestCase):

    def test_it(self):
        self_obj = ToWorkWithVacancies(
            "Менеджер по работе с клиентами",
            "https://api.hh.ru/areas/88",
            60,
            "Опыт работы в продажах. Развитые коммуникативные навыки. Знание документооборота."
        )
        other_obj = ToWorkWithVacancies(
            "Менеджер по работе с клиентами",
            "https://api.hh.ru/areas/88",
            50,
            "Опыт работы в продажах. Развитые коммуникативные навыки. Знание документооборота."
        )
        self.assertTrue(self_obj > other_obj)

    def test_gt(self):
        self_obj = ToWorkWithVacancies(
            "Менеджер по работе с клиентами",
            "https://api.hh.ru/areas/88",
            50,
            "Опыт работы в продажах. Развитые коммуникативные навыки. Знание документооборота."
        )
        other_obj = ToWorkWithVacancies(
            "Менеджер по работе с клиентами",
            "https://api.hh.ru/areas/88",
            60,
            "Опыт работы в продажах. Развитые коммуникативные навыки. Знание документооборота."
        )
        self.assertTrue(self_obj < other_obj)
