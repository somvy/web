from flask import Flask, redirect, render_template, session
from login_form import LoginForm
from add_news_form import AddNewsForm
from add_item_form import AddItemForm
from register_form import RegisterForm
from db import DB
from user_model import UserModel
from news_model import NewsModel
from items_model import ItemsModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db = DB()
current_user_mode = 'userid'


def exits(args):
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UserModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        print(exists)
        if (exists[0]):
            session['username'] = user_name
            session['user_id'] = exists[1]
            current_user_mode = exists[2]
        return redirect("/index")
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    print(current_user_mode)
    if 'username' not in session:
        return redirect('/login')
    if current_user_mode == 'user':
        return redirect('/access_denied')
    form = AddNewsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        nm = NewsModel(db.get_connection())
        nm.insert(title, content, session['user_id'])
        return redirect("/index")
    return render_template('add_news.html', title='Добавление новости', form=form, username=session['username'])


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        passwordagain = form.password_again.data
        email = form.email.data
        user_type = form.mode.data
        if password == passwordagain:
            um = UserModel(db.get_connection())
            um.insert(name, password, email, user_type)
            exi = um.exists(name, password)
            session['username'] = name
            session['user_id'] = exi[1]
            return redirect("/succes_register")
        else:
            return redirect("/passw_dont_match")
    return render_template('register.html', form=form)


@app.route('/succes_register')
def success_register():
    return render_template('succes_register.html', )


@app.route('/acces_denied')
def access_denied():
    return render_template('access_denied.html')


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if 'username' not in session:
        return redirect('/login')
    if current_user_mode == 'user':
        return redirect('/access_denied')
    form = AddItemForm()
    if form.validate_on_submit():
        name = form.name.data
        image = form.image.data
        price = form.price.data
        info = form.info.data
        count = form.count.data
        im = ItemsModel(db.get_connection())
        im.insert(name, image, price, info, count)
        return redirect("/index")
    return render_template('add_item.html', title='Добавление товара', form=form, username=session['username'])


@app.route('/delete_item/<int:item_id>', methods=['GET'])
def delete_item(item_id):
    if 'username' not in session:
        return redirect('login')
    im = ItemsModel(db.get_connection())
    im.delete(item_id)
    return redirect('/index')


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/index")


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect('/login')
    news = NewsModel(db.get_connection()).get_all(session['user_id'])
    items = ItemsModel(db.get_connection()).get_all()
    return render_template('index.html', username=session['username'], news=news, items=items)


@app.route('/error', methods=['GET', 'POST'])
def error():
    return "error, unknown user"


@app.route('/passw_dont_match')
def no_match():
    return render_template('passw_dont_match.html')


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
