from flask import Flask, render_template 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from market.config import DEV_DB, PROD_DB
import os

app=Flask(__name__) # build application object
if os.environ.get('DEBUG')=='1':
    app.config['SQLALCHEMY_DATABASE_URI'] = DEV_DB
else: 
    app.config['SQLALCHEMY_DATABASE_URI'] = PROD_DB

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '4da3282a970dc5e72b1f5cc6'
db = SQLAlchemy(app)
app.app_context().push()
bcrypt=Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from market import routes

with app.app_context():
    db.create_all()