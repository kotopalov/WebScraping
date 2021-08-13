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


def is_exist(col, el):
    # v_lst = col.find(el)
    v_lst = col.find({'url': el['url']})
    v_lst = list(v_lst)
    if len(v_lst) > 0:
        return True
    return False


def remove_exist(col, row_list):
    new_list = list()
    for el in row_list:
        if not is_exist(col, el):
            new_list.append(el)
    return new_list


def add_new_data_to_db(row_list):
    v_col = get_mongo_collection('vacancies', 'vacancies_info')
    print(type(row_list))
    row_list = remove_exist(v_col, row_list)
    # if row_list.count() > 0:
    if len(list(row_list)) > 0:
        v_col.insert_many(row_list)


job_title = sys.argv[1]
page_count = int(sys.argv[2])

arr_vacancies = []
arr_vacancies = get_superjob_vacancies(arr_vacancies, job_title, page_count)
arr_vacancies = get_HH_vacancies(arr_vacancies, job_title, page_count)

add_new_data_to_db(arr_vacancies)
