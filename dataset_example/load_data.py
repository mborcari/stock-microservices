import json
from os import path
import csv
import requests

URL_BASE = 'youappurl

def load_stock():
    '''
    Função pra carregar ativos da bovespa
    '''

    file = 'stocks_list.csv'
    path_full = f'{path.dirname(path.abspath(__file__))}\\{file}'
    with open(path_full, encoding='ISO-8859-1') as csv_file:
        csv_read = csv.reader(csv_file, delimiter=';')
        for row in csv_read:
            code_stock, name, category, data_source = row[0], row[1], row[2], row[3]
            print(f'Creating stocks {code_stock}')
            body = {
                        "code": code_stock,
                        "name": name,
                        "category": category,
                        "data_source": data_source
                    }
            body = json.dumps(body)
            s = requests.Session()
            s.headers.update({
                            "content-Type": "application/json",
                            "Accept": "application/json",
                            "Cache-Control": "no-cache"
                            })
            r = s.post(url=URL_BASE, data=body)
            print(f'return {r}')


if __name__ == '__main__':
    load_stock()
