from typing import List, Dict, Optional


class Vacancy:
    """Класс для работы с вакансиями."""

    def __init__(self, name: str, url: str, salary: Optional[int], description: Optional[str]) -> None:
        """Инициализирует экземпляр вакансии."""
        self.name = name  # Название вакансии.
        self.url = url  # Ссылка на вакансию.
        self.salary = self._validate_salary(salary)  # Зарплата. Если не указана, будет установлена в 0.
        self.description = self._validate_description(description)  # Описание вакансии или требования.

    def _validate_salary(self, salary: Optional[int]) -> int:
        """Проверяем зарплату. Если зарплата не указана, возвращает 0."""
        if salary is None:
            return 0
        return salary

    def _validate_description(self, description: Optional[str]) -> str:
        """Проверяем описание. Если описание не указано, возвращает пустую строку."""
        if description is None:
            return ""
        return description

    def __lt__(self, other: 'Vacancy') -> bool:
        """Сравнивает вакансии по зарплате (меньше)."""
        return self.salary < other.salary

    def __gt__(self, other: 'Vacancy') -> bool:
        """Сравнивает вакансии по зарплате (больше)."""
        return self.salary > other.salary

    def __eq__(self, other: 'Vacancy') -> bool:
        """Сравнивает вакансии по зарплате (равенство)."""
        return self.salary == other.salary

    @staticmethod
    def cast_to_object_list(vacancies_json: List[Dict]) -> List['Vacancy']:
        """Преобразует список словарей с данными о вакансиях в список объектов Vacancy."""
        vacancies = []
        for item in vacancies_json:
            name = item.get("name")
            url = item.get("alternate_url")
            salary = item.get("salary")
            if salary is not None:
                salary = salary.get("from")
            description = item.get("snippet", {}).get("requirement", "")
            vacancies.append(Vacancy(name, url, salary, description))
        return vacancies
