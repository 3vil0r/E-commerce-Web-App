import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from unwrap import app, db, bcrypt
from unwrap.forms import RegistrationForm, LoginForm, UpdateAccountForm
from unwrap.models import User, Products, Cart
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(lastname=form.lastname.data,firstname=form.firstname.data,email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.lastname = form.lastname.data
        current_user.firstname = form.firstname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.lastname.data = current_user.lastname
        form.firstname.data = current_user.firstname
        form.email.data = current_user.email
    return render_template('account.html', title='Account',
                           form=form)

@app.route("/partners")
def partners():
     return render_template("partners.html", title='Partners')

@app.route("/products-list")
def products_list():
     return render_template("products-list.html", title='Products list')

@app.route("/unwrap-project")
def unwrap_project():
     return render_template("unwrap-project.html", title='The project')


@app.route("/how-it-works")
def how_it_works():
     return render_template("how-it-works.html", title='How it works')


# @app.route("/select_products/new", methods=['GET', 'POST'])
@app.route("/select_products", methods=['GET', 'POST'])
# @login_required
def select_products():
    products = Products.query.all()
    # form = AddToCartForm()
    # if form.validate_on_submit():
    #     # item_to_add = Cart(name=product.name, product_id=product.id, buyer=current_user)
    #     item_to_add = Cart(name=form.name, product_id=form.product_id, buyer=current_user)
    #     db.session.add(item_to_add)
    #     db.session.commit()
    #     flash('Your item has been added to your cart!', 'success')
    #     return redirect(url_for('home'))
    return render_template('select_products.html', products=products)


# <div class="form-group">
                        # {{ form.submit(class="btn btn-outline-info") }}
                        # </div>


@app.route("/product/<int:product_id>")
def queryproduct(product_id):
    product = Products.query.get_or_404(product_id)
    return render_template('product.html', product=product)

    # <a href="{{ url_for('product', product_id=product.id) }}">{{ product.name }}</a>

# @app.route("/addToCart")
# @login_required
# def addToCart():
    
#     product_id = int(request.args.get('product_id'))
#     # user_id = current_user
#     item_to_add = Cart(product_id=product_id, buyer=current_user)
#     db.session.add(item_to_add)
#     db.session.commit()
#     return redirect(url_for('select_products'))

@app.route("/addToCart/<int:product_id>")
@login_required
def addToCart(product_id):
    product = Products.query.get_or_404(product_id)
    item_to_add = Cart(product_id=product.id, buyer=current_user)
    db.session.add(item_to_add)
    db.session.commit()
    return redirect(url_for('select_products'))



@app.route("/cart")
def cart():
    cart = Cart.query.all()
    return render_template('cart.html', cart=cart)