from db import db

def addComment(quiz_id, user_id, text):
    sql = """INSERT INTO comments (quiz_id, user_id, comment) VALUES (:quiz_id, :user_id, :text)"""
    db.session.execute(sql, {"quiz_id":quiz_id, "user_id":user_id, "text":text})
    db.session.commit()
    return

def getCommentsByQuiz(quiz_id):
    sql = "SELECT user_id, comment FROM comments WHERE quiz_id = :quiz_id"
    return db.session.execute(sql, {"quiz_id":quiz_id}).fetchall()
    