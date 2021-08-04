import requests
import json

import sys

if len(sys.argv) != 3:
    print("Incorrect arguments")
    print("example: task_02 <username> <usertoken>")
    sys.exit(3)

username = sys.argv[1]
token = sys.argv[2]

data_json = requests.get('https://api.github.com/user/repos', auth=(username, token))
with open('auth_json.txt', 'w') as outfile:
    json.dump(data_json.json(), outfile)


# Вывод: если получать список репозиториев без авторизации как в task_01,
# мы получаем список только публичный репозиториев
# с авторизацией мы получаем список всех репозиториев

