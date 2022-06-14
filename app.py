from flask import Flask, request, render_template, redirect
import sqlite3
import hashlib
from typing import Dict, Text, Union
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.cli.command("create-db")
def create_db():
  db.drop_all()
  db.create_all()

# @app.cli.command("add2DB")
# def create_db(filename):
#   with open(filename) as file_in:
#       lines = []
#       for line in file_in:
#           lines.append(line)


def encrypt(string:str) -> None:
  encoded =hashlib.sha256(string.encode()).hexdigest()
  return encoded

@app.route('/')
def home():
  return render_template("home.html", correct=False)


@app.route('/add2DB/<authKey>/<link>')
def add2DB(authKey, link):
  if authKey == 'scary':
    try:
      r = requests.get(link)
      print(r.text)
    finally: 
      return "broken add2DB link"



@app.route('/hash/<text>')
def hash(text):
  try:
    db.session.add(HashPair(hash=encrypt(text), text=text))
    db.session.commit()
  finally: 
    return """<body><style>.fieldset {background-color: #32CD32;font-family: Helvetica, sans-serif;}</style><div> <fieldset   class="fieldset" id="answer">""" + str(text + " is " + str(encrypt(text))) + """</fieldset></div></body>"""



class HashPair(db.Model):
  hash = db.Column(db.String(255), primary_key=True)
  text = db.Column(db.String(255), default=0)


@app.route('/unhash/<hash>')
def unhash(hash : Union[str, None] = None):
  if hash is None:
    return "No hash provided", 400

  hashPair: Union[HashPair, None] = HashPair.query.get(hash)

  if hashPair is None:
    return "Hash not found", 200


  return """<body><style>.fieldset {background-color: #32CD32;font-family: Helvetica, sans-serif;}</style><div> <fieldset   class="fieldset" id="answer">""" + f"""Hash = '{hashPair.text}'""" + """</fieldset></div></body>""", 200


@app.errorhandler(404) 
def invalid_route(e):
  print("broke invalid route")
  return """<body><style>.fieldset {background-color: #FF0000;font-family: Helvetica, sans-serif;}</style><div> <fieldset   class="fieldset" id="answer">Congrats, you broke it</fieldset></div></body"""

if __name__ == "__main__":
  app.run(
	host='0.0.0.0',
	port=8080,
	debug=True,
  )
