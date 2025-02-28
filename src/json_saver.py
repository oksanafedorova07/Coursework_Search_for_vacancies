import json
import os
from abc import ABC, abstractmethod


class FileSaver(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, criteria):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JSONSaver(FileSaver):
    def __init__(self, filename="vacancies.json"):
        self.filename = filename

    def add_vacancy(self, vacancy):
        with open(self.filename, "a") as file:
            json.dump(vacancy.__dict__, file)
            file.write("\n")

    def get_vacancies(self, criteria):
        # Проверяем, существует ли файл
        if not os.path.exists(self.filename):
            return []  # Если файла нет, возвращаем пустой список

        with open(self.filename, "r") as file:
            vacancies = [json.loads(line) for line in file]
            return [v for v in vacancies if criteria(v)]

    def delete_vacancy(self, vacancy):
        # Проверяем, существует ли файл
        if not os.path.exists(self.filename):
            return  # Если файла нет, ничего не делаем

        with open(self.filename, "r") as file:
            vacancies = [json.loads(line) for line in file]
        with open(self.filename, "w") as file:
            for v in vacancies:
                if v["url"] != vacancy.url:
                    json.dump(v, file)
                    file.write("\n")
