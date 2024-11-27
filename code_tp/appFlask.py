from flask import Flask, Request, request, jsonify, send_file
from models import db
from models.stock import Stock
import matplotlib.pyplot as plt
import pandas as pd
from code_tp.alphaAPI import StockAPI
from clientTK import ClientTK
from io import BytesIO

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stocks.db"

db.init_app(app)

with app.app_context():
    db.create_all()

stockAPI = StockAPI()


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


@app.route("/my_stocks/<get_symbol>", methods=["GET"])
def get_stock(get_symbol):
    stocks = Stock.query.get(get_symbol)
    stock = {"id": stocks.id, "name": stocks.name, "symbol": stocks.symbol}
    return jsonify(stock)


@app.route("/my_stocks/<delete_symbol>", methods=["DELETE"])
def delete_stock(delete_symbol):
    Stock.query.filter_by(symbol=delete_symbol).delete()
    db.session.commit()
    return jsonify({"message": "Stock Deleted"}), 201


@app.route('/my_stocks/<graphic_symbol>/30_days', methods=["GET"])
def get_30days_graph(graphic_symbol):
    données_30_jours = stockAPI.get_data_30_days(graphic_symbol)

    # Convertir les données journalières en DataFrame
    daily_data_brut = pd.DataFrame.from_dict(données_30_jours["Time Series (Daily)"], orient="index")
    daily_data = daily_data_brut.head(30)
    daily_data = daily_data.astype(float)  # Convertir toutes les colonnes en float
    daily_data.index = pd.to_datetime(daily_data.index)  # Convertir l'index en datetime
    daily_data.sort_index(inplace=True)

    # Graphique à lignes (30 derniers jours)
    figure = plt.figure(figsize=(12, 6))
    plt.plot(daily_data.index, daily_data["4. close"], marker="o", label="Clôture")
    plt.fill_between(daily_data.index, daily_data["3. low"], daily_data["2. high"], alpha=0.2,
                     label="Range (Low-High)")
    plt.title(f"Prix des 30 derniers jours : {graphic_symbol})")
    plt.ylabel("Prix (USD)")
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()

    tmp_file = f"/tmp/{graphic_symbol}_30_days.png"
    filestream = BytesIO()
    plt.savefig(filestream, format="png")
    filestream.seek(0)

    return send_file(filestream, mimetype="image/png", as_attachment=False, download_name=f"{graphic_symbol}_30_days.png")


@app.route('/my_stocks/<graphic_symbol>/past_year', methods=["GET"])
def get_past_year_graph(graphic_symbol):
    données_monthly = stockAPI.get_data_monthly(graphic_symbol)

    # Convertir les données mensuelles en DataFrame
    monthly_data_brut = pd.DataFrame.from_dict(données_monthly["Monthly Adjusted Time Series"], orient="index")
    monthly_data = monthly_data_brut.head(12)
    monthly_data = monthly_data.astype(float)
    monthly_data.index = pd.to_datetime(monthly_data.index)
    monthly_data.sort_index(inplace=True)

    # Graphique à barres (Prix mensuel)
    figure1 = plt.figure(figsize=(10, 6))
    monthly_data["4. close"].plot(kind="bar", color="skyblue")
    plt.title(f"Prix de clôture mensuel : {graphic_symbol}")
    plt.ylabel("Prix de clôture (USD)")
    plt.xlabel("Mois")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    # Save to temporary file
    tmp_file = f"/tmp/{graphic_symbol}_past_year.png"
    filestream = BytesIO()
    plt.savefig(filestream, format="png")
    filestream.seek(0)

    # Return the file
    return send_file(filestream, mimetype="image/png", as_attachment=False, download_name=f"{graphic_symbol}_past_year.png")


if __name__ == '__main__':
    app.run(debug=True, port=8200, host="127.0.0.1")
