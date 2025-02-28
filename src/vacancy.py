class Vacancy:
    def __init__(self, name, url, salary, description):
        self.name = name
        self.url = url
        self.salary = self.validate_salary(salary)
        self.description = description if description is not None else ""

    def validate_salary(self, salary):
        if salary is None:
            return 0  # Если зарплата не указана, считаем её равной 0
        return salary

    def __lt__(self, other):
        return self.salary < other.salary

    def __gt__(self, other):
        return self.salary > other.salary

    def __eq__(self, other):
        return self.salary == other.salary

    @staticmethod
    def cast_to_object_list(vacancies_json):
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
