import json

import pytest

from src.json_saver import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def json_saver(tmpdir):
    # Используем временный файл для тестов
    filename = tmpdir.join("test_vacancies.json")
    return JSONSaver(filename=str(filename))


def test_add_vacancy(json_saver):
    vacancy = Vacancy(
        "Python Developer",
        "https://hh.ru/vacancy/123456",
        100000,
        "Требования: опыт работы от 3 лет...",
    )
    json_saver.add_vacancy(vacancy)

    # Проверяем, что файл содержит добавленную вакансию
    with open(json_saver.filename, "r") as file:
        data = json.loads(file.readline())
        assert data["name"] == "Python Developer"
        assert data["url"] == "https://hh.ru/vacancy/123456"
        assert data["salary"] == 100000
        assert data["description"] == "Требования: опыт работы от 3 лет..."


def test_get_vacancies(json_saver):
    vacancy1 = Vacancy(
        "Python Developer",
        "https://hh.ru/vacancy/123456",
        100000,
        "Требования: опыт работы от 3 лет...",
    )
    vacancy2 = Vacancy(
        "Java Developer",
        "https://hh.ru/vacancy/654321",
        120000,
        "Требования: опыт работы от 5 лет...",
    )
    json_saver.add_vacancy(vacancy1)
    json_saver.add_vacancy(vacancy2)

    # Получаем вакансии с зарплатой больше 100000
    criteria = lambda v: v["salary"] > 100000
    vacancies = json_saver.get_vacancies(criteria)

    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Java Developer"


def test_delete_vacancy(json_saver):
    vacancy1 = Vacancy(
        "Python Developer",
        "https://hh.ru/vacancy/123456",
        100000,
        "Требования: опыт работы от 3 лет...",
    )
    vacancy2 = Vacancy(
        "Java Developer",
        "https://hh.ru/vacancy/654321",
        120000,
        "Требования: опыт работы от 5 лет...",
    )
    json_saver.add_vacancy(vacancy1)
    json_saver.add_vacancy(vacancy2)

    # Удаляем вакансию Python Developer
    json_saver.delete_vacancy(vacancy1)

    # Проверяем, что осталась только одна вакансия
    with open(json_saver.filename, "r") as file:
        vacancies = [json.loads(line) for line in file]
        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Java Developer"


def test_empty_file(json_saver):
    # Проверяем, что get_vacancies возвращает пустой список для пустого файла
    vacancies = json_saver.get_vacancies(lambda v: True)
    assert len(vacancies) == 0


def test_delete_nonexistent_vacancy(json_saver):
    vacancy1 = Vacancy(
        "Python Developer",
        "https://hh.ru/vacancy/123456",
        100000,
        "Требования: опыт работы от 3 лет...",
    )
    vacancy2 = Vacancy(
        "Java Developer",
        "https://hh.ru/vacancy/654321",
        120000,
        "Требования: опыт работы от 5 лет...",
    )
    json_saver.add_vacancy(vacancy1)

    # Пытаемся удалить вакансию, которой нет в файле
    json_saver.delete_vacancy(vacancy2)

    # Проверяем, что файл не изменился
    with open(json_saver.filename, "r") as file:
        vacancies = [json.loads(line) for line in file]
        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Python Developer"
