import json

from src.base_files import BaseFiles


class CreatedJson(BaseFiles):

    def __init__(self):
        """Конструктор класса"""
        super().__init__()
        self.json_data = "../data/vacancies.json"  # Файл с которого берем данные
        self.new_vacancy_file = "../data/sorted_vacancies.json"  # Новый файл
        self.stop_words = "../data/stop_words.json"
        self.sorted_vacancy = input(
            "Введите поисковый запрос для запроса вакансий из hh.ru: "
        )
        self.delete_vacancy = input("Введите поисковый запрос для удаления вакансии: ")

    def created_new_file(self):
        """Метод обрабатывает файл и создаёт новый с запрошенными вакансиями"""
        try:
            # Список стоп-слов (можно расширить)

            with open(
                self.stop_words, "r", encoding="utf-8"
            ) as f:  # Загрузка json-файла со стоп-словами
                stop_words = set(json.load(f))

            if self.sorted_vacancy.lower() in stop_words:  # Проверка на стоп-слово
                print("Поиск отменён: стоп-слово.")
                return False

            matched_vacancies = []
            with open(
                self.json_data, "r", encoding="utf-8"
            ) as json_file:  # Загрузка файла
                data_json = json.load(json_file)

                for obj_items in data_json.get("items", []):  # Раскрываем items
                    if self.sorted_vacancy.lower() in obj_items["name"].lower():
                        matched_vacancies.append(
                            obj_items
                        )  # Добавление для создания единого массива

            if matched_vacancies:
                with open(
                    self.new_vacancy_file, "w", encoding="utf-8"
                ) as new_file:  # Сохранение в файл
                    json.dump(matched_vacancies, new_file, ensure_ascii=False, indent=4)
                print(
                    f"Сохранено {len(matched_vacancies)} вакансий."
                )  # Сообщение один раз!
            else:
                print("Ничего не найдено.")

            return bool(matched_vacancies)  # True, если есть результат

        except json.JSONDecodeError as e:
            print(f"Ошибка при обработке JSON: {e}")
        except FileNotFoundError:
            print(f"Файл {self.json_data} не найден.")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")

    def removal_of_vacancies(self):
        """Метод позволяет удалять вакансии в созданном json-файле"""
        if self.delete_vacancy != "нет".lower():
            with open(self.new_vacancy_file, "r", encoding="utf-8") as f:  # Чтение
                list_with_dict = json.load(f)
            # Создаем новый список без удаляемой вакансии
            updated_list = [
                dict_w_vac
                for dict_w_vac in list_with_dict
                if self.delete_vacancy.lower() not in dict_w_vac["name"].lower()
            ]
            # Проверяем, действительно ли что-то было удалено
            if len(updated_list) == len(list_with_dict):
                print(f"Вакансия '{self.delete_vacancy}' не найдена.")
                return
            # Записываем обновленный список обратно в файл
            with open(self.new_vacancy_file, "w", encoding="utf-8") as f:
                json.dump(updated_list, f, ensure_ascii=False, indent=2)
                print(f"Информация успешно удалена по: '{self.delete_vacancy}'.")


obj_cl = CreatedJson()
obj_cl.created_new_file()
obj_cl.removal_of_vacancies()
