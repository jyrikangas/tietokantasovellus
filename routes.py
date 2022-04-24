from urllib import request
from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from db import db
from app import app
from random import shuffle
import users
import quiz

@app.route("/")
def index():
    db.session.execute("INSERT INTO visitors (time) VALUES (NOW())")
    db.session.commit()
    result = db.session.execute("SELECT COUNT(*) FROM visitors")
    counter = result.fetchone()[0]
    return render_template("index.html", counter=counter) 

@app.route("/login", methods=["get","post"])
def login():
    if request.method == "GET": return render_template("login.html")
    if request.method == "POST": 
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template("error.html")
        return redirect("/")

@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET": return render_template("register.html")
    if request.method == "POST": 
        username = request.form["username"]
        password = request.form["password"]
        if not users.register(username, password):
            return render_template("error.html")
        return redirect("/login")
    
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/quizs")
def quizs():
    return render_template("quizs.html", quizs=quiz.get_quizs())

@app.route("/play/<int:quiz_id>/<int:qnumber>")
def playquiz(quiz_id,qnumber):
    questioncontent = quiz.get_question(quiz_id,qnumber)
    
    question = questioncontent[0][0]
    answers=[questioncontent[0][1],questioncontent[0][2],questioncontent[0][3],questioncontent[0][4]]
    shuffle(answers)
    return render_template("quiz.html",question=question, answer1=answers[0],answer2=answers[1], answer3=answers[2], answer4=answers[3])

#todo input checking
@app.route("/addquiz", methods=["GET","POST"])
def addquiz():
    if request.method == "GET":
        return render_template("addquiz.html")
    
    if request.method == "POST":
        name = request.form["name"]
        words = request.form["words"]
        quiz.add_quiz(name, words)
        return redirect("/quizs/")