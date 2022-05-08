
import os
from flask import session, request, abort
from db import db
from werkzeug.security import check_password_hash, generate_password_hash

def login(name, password):
    sql = "SELECT password, id FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_name"] = name
    session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
    del session["user_id"]
    del session["user_name"]
    
def register(name, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (name, password) VALUES (:name, :password)"
        db.session.execute(sql, {"name":name, "password":hash_value})
        db.session.commit()
    except:
        return False
    return True

def user_id():
    return session.get("user_id", 0)

def getUsersName(user_id):
    sql = "SELECT name FROM users WHERE user_id=:user_id"
    return db.session.execute(sql, {"user_id":user_id}).fetchone()[0]

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)