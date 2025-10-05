import requests
import json
import pandas as pd
url = f"https://api.tvmaze.com/schedule?country=GB&date=2016-12-25"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    processed_data = []
    for item in data:
        processed_item = {
            'id': item.get('id'),
            'name': item.get('name'),
            'airtime': item.get('airtime'),
            'runtime': item.get('runtime'),
        }

        if 'show' in item:
            show = item['show']
            processed_item['show_name'] = show.get('name')
            processed_item['show_type'] = show.get('type')
            processed_item['show_language'] = show.get('language')

        processed_data.append(processed_item)
        
    df = pd.DataFrame(processed_data)

    print(df.head())
else:
    print(f"Ошибка при загрузке данных: {response.status_code}")
