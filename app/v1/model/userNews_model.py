
from datetime import datetime

import peewee
#from .user_model import User

from app.v1.utils.db import db
#from .noticia_model import Noticias
from .user_model import User
from .news_model import News

class UserNews(peewee.Model):
    user = peewee.ForeignKeyField(User)
    noticia = peewee.ForeignKeyField(News)

    class Meta:
            database = db

