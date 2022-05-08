from db import db

def addResult(quiz_id, user_id, rightCounter, wrongCounter, correct):
    if correct:
        rights = rightCounter
        wrongs = wrongCounter
        rights = rights+1
    else:
        rights = rightCounter
        wrongs = wrongCounter + 1
        print(quiz_id, user_id, rights, wrongs, correct)
    if getResult(quiz_id, user_id):
        sql = "UPDATE results SET rights=:rights, wrongs=:wrongs WHERE quiz_id=:quiz_id AND user_id=:user_id"
        db.session.execute(sql, {"quiz_id":quiz_id, "user_id":user_id, "rights":rights, "wrongs":wrongs})
        db.session.commit()
        return
    sql = """INSERT INTO results (quiz_id, user_id, rights, wrongs) 
    VALUES (:quiz_id, :user_id, :rights, :wrongs)"""
    db.session.execute(sql, {"quiz_id":quiz_id, "user_id":user_id, "rights":rights, "wrongs":wrongs})
    db.session.commit()
    return

def getResult(quiz_id, user_id):
    print(quiz_id, user_id )
    sql = """SELECT rights, wrongs FROM results 
    WHERE quiz_id=:quiz_id AND user_id=:user_id"""
    
    return db.session.execute(sql, {"quiz_id":quiz_id, "user_id":user_id}).fetchall()

def get_results_by_user(user_id):
    sql = "SELECT quiz_id, rights, wrongs, correctPercent FROM resultsStorage WHERE user_id=:user_id"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def get_results_by_quiz(quiz_id):
    sql = "SELECT user_id, rights, wrongs, correctPercent FROM resultsStorage WHERE quiz_id=:quiz_id"
    return db.session.execute(sql, {"quiz_id":quiz_id}).fetchall()

def get_avg_score_by_quiz(quiz_id):
    sql = "SELECT AVG(correctPercent) FROM resultsStorage WHERE quiz_id = :quiz_id"
    return db.session.execute(sql, {"quiz_id":quiz_id}).fetchone()[0]

def get_best_result_on_quiz_by_user(quiz_id,user_id):
    sql = """SELECT MAX(correctPercent) FROM resultsStorage 
    WHERE quiz_id = :quiz_id AND user_id = :user_id"""
    return db.session.execute(sql, {"quiz_id":quiz_id,"user_id":user_id}).fetchone()[0]

def final_result(quiz_id, user_id, counters, answer : bool):
    ##save result adding 1 to counters, delete old result
    ##check that result works,
    print(quiz_id, user_id, counters, answer)
    print(counters[0][0])
    print(counters[0][1])
    rights = int(counters[0][0])
    wrongs = int(counters[0][1])
    if answer:
        rights = rights + 1
    else:
        wrongs = wrongs + 1
    
    correct_percent = int((rights/(rights+wrongs))*100)
    
    sql = """INSERT INTO resultsStorage (quiz_id, user_id, rights, wrongs, correctPercent) 
    VALUES (:quiz_id, :user_id, :rights, :wrongs, :correctPercent) RETURNING id"""
    sql2 = "DELETE FROM results WHERE quiz_id= :quiz_id AND user_id= :user_id"
    result_id = db.session.execute(sql, {"quiz_id":quiz_id, "user_id":user_id, "rights":rights, "wrongs":wrongs, "correctPercent":correct_percent})
    db.session.execute(sql2, {"quiz_id":quiz_id, "user_id":user_id})
    db.session.commit()
    return result_id

def result_count_by_quiz(quiz_id):
    sql = """SELECT COUNT(*) FROM resultStorage WHERE quiz_id = :quiz_id"""
    return db.session.execute(sql, {"quiz_id":quiz_id}).fetchone[0]