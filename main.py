from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json
import mysql.connector
import pymysql

local_server=True
with open("config.json","r")as c:
    params=json.load(c)["params"]

app = Flask(__name__,template_folder='template')
# app.config.update(
#     MAIL_SERVER="smtp.gmail.com",
#     MAIL_PORT="465",
#     MAIL_USE_SSL=True,
#     MAIL_USERNAME=params["gmail_user"],
#     MAIL_PASSWORD=params["gmail_pass"]
# )
# mail=Mail(app)

if local_server:
        app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["production_uri"]
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(120), nullable=True)

@app.route("/")
def About():
    return render_template('index.html',params=params)

@app.route("/experience")
def Experience():
    return render_template('index.html',params=params)

@app.route("/education")
def Education():
    return render_template('index.html',params=params)

@app.route("/skills")
def Skills():
    return render_template('index.html',params=params)

@app.route("/interests")
def Interests():
    return render_template('index.html',params=params)

@app.route("/awards")
def Awards():
    return render_template('index.html',params=params)

@app.route("/posts_comment", methods=['GET','POST'])
def posts_comment():
       if(request.method=='POST'):
            uname = request.form.get('name')
            email =request.form.get('email')
            phone = request.form.get('phone')
            message =request.form.get('message')

            entry=Contact(name=uname, email=email, phone=phone, message=message, date=datetime.now())
            db.session.add(entry)
            db.session.commit()
       return render_template('index.html',params=params)

@app.route("/show")
def show_posts():
    post=Contact.query.all()
    return render_template('show.html',params=params, posts=post)

@app.route("/delete/<string:id>")
def delete(id):
    post=Contact.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    return render_template('show.html',params=params, posts=post, id=id)

app.run(debug=True)