from urllib import request
from flask import Flask
from flask import redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from os import getenv


app = Flask(__name__,template_folder='templates')
import routes

