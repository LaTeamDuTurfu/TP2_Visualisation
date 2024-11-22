import requests


class StockAPI:
    def __init__(self):
        self.API_KEY0 = "ANSX5B4IN6HF5B1I"
        self.API_KEY1 = "G7XCJE76LE2I1YE2"
        self.API_KEY2 = "XAIRRBTAGZH13SPP"
        self.API_KEY3 = "349N53YI24F87Q34"
        self.API_KEY4 = "MYLWAH63FIVH7Y8I"
        self.API_KEY5 = "VI0CJYYC0R4IQMKO"
        self.API_KEY6 = "MEHT739CQ7OC38XN"
        self.API_KEY7 = "TL1EBPOAVKFN6P56"
        self.API_KEY8 = "1O6BQAOX3ZK2GYH6"
        self.API_KEY9 = "FFAIB7TUAP5GWFOH"

        self.API_KEYS = [self.API_KEY0, self.API_KEY1, self.API_KEY2, self.API_KEY3, self.API_KEY4, self.API_KEY5,
                         self.API_KEY6, self.API_KEY7, self.API_KEY8, self.API_KEY9]

        self.current_api_key_num = 3
        self.current_api_key = self.API_KEYS[self.current_api_key_num]

    def recherche_stock(self, keyword):
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={self.current_api_key}'
        return self.faire_requete(url)

    def get_data_monthly(self, symbol):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={self.current_api_key}'
        return self.faire_requete(url)

    def get_data_30_days(self, symbol):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputize=compact&apikey={self.current_api_key}'
        return self.faire_requete(url)

    def faire_requete(self, url):
        print(f"Key #{self.current_api_key_num} used for the request: {self.current_api_key}")
        response = requests.get(url)
        data = response.json()
        print(data)
        return data


