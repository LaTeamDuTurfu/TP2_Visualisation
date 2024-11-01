import requests
API_KEY = "G7XCJE76LE2I1YE2"


def recherche_stock(keyword):
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={API_KEY}'
    reponse = requests.get(url)
    data = reponse.json()

    if reponse.status_code == 200:
        return data
    else:
        print(f"{reponse.status_code} - {reponse.reason}")
        return None

def get_data_monthly(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={API_KEY}'
    data = requests.get(url).json()
    return data


def get_data_30_days(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputize=compact&apikey={API_KEY}'
    data = requests.get(url).json()
    return data
