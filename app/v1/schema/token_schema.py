#creacion del modelo para los tokens
from pydantic import BaseModel
from typing import Optional

#objeto que retorna el token y el tipo de autenticacion
class Token(BaseModel):
    access_token: str
    token_type: str

#almacena el username de usuario en el token (añadir mas luego)
class TokenData(BaseModel):
    username: Optional[str] = None