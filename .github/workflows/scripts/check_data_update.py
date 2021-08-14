import json
import pathlib
import sys
import datetime
import requests


def get_most_recent_date():
    data_file = pathlib.Path('data.csv')
    with open(data_file, "r") as file:
        last_line = file.readlines()[-1]
    #print(f'last_line=\'{last_line}\'')
    last_date = last_line.split(',')[0]
    #print(f'last_date=\'{last_date}\'')
    #last_date = datetime.datetime.strptime(last_date, "%d-%m-%Y")
    #print(f'last_date=\'{last_date}\'')
    return last_date


def get_data_data_from_api():

    URL = (
        'https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID_ARS_PT_HISTORICO_view/FeatureServer/0/query'
        "?f=json&outFields=*&cacheHint=false"
        '&where=1%3d1'
        '&orderByFields=Data_ARS+desc'
        '&resultRecordCount=10000'
    )
    # print(f"Loading from '{URL}'")
    response = requests.get(URL)

    if response.status_code != 200:
        raise ValueError('Unable to retrieve data from data endpoint. Error %s: $s' % response.status_code, response.text)

    data =  response.json()

    latest_date = data['features'][0]['attributes']['Data_ARS']
    #print(f'latest_date=\'{latest_date}\'')
    latest_date = datetime.datetime.utcfromtimestamp(latest_date / 1000)
    #print(f'latest_date=\'{latest_date}\'')
    latest_date = latest_date.strftime("%d-%m-%Y")
    #print(f'latest_date=\'{latest_date}\'')
    return latest_date


if __name__ == '__main__':

    last_date = get_most_recent_date()

    latest_date = get_data_data_from_api()
    #print(f"last_date={last_date} latest_date={latest_date}")

    try:
        assert last_date == latest_date
    except AssertionError:
        print("TRUE")
        sys.exit()

    print("FALSE")
