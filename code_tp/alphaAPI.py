import requests


class StockAPI:
    def __init__(self):
        self.current_api_key = "ANSX5B4IN6HF5B1I"

    @staticmethod
    def faire_requête(url):
        response = requests.get(url)
        data = response.json()
        return data

    def recherche_stock(self, keyword):
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={self.current_api_key}'
        return self.faire_requête(url)

    def get_data_monthly(self, symbol):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={self.current_api_key}'
        return self.faire_requête(url)

    def get_data_30_days(self, symbol):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputize=compact&apikey={self.current_api_key}'
        return self.faire_requête(url)


