from flask import Flask, Request, request, jsonify
from models import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///livres.db"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return "Home Page"
