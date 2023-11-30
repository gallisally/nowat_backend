#para configurar excepciones controladas por fastapi y personalizar respuesta al usuario
#respuesta para el usuario en formato JSON y con un código de estado de HTTP.
from fastapi import HTTPException, status

from passlib.context import CryptContext

from app.v1.model.userNews_model import User as UserModel
from app.v1.schema import user_schema

#instancia de cryptcontext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#encriptacion contraseña
def get_password_hash(password):
    return pwd_context.hash(password)
#para guardar usuario recibiendo modelo pydantic de UserRegister
def create_user(user: user_schema.UserRegister):

    get_user = UserModel.filter((UserModel.email == user.email) | (UserModel.nombre == user.nombre)).first()
    if get_user:
        msg = "email ya registrado"
        #lanzando excepcion si el usuario ya existe
        if get_user.nombre == user.nombre:
            msg = "Ya existe ese nombre de usuario"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )
    #creacion  y guardado de nuevo usuario si no existe
    db_user = UserModel(
        nombre=user.nombre,
        email=user.email,
        password=get_password_hash(user.password)
    )

    db_user.save()

    return user_schema.User(
        id = db_user.id,
        nombre = db_user.nombre,
        email = db_user.email
    )