from abc import ABC, abstractmethod
import requests

class VacancyAPI(ABC):
    @abstractmethod
    def get_vacancies(self, query):
        pass

class HeadHunterAPI(VacancyAPI):
    def get_vacancies(self, query):
        url = "https://api.hh.ru/vacancies"
        params = {"text": query, "area": 113, "per_page": 100}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()["items"]
        else:
            raise Exception(f"Ошибка при запросе к API: {response.status_code}")
