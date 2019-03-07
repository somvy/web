from db import DB
from user_model import UserModel
from news_model import NewsModel
from items_model import ItemsModel

db = DB()
users_model = UserModel(db.get_connection())
users_model.init_table()
users_model.insert("test1", "11111111", "yandex.fd@mail.ru", "admin")
users_model.insert("admin", "password11", "mainmail@ya.ru", "admin")
news_model = NewsModel(db.get_connection())
news_model.init_table()
items_model = ItemsModel(db.get_connection())
items_model.init_table()
items_model.insert("Defaul candy", "www.yandex.ru", "30", "Classic candy with honey and cream.", "25")
