from db import db

def addResult(quiz_id, user_id, rightCounter, wrongCounter, correct):
    if correct:
        rights = rightCounter + 1
        wrongs = wrongCounter
    else:
        rights = rightCounter
        wrongs = wrongCounter + 1
        print(quiz_id, user_id, rights, wrongs, correct)
    sql = "INSERT INTO results (quiz_id, user_id, rights, wrongs) VALUES (:quiz_id, :user_id, :rights, :wrongs)"
    db.session.execute(sql, {"quiz_id":quiz_id, "user_id":user_id, "rights":rights, "wrongs":wrongs})
    db.session.commit()
    return

def getResult(quiz_id, user_id):
    print(quiz_id, user_id )
    sql = "SELECT rights, wrongs FROM results WHERE quiz_id=:quiz_id AND user_id=:user_id"
    
    return db.session.execute(sql, {"quiz_id":quiz_id, "user_id":user_id}).fetchall()

def getResultsByUser(user_id):
    sql = "SELECT quiz_id, rights, wrongs FROM resultsStorage WHERE user_id=:user_id"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def getResultsByQuiz(quiz_id):
    sql = "SELECT user_id, rights, wrongs FROM resultsStorage WHERE quiz_id=:quiz_id"
    return db.session.execute(sql, {"quiz_id":quiz_id}).fetchall()

def finalResult(quiz_id, user_id, counters, answer : bool):
    ##save result adding 1 to counters, delete old result
    ##check that result works,
    print(quiz_id, user_id, counters, answer)
    print(counters[0][0])
    print(counters[0][1])
    rights = counters[0][0]
    wrongs = counters[0][1]
    if answer:
        rights = rights + 1
    else:
        wrongs = wrongs + 1
        
    sql = "INSERT INTO resultsStorage (quiz_id, user_id, rights, wrongs) VALUES (:quiz_id, :user_id, :rights, :wrongs) RETURNING id"
    sql2 = "DELETE FROM results WHERE quiz_id= :quiz_id AND user_id= :user_id"
    result_id = db.session.execute(sql, {"quiz_id":quiz_id, "user_id":user_id, "rights":rights, "wrongs":wrongs})
    db.session.execute(sql2, {"quiz_id":quiz_id, "user_id":user_id})
    db.session.commit()
    return result_id
