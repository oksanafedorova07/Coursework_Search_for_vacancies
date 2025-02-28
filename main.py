from src.hh_api import HeadHunterAPI
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


def user_interaction():
    hh_api = HeadHunterAPI()
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()

    hh_vacancies = hh_api.get_vacancies(search_query)
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

    # Фильтрация вакансий с проверкой на None
    filtered_vacancies = [
        v
        for v in vacancies_list
        if v.description is not None
        and all(word in v.description for word in filter_words)
    ]

    sorted_vacancies = sorted(filtered_vacancies, reverse=True)
    top_vacancies = sorted_vacancies[:top_n]

    json_saver = JSONSaver()
    for vacancy in top_vacancies:
        json_saver.add_vacancy(vacancy)

    for vacancy in top_vacancies:
        print(f"{vacancy.name} - {vacancy.salary} - {vacancy.url}")


if __name__ == "__main__":
    user_interaction()
