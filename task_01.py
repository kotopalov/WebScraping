import requests
import json

username = input("Enter username:")

request = requests.get('https://api.github.com/users/'+username+'/repos')
if request.status_code != 200:
    print("Нет авторизации для пользователя: "+username)
else:
    data_json = request.json()

    # поскольку в задание не идется про какие-то отдельнеые поля,
    # то я сохраняю весь json как есть в файл
    with open('data_json.txt', 'w') as outfile:
        json.dump(data_json, outfile)

    # но можно было бы сохранить отдельные поля пробежавшись по элементам
    # и создав новую json переменную заолнить ее нужными полями
    data_json2 = []
    for i, elem in enumerate(data_json):
        data_json2.append(
            {"name": elem['name'],
             "url": elem['svn_url']}
        )

    with open('data_json2.txt', 'w') as outfile:
        json.dump(data_json2, outfile)
