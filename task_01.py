import sys
import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import re
import pymongo


mongodb_host = 'localhost'
mongodb_port = '27017'


def get_salary(text):
    min_s = 0
    max_s = 0

    regex_num = re.compile('\d+[ , , ]\d+')
    result = regex_num.findall(text)
    result = [i.replace(' ', '').replace(' ', '').replace(' ', '') for i in result]

    if len(result) > 0:
        min_s = int(result[0])
        max_s = int(result[-1])

    return min_s, max_s


def get_superjob_vacancies(arr_vacancies, job_name, page_count):
    header = Headers(headers=True).generate()
    for i in range(page_count):
        url = f'https://www.superjob.ru/vacancy/search/?keywords={job_title}&geo%5Bt%5D%5B0%5D=4&page={i + 1}'

        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'lxml')

        vacancies = soup.select('div.f-test-vacancy-item')

        for el in vacancies:
            name = el.find(class_='_6AfZ9').text
            url = 'https://www.superjob.ru' + el.find(class_='_6AfZ9')['href']
            salary = el.find(class_='_1OuF_').text
            min_s, max_s = get_salary(salary)
            source = 'superjob'
            arr_vacancies.append({'name': name,
                                  'salary': salary,
                                  'min_salary': min_s,
                                  'max_salary': max_s,
                                  'url': url,
                                  'source': source
                                  })

    return arr_vacancies


def get_HH_vacancies(arr_vacancies, job_name, page_count):
    header = Headers(headers=True).generate()
    for i in range(page_count):
        url = f'https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&st=searchVacancy&text={job_name}&page={i + 1}'

        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'lxml')

        vacancies = soup.select('div.vacancy-serp-item')

        for el in vacancies:
            name = el.find(class_='bloko-link').text
            url = el.find(class_='bloko-link')['href']
            salary = el.find(class_='vacancy-serp-item__sidebar').text
            min_s, max_s = get_salary(salary)
            source = 'HH'
            arr_vacancies.append({'name': name,
                                  'salary': salary,
                                  'min_salary': min_s,
                                  'max_salary': max_s,
                                  'url': url,
                                  'source': source
                                  })

    return arr_vacancies


def get_mongo_collection(db_name, col_name):
    myclient = pymongo.MongoClient(f"mongodb://{mongodb_host}:{mongodb_port}/")

    db = myclient[db_name]
    col = db[col_name]

    return col


def add_data_to_db(row_list):
    v_col = get_mongo_collection('vacancies', 'vacancies_info')
    v_col.insert_many(row_list)


job_title = sys.argv[1]
page_count = int(sys.argv[2])

arr_vacancies = []
arr_vacancies = get_superjob_vacancies(arr_vacancies, job_title, page_count)
arr_vacancies = get_HH_vacancies(arr_vacancies, job_title, page_count)

add_data_to_db(arr_vacancies)

