import peewee
from app.v1.utils.db import db

# Modelo `usuarios`
class User(peewee.Model):
    id = peewee.AutoField()
    nombre = peewee.CharField(max_length=100)
    email = peewee.CharField(max_length=100)
    password = peewee.CharField(max_length=100)

    #clase meta que contiene la conexion a la bbdd
    class Meta:
        database = db
        #engine = peewee.PostgresqlDatabase