from datetime import datetime
from unwrap import db, login_manager
from flask_login import UserMixin

#  https://www.pythoncentral.io/sqlalchemy-expression-language-advanced/
# from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Float
# from sqlalchemy.orm import relationship, backref
# from sqlalchemy.ext.declarative import declarative_base


# Base = declarative_base()
# end from

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=True, nullable=False)
    lastname = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    cart = db.relationship('Cart', backref='buyer', lazy=True)

    def __repr__(self):
        return f"User('{self.firstname}','{self.lastname}', '{self.email}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Products('{self.name}', '{self.price}')"

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    # name = db.Column(db.String(100), db.ForeignKey('products.name'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # items = db.relationship('Products', secondary=cart_with_items, lazy='subquery', backref=backref('carts', lazy=True))

    def __repr__(self):
        return f"Cart('{self.cartproductName}')"
