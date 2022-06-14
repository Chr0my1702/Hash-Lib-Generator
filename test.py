from flask import Flask, request, render_template, redirect
import sqlite3
import hashlib
from typing import Dict, Text, Union
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests


# To create a new database, run the following command:
#>>> from test import db
#>>> db.create_all()

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class HashPair(db.Model):
  hash = db.Column(db.String(255), primary_key=True)
  text = db.Column(db.String(255), default=0)

@app.before_first_request
def create_tables():
    db.create_all()

@app.cli.command("create-db")
def create_db():
  db.drop_all()
  db.create_all()

def encrypt(string:str):
  encoded =hashlib.sha256(string.encode()).hexdigest()
  return encoded

with open("10-million-password-list-top-1000000.txt") as file_in:
    for index, line in enumerate(file_in):
        db.session.add(HashPair(hash=encrypt((line[:-1])), text=(line[:-1])))
        if index % 1000000 == 0:
            db.session.commit()

    db.session.commit()