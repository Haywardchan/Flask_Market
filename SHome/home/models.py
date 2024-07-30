from home import db, login_manager
from home import bcrypt
from flask_login import UserMixin
from datetime import date
import re

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id= db.Column(db.Integer(), primary_key=True)
    username= db.Column(db.String(length=30), nullable=False, unique=True)
    email_addr= db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash= db.Column(db.String(length=60), nullable=False)
    budget= db.Column(db.Integer(),nullable=False, default=1000)
    items= db.relationship('Item', backref='owned_user', lazy=True)

    # @property
    # def prettier_budget(self):
    #     if len(str(self.budget)) > 3:
    #         return f'${str(self.budget)[:-3]},{str(self.budget)[-3:]}'
    #     else:
    #         return f'${self.budget}'

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    # def can_purchase(self, item_obj):
    #     return self.budget >= item_obj.price
    
    # def can_sell(self, item_obj):
    #     return item_obj in self.items

class Item(db.Model):
    # limits the length of name 
    id= db.Column(db.Integer(), primary_key=True)
    name= db.Column(db.String(length=30), nullable=False, unique=True)
    count= db.Column(db.Integer(), nullable=False)
    total_count= db.Column(db.Integer(), nullable=False)
    consumption = db.Column(db.Integer(), nullable=False)
    description= db.Column(db.String(length=1024), nullable=False, unique=True)
    owner= db.Column(db.Integer(), db.ForeignKey('user.id'))
    creationdate= db.Column(db.Integer(), nullable=False)
    def __repr__(self):
        return f'Item{self.name}'

    def reduce_item(self, user):
        regex = '\d+'
        dates=list(map(int,re.findall(regex, self.creationdate)))
        diff=(date.today()-date(dates[0], dates[1], dates[2])).days
        self.count=self.total_count
        if self.count-self.consumption*diff>0:
            self.count-=self.consumption*diff
        else: 
            self.count=0
        db.session.commit()
    # def sell(self, user):
    #     self.owner = None
    #     user.budget += self.price
    #     db.session.commit()
    def recharge_items(self, user):
        self.creationdate=date.today()
        db.session.commit()