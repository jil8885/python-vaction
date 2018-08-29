import json


def save_json():
    customer = {
        'id': '00001',
        'name': '홍길동',
        'history': [
            {'date': '2018-05-22', 'log': True},
            {'date': '2018-05-23', 'log': False},
        ]
    }
    with open('data/03_json_tutorial_json', 'w', encoding='utf-8') as make_file:
        json.dump(customer, make_file, ensure_ascii=False, indent=4)


def load_json():
    with open('data/us-states.json') as f:
        json_test = json.load(f)
        print(json_test)


load_json()