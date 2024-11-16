from flask import Flask, Request, request, jsonify
from models import db
from models.stock import Stock

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stocks.db"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return "Home Page"

@app.route("/my_stocks", methods=["POST"])
def add_stock():
    data = request.get_json()
    new_stock = Stock(name=data["name"], symbol=data["symbol"])
    if db.session.query(Stock).filter(Stock.symbol == data["symbol"]).first():
        return jsonify({"message": "Stock already exists"}), 400
    db.session.add(new_stock)
    db.session.commit()
    return jsonify({"message": "Stock Added"}), 201

@app.route("/my_stocks", methods=["GET"])
def get_stocks():
    stocks = Stock.query.all()
    mes_symboles = []
    for stock in stocks:
        mes_symboles.append({"id": stock.id, "name": stock.name, "symbol": stock.symbol})
    return jsonify(mes_symboles)

@app.route("/my_stocks/<int:id_stock>", methods=["GET"])
def get_stock(id_stock):
    stocks = Stock.query.get(id_stock)
    stock = {"id": stocks.id, "name": stocks.name, "symbol": stocks.symbol}
    return jsonify(stock)

if __name__ == '__main__':
    app.run(debug=True, port=8100, host="127.0.0.1")