#para crear rutas separadas del archivo main
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
#para recuperar info insertada por el usuario
from fastapi import Body

from app.v1.schema import user_schema
from app.v1.service import user_service

from app.v1.utils.db import get_db

#instancia apirouter con prefijo del navegador
router = APIRouter(prefix="/api/v1")

@router.post(
    "/user/",
    #para la agrupacion de endpoints por tipo. Util para la documentacion
    tags=["users"],
    #estado 201 y no 200 porque se crea un dato
    status_code=status.HTTP_201_CREATED,
    #modelo de pydantic de tipo user
    response_model=user_schema.User,
    #dependencia de la bbdd
    dependencies=[Depends(get_db)],
    #para la documentacion
    summary="Create a new user"
)
def create_user(user: user_schema.UserRegister = Body(...)):
    """
    ## Create a new user in the app

    ### Args
    The app can recive next fields into a JSON
    - email: A valid email
    - nombre: Unique username
    - password: Strong password for authentication

    ### Returns
    - user: User info
    """
    return user_service.create_user(user)