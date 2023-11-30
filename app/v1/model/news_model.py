import peewee
from app.v1.utils.db import db

# Modelo `noticias`
class News(peewee.Model):
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