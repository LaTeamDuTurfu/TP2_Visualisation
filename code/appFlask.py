from flask import Flask, Request, request, jsonify

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///livres.db"
