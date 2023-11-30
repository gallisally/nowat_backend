from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
#para indicar la URL de login y validar token
from fastapi.security import OAuth2PasswordBearer
#libreria jose para validar y generar tokens con JWT
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.v1.model.user_model import User as UserModel
from app.v1.schema.token_schema import TokenData
from app.v1.utils.settings import Settings

settings = Settings()


SECRET_KEY = settings.secret_key
#algoritmo de codificacion
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_expire

#verificacion validez password y generacion de hash a partir de la contraseña
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)

#password hash a guardar en la bbdd
def get_password_hash(password):
    return pwd_context.hash(password)

#permite autenticacion con email y username retornando el username de usuario en caso de que ya exista
def get_user(username: str):
    return UserModel.filter((UserModel.email == username) | (UserModel.username == username)).first()

#comprobacion existencia usuario -> busca si la contraseña coincide
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

#recibe diccionario con info y el tiempo de expiracion a guardar en el token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    #copia los datos para evitar modificar el dicc original
    to_encode = data.copy()
    #calculo fecha expiracion dependiendo si existe
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        #establece una expiración predeterminada de 15 minutos
        expire = datetime.utcnow() + timedelta(minutes=15)
    # Agrega la clave "exp" al diccionario de datos con la fecha de expiración
    to_encode.update({"exp": expire})
    # Codifica el JWT (JSON Web Token) usando jwt.encode
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_token(username, password):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="username de usuario/email o contraseña incorrecta",
            #convencion respuesta HTTP para indicar al cliente que debe incluir un token tipo beares para autenticarse
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

#recibe un token por paramentro
async def get_current_user(token: str = Depends(oauth2_scheme)):
    #define una excepción predeterminada para manejar problemas de credenciales
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        #intenta decodificar el token usando la clave secreta y el algoritmo definidos
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #extraccion username usuario (sub) del payload del token
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        #creacion obketo con el username extraido del token
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    #obtencion usuario correspdiente al username extraido
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    #retorno de objeto usuario si todo ok
    return user