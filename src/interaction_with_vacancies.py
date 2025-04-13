class ToWorkWithVacancies:

    __slots__ = ("job_title", "job_link", "salary", "requirements")

    def __init__(self, job_title, job_link, salary, requirements):
        """Конструктор класса:
        :param job_title: название вакансии
        :param job_link: ссылка на вакансию
        :param salary: зарплата
        :param requirements: требования
        """
        self.job_title = job_title
        self.job_link = job_link
        self.salary = salary
        self.requirements = requirements

    def __lt__(self, other):
        """Магический метод для оператора меньше <"""
        self.__validate_comparison(other)
        return self.salary < other.salary

    def __gt__(self, other):
        """Магический метод для оператора больше >"""
        self.__validate_comparison(other)
        return self.salary > other.salary

    def __le__(self, other):
        """Магический метод для оператора меньше либо равно <="""
        self.__validate_comparison(other)
        return self.salary <= other.salary

    def __ge__(self, other):
        """Магический метод для оператора больше либо равно >="""
        self.__validate_comparison(other)
        return self.salary >= other.salary

    def __validate_comparison(self, other):
        """Приватный метод валидации для сравнения.
        Проверяет:
        1. Что other — экземпляр ToWorkWithVacancies.
        2. Что salary не None.
        3. Что salary — целое число (int).
        """
        if not isinstance(other, ToWorkWithVacancies):
            raise TypeError("Сравнение возможно только с объектами ToWorkWithVacancies")
        if self.salary is None or other.salary is None:
            raise AttributeError("Зарплата не указана")
        if not isinstance(self.salary, int) or not isinstance(other.salary, int):
            raise TypeError("Зарплата должна быть целым числом (int)")
