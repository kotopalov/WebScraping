import sys
import pymongo


mongodb_host = 'localhost'
mongodb_port = '27017'


def get_mongo_collection(db_name, col_name):
    myclient = pymongo.MongoClient(f"mongodb://{mongodb_host}:{mongodb_port}/")

    db = myclient[db_name]
    col = db[col_name]

    return col


def get_vacancie_by_selary(min_sel):
    query = {"max_salary": {"$gt": min_sel}}

    v_col = get_mongo_collection('vacancies', 'vacancies_info')
    v_lst = v_col.find(query)
    return v_lst


min_sal = int(sys.argv[1])
v = get_vacancie_by_selary(min_sal)

for el in v:
    print(f"{el['name']} - {el['max_salary']}")
