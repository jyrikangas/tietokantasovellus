from re import S
from db import db

def add_quiz(name, questions):
    sql = "INSERT INTO quizs (name) VALUES (:name) RETURNING id" 
    quiz_id = db.session.execute(sql, {"name":name}).fetchone()[0]
    
    for question in questions.split("\n"):
        parts = question.strip().split(";")
        if len(parts) != 6:
            continue
        sql = "INSERT INTO quiz (quiz_id, qnumber, question, answer, wronganswer_1, wronganswer_2, wronganswer_3) VALUES (:quiz_id, :qnumber, :question, :answer, :wronganswer_1, :wronganswer_2, :wronganswer_3)"
        db.session.execute(sql, {"quiz_id":quiz_id, "qnumber":parts[0],"question":parts[1],"answer":parts[2],"wronganswer_1":parts[3], "wronganswer_2":parts[4], "wronganswer_3":parts[5]})
    db.session.commit()
    return quiz_id

def get_questions(quiz_id):
    sql = "SELECT qnumber, question, answer, wronganswer_1, wronganswer_2, wronganswer_3 FROM quiz WHERE quiz_id=:quiz_id"
    return db.session.execute(sql, {"quiz_id":quiz_id}).fetchall()

def get_question(quiz_id, qnumber):
    sql = "SELECT question, answer, wronganswer_1, wronganswer_2, wronganswer_3 FROM quiz WHERE quiz_id=:quiz_id AND qnumber=:qnumber"
    return db.session.execute(sql, {"quiz_id":quiz_id, "qnumber":qnumber}).fetchall()

def get_quizs():
    sql = "SELECT * from quizs"
    return db.session.execute(sql).fetchall()