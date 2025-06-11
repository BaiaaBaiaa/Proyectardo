from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    first_name: str
    last_name: str
    username: EmailStr  # será el correo
    password: str

class UsuarioLogin(BaseModel):
    username: EmailStr
    password: str

class UsuarioOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: EmailStr

    class Config:
        from_attributes = True  # pydantic v2
