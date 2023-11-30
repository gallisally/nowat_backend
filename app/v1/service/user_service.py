#para configurar excepciones controladas por fastapi y personalizar respuesta al usuario
#respuesta para el usuario en formato JSON y con un código de estado de HTTP.
from fastapi import HTTPException, status


from app.v1.model.userNews_model import User as UserModel
from app.v1.schema import user_schema
from app.v1.service.auth_service import get_password_hash


#para guardar usuario recibiendo modelo pydantic de UserRegister
def create_user(user: user_schema.UserRegister):

    get_user = UserModel.filter((UserModel.email == user.email) | (UserModel.username == user.username)).first()
    if get_user:
        msg = "email ya registrado"
        #lanzando excepcion si el usuario ya existe
        if get_user.username == user.username:
            msg = "Ya existe ese username de usuario"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )
    #creacion  y guardado de nuevo usuario si no existe
    db_user = UserModel(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password)
    )

    db_user.save()

    return user_schema.User(
        id = db_user.id,
        username = db_user.username,
        email = db_user.email
    )