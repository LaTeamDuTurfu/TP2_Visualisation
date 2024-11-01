from models import db


class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    symbol = db.Column(db.String(5), nullable=False)
    data_year = db.Column(db.Json, nullable=False)
    data_month = db.Column(db.Json, nullable=False)

    def __init__(self, name, symbol, data_year, data_month):
        self.name = name
        self.symbol = symbol
        self.data_year = data_year
        self.data_month = data_month
    