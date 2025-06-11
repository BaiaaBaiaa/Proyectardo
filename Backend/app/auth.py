from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from . import models, schemas
from .database import SessionLocal
from .schemas import UsuarioLogin  # <--- esto debe estar

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "secreto"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@router.post("/register")
def register(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(models.Usuario).filter_by(username=user.username).first():
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    hashed = hash_password(user.password)
    db_user = models.Usuario(
    first_name=user.first_name,
    last_name=user.last_name,
    username=user.username,
    password=hashed
)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "Usuario creado"}

@router.post("/login")
def login(user: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter_by(username=user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    token = create_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def read_me(current_user: str = Depends(get_current_user)):
    return {"user": current_user}

