from flask import request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from db import db
from app import app
from random import shuffle
import users
import quiz
import result
import comments

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET": return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template("error.html")
        return redirect("/")
    return redirect("/")

@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET": return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.register(username, password):
            return render_template("error.html", message="registration failed")
        return redirect("/login")
    return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/quizs")
def quizs():
    quizs=quiz.get_quizs()
    return render_template("quizs.html", quizs=quizs)

@app.route("/play")
def play():
    quizs = quiz.get_quizs()
    return render_template("quizs.html", quizs=quizs)


@app.route("/play/<int:quiz_id>/<int:qnumber>", methods=["get", "post"])
def playquiz(quiz_id, qnumber):
    if request.method == "GET":
        questioncontent = quiz.get_question(quiz_id, qnumber)
        question = questioncontent[0][0]
        answers = [questioncontent[0][1], questioncontent[0][2], questioncontent[0][3], questioncontent[0][4]]
        shuffle(answers)
        return render_template("quiz.html", question=question, answer1=answers[0], answer2=answers[1], answer3=answers[2], answer4=answers[3], quizid=quiz_id, qnum=qnumber)

    if request.method == "POST":

        users.check_csrf()
        questioncontent = quiz.get_question(quiz_id, qnumber)
        correct = False
        submittedanswer = request.form["answer"]
        if submittedanswer == questioncontent[0][1]:
            correct = True
        user_id = users.user_id()
        if qnumber == 1:
            counters = [(0, 0)]
        else:
            counters = result.getResult(quiz_id, user_id)
        nextquestioncontent = quiz.get_question(quiz_id, qnumber+1)
        if not nextquestioncontent:

            if correct:
                result.finalResult(quiz_id, user_id, counters, correct)
                rights = counters[0][0] + 1 
                wrongs = counters[0][1]
                return render_template("finished.html", evaluation="CORRECT", answer=questioncontent[0][1], rights=rights, wrongs=wrongs)
            else:
                result.finalResult(quiz_id, user_id, counters, correct)
                rights = counters[0][0]
                wrongs = counters[0][1] + 1 
                return render_template("finished.html", evaluation="INCORRECT", answer=questioncontent[0][1], rights=rights, wrongs=wrongs)
        else:
            rights = counters[0][0]
            wrongs = counters[0][1]
            if correct:
                result.addResult(quiz_id, user_id, rights, wrongs, correct)
                return render_template("answer.html", evaluation="CORRECT", answer=questioncontent[0][1], quizid=quiz_id, qnum=qnumber+1)
            else:
                result.addResult(quiz_id, user_id, rights, wrongs, correct)
                return render_template("answer.html", evaluation="INCORRECT", answer=questioncontent[0][1], quizid=quiz_id, qnum=qnumber+1)
    return redirect("/")

@app.route("/addquiz", methods=["GET", "POST"])
def addquiz():
    if request.method == "GET":
        return render_template("addquiz.html")

    if request.method == "POST":
        users.check_csrf()
        name = request.form["name"]
        words = request.form["words"]
        quiz.add_quiz(name, words)
        return redirect("/quizs")
    return redirect("/")

@app.route("/user/<int:user_id>/results")
def userresults(user_id):
    userResults = result.getResultsByUser(user_id)
    userName = users.getUsersName(user_id)
    return render_template("results.html", text="results from user " + userName, results=userResults)

@app.route("/quiz/<int:quiz_id>/results")
def quizresults(quiz_id):
    quizResults = result.getResultsByQuiz(quiz_id)
    quizName = quiz.getQuizName(quiz_id)
    return render_template("results.html", text="results from quiz " + quizName, results=quizResults)

@app.route("/quiz/<int:quiz_id>", methods=["GET", "POST"])
def quizpage(quiz_id):
    if request.method == "GET":
        user_id = users.user_id()
        quizname = quiz.getQuizName(quiz_id)
        average = result.getAvgScoreByQuiz(quiz_id)
        allcomments = comments.getCommentsByQuiz(quiz_id)
        if user_id:
            best = result.getBestResultOnQuizByUser(quiz_id, user_id)
            if best:
                return render_template("quizinfo.html", quizname=quizname, average=average, best="Your best result on this quiz: " + str(int(best)) + "%", quiz_id=quiz_id, commentlist=allcomments)
        return render_template("quizinfo.html", quizname=quizname, average=average, commentlist=allcomments)

    if request.method == "POST":
        users.check_csrf()
        user_id = users.user_id()
        text = request.form["comment"]
        comments.addComment(quiz_id, user_id, text)
        return redirect("/quiz/"+str(quiz_id))
    return redirect("/")