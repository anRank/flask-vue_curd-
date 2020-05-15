import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, request, flash
import ast
import json
import sqlite3 as sql


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todolist(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(64))
    mission = db.Column(db.String(64))
    level = db.Column(db.String(64))

    def __init__(self, date, mission, level):
        self.date = date
        self.mission = mission
        self.level = level

    def __repr__(self):
        return '<Todolist %r>' % self.mission


@app.route('/')
def index():
    return render_template('test2.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        data = request.data.decode()
        if data != '':  # 这里有个异步的问题。。
            d = eval(data)
            date = d['date']
            mission = d['mission']
            level = d['level']
            newlist = Todolist(date, mission, level)
            db.session.add(newlist)
            db.session.commit()
        return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/readdata')
def readdata():
    con = sql.connect("data.sqlite")
    con.row_factory = sql.Row
    cur = con.cursor()
    cursor = cur.execute("select date, mission, level from todolist")
    res = ''
    for row in cursor:
        res = res + ' ' + str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2])
    return res


@app.route('/deletedata', methods=['GEt', 'POST'])
def deletedata():
    data = request.data.decode()
    if request.method == 'POST':
        if data != '':  # 这里有个异步的问题。。
            d = eval(data)
            date = d['date']
            mission = d['mission']
            level = d['level']
            newlist = Todolist.query.filter_by(date=date, mission=mission, level=level).first()
            db.session.delete(newlist)
            db.session.commit()
            print('ok')
            return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    data = request.data.decode()
    if request.method == 'POST':
        if data != '':  # 这里有个异步的问题。。
            d = eval(data)
            date = d['date']
            mission = d['mission']
            level = d['level']
            upd = d['new']
            nlist = Todolist.query.filter_by(date=date, mission=mission, level=level).first()
            nlist.mission = upd
            db.session.commit()
            return render_template('index.html')
    else:
        return render_template('index.html')
    data = request.data.decode()


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
