import requests
API_KEY0 = "ANSX5B4IN6HF5B1I"
API_KEY1 = "G7XCJE76LE2I1YE2"
API_KEY2 = "XAIRRBTAGZH13SPP"
API_KEY3 = "88UNJ0ZNOASJ227E"
API_KEY4 = "MYLWAH63FIVH7Y8I"
API_KEY5 = "VI0CJYYC0R4IQMKO"
API_KEY6 = "MEHT739CQ7OC38XN"
API_KEY7 = "TL1EBPOAVKFN6P56"
API_KEY8 = "1O6BQAOX3ZK2GYH6"
API_KEY9 = "FFAIB7TUAP5GWFOH"


def recherche_stock(keyword):
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={API_KEY0}'
    reponse = requests.get(url)
    data = reponse.json()

    if reponse.status_code == 200:
        return data
    else:
        print(f"{reponse.status_code} - {reponse.reason}")
        return None

def get_data_monthly(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={API_KEY0}'
    data = requests.get(url).json()
    return data


def get_data_30_days(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputize=compact&apikey={API_KEY0}'
    data = requests.get(url).json()
    return data
