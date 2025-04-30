from src.working_with_api import WorkingWithApi


class ToWorkWithVacancies:
    __slots__ = (
        "job_title",
        "job_link",
        "salary_from",
        "salary_to",
        "currency",
        "requirement",
    )

    def __init__(
        self, job_title, job_link, salary_from, salary_to, currency, requirements
    ):
        """Конструктор класса:
        :param job_title: название вакансии
        :param job_link: ссылка на вакансию
        :param salary_from: минимальная зарплата (целое число > 0)
        :param salary_to: максимальная зарплата (целое число > 0)
        :param currency: валюта (целое число > 0)
        :param requirements: требования
        """
        # Проверка обязательных полей
        if not job_title:
            raise ValueError("Название вакансии не может быть пустым")
        if not job_link:
            raise ValueError("Ссылка на вакансию не может быть пустой")
        if not requirements:
            raise ValueError("Требования не могут быть пустыми")

        # Проверка формата ссылки
        if not job_link.startswith(("http://", "https://")):
            raise ValueError("Некорректная ссылка на вакансию")

        # Проверка зарплаты
        if not isinstance(salary_from, int) or salary_from <= 0:
            raise ValueError("Минимальная зарплата должна быть целым числом больше 0")
        if not isinstance(salary_to, int) or salary_to <= 0:
            raise ValueError("Максимальная зарплата должна быть целым числом больше 0")

        # Инициализация атрибутов
        self.job_title = job_title
        self.job_link = job_link
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.requirement = requirements
        self.currency = currency

    def __lt__(self, other):
        """Магический метод для оператора меньше <"""
        if not isinstance(other, ToWorkWithVacancies):
            raise TypeError("Можно сравнивать только с объектами ToWorkWithVacancies")
        return self.salary_from < other.salary_from

    def __gt__(self, other):
        """Магический метод для оператора больше >"""
        if not isinstance(other, ToWorkWithVacancies):
            raise TypeError("Можно сравнивать только с объектами ToWorkWithVacancies")
        return self.salary_from > other.salary_from

    def method_for_vac(self, keyword_2: str) -> list:
        """Метод подготавливает вакансии для модуля, который будет добавлять в файл"""
        api_path = WorkingWithApi()
        none_list = []
        for vac in api_path.get_vacancies(keyword_2):
            counter = 0
            # Проверка названия
            if self.job_title in vac["name"]:
                counter += 1
            # Проверка ссылки
            if self.job_link in vac["url"]:
                counter += 1
            # Проверка валюты
            if vac.get("salary") is not None:
                salary_data = vac["salary"]
                if "currency" in salary_data:
                    vacancy_currency = salary_data["currency"]
                    if (
                        vacancy_currency is not None
                        and self.currency == vacancy_currency
                    ):
                        counter += 1
            # Проверка минимальной зарплаты
            if vac.get("salary") is not None:
                salary_data = vac["salary"]
                if "from" in salary_data:
                    vacancy_from = salary_data["from"]
                    if vacancy_from is not None and self.salary_from == vacancy_from:
                        counter += 1
            # Проверка максимальной зарплаты
            if vac.get("salary") is not None:
                salary_data = vac["salary"]
                if "to" in salary_data:
                    vacancy_to = salary_data["to"]
                    if vacancy_to is not None and self.salary_to == vacancy_to:
                        counter += 1
            # Проверка умений кандидата
            if (
                vac["snippet"]["requirement"] is not None
                and self.requirement in vac["snippet"]["requirement"]
            ):
                counter += 1
            # На основе проверок, происходит создание списка словарей
            if counter >= 1:
                none_list.append(
                    {
                        "title": vac.get("name", {}),
                        "url": vac.get("url", {}),
                        "alternate_url": vac.get("alternate_url", {}),
                        "experience": vac.get("experience", {}),
                        "employment": vac.get("employment", {}),
                        "address": vac.get("address", {}),
                        "salary": {
                            "salary_from": (
                                vac.get("salary", {}).get("from")
                                if vac and vac.get("salary")
                                else None
                            ),
                            "salary_to": (
                                vac.get("salary", {}).get("to")
                                if vac and vac.get("salary")
                                else None
                            ),
                            "currency": (
                                vac.get("salary", {}).get("currency")
                                if vac and vac.get("salary")
                                else None
                            ),
                        },
                        "requirement": vac.get("snippet", {}).get("requirement"),
                        "match_score": counter,
                    }
                )

        none_list.sort(
            key=lambda x: x["match_score"], reverse=True
        )  # Сортировка совпадений
        # Создание нового списка словарей
        result_list = []
        for vac in none_list:
            result_list.append(
                {
                    "title": vac["title"],
                    "url": vac["url"],
                    "alternate_url": vac["alternate_url"],
                    "experience": vac["experience"],
                    "employment": vac["employment"],
                    "address": vac["address"],
                    "salary": vac["salary"],
                    "requirement": vac["requirement"],
                }
            )

        return result_list
