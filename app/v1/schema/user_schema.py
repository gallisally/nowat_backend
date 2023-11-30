from pydantic import BaseModel
from pydantic import Field
#para validar email validez 
from pydantic import EmailStr


class UserBase(BaseModel):
    email: EmailStr = Field(
        ...,
        example="tuemail@ejemplo.com"
    )
    nombre: str = Field(
        ...,
        min_length=3,
        max_length=50,
        example="tuNombreDeUsuario"
    )

#extension de UserBase para retornar info del usuario
class User(UserBase):
    #field para validar tipos de datos
    id: int = Field(
        #campo obligatorio
        ...,
        #ejemplo para el usuario
        example="5"
    )

#extension de UserBase para realizar registro
class UserRegister(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        example="contraseña segura"
    )