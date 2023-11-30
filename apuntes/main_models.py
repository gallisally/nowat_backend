import peewee

from app.v1.utils.db import db
#import peewee


# Modelo `usuarios`
class Usuarios(peewee.Model):
    id = peewee.AutoField()
    nombre = peewee.CharField(max_length=100)
    email = peewee.CharField(max_length=100)
    password = peewee.CharField(max_length=100)

    #clase meta que contiene la conexion a la bbdd
    class Meta:
        database = db
        #engine = peewee.PostgresqlDatabase

# Modelo `noticias`
class Noticias(peewee.Model):
    id = peewee.AutoField()
    nombre_medio = peewee.CharField(max_length=100)
    tipo_medio = peewee.CharField(max_length=50)
    url = peewee.CharField(max_length=10000)
    seccion = peewee.CharField(max_length=500)
    titulo = peewee.CharField(max_length=5000)
    autor = peewee.CharField(max_length=500)
    fecha_publicacion = peewee.DateTimeField()
    resumen = peewee.CharField(max_length=100000)
    texto = peewee.TextField()
    keywords = peewee.CharField(max_length=1000)
    tema = peewee.CharField(max_length=100)
    asunto = peewee.CharField(max_length=300)
    subjetividad = peewee.DoubleField()
    polaridad = peewee.DoubleField()
    imagen_principal = peewee.CharField(max_length=10000)
    imagenes_2 = peewee.TextField()

    class Meta:
        database = db
        #engine = peewee.PostgresqlDatabase

# Modelo `noticias_consumidas`
class NoticiasConsumidas(peewee.Model):
    id = peewee.AutoField()
    usuario = peewee.ForeignKeyField(Usuarios, backref="noticias_consumidas")
    noticia = peewee.ForeignKeyField(Noticias, backref="usuarios_consumidores")

    class Meta:
        database = db
        #engine = peewee.PostgresqlDatabase

# Creamos la base de datos
database = db
database.connect()

# Creamos las tablas
Usuarios.create_table()
Noticias.create_table()
NoticiasConsumidas.create_table()

# Cerramos la conexión a la base de datos
database.close()