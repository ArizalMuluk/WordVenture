from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
import os
from dotenv import load_dotenv
from flask_mysqldb import MySQL
from flask import Flask
import bcrypt


load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


mysql = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('auth'))


if __name__ == '__main__':
    app.run(debug=True)