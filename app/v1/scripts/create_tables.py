#from app.v1.model.main_models import Usuarios,Noticias,NoticiasConsumidas
from app.v1.model.user_model import User
from app.v1.model.news_model import News
from app.v1.model.userNews_model import UserNews

from app.v1.utils.db import db

def create_tables():
    with db:
        db.create_tables([User, News, UserNews])
        print('las tablas se han creado correctamente')