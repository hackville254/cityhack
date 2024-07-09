from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import date, datetime
from ninja.errors import HttpError


class LoginSchema(BaseModel):
    email: str
    password: str
    
    
class TokenResponse(BaseModel):
    token: str
    is_client: bool
    is_travailleur: bool


class UserCreateSchema(BaseModel):
    nom: str
    prenom: str
    password: str
    email: str
    pays: str
    ville: str
    categorie:str
    
    @validator('password')
    def validate_password_length(cls, v):
        if len(v) < 8:
            raise HttpError(status_code=400, message="Le mot de passe doit contenir au moins 8 caractères")
        return v
    
    @validator('email')
    def validate_email(cls, value):
        if not value or '@' not in value:
            raise HttpError(status_code = 400, message = "L'email fourni n'est pas valide.")
        return value
    
class EntrepriseCreateSchema(BaseModel):
    nom: str
    email: str
    password:str
    pays: str
    ville: str
    secteur_activite:str
    
    @validator('password')
    def validate_password_length(cls, v):
        if len(v) < 8:
            raise HttpError(status_code=400, message="Le mot de passe doit contenir au moins 8 caractères")
        return v
    
    @validator('email')
    def validate_email(cls, value):
        if not value or '@' not in value:
            raise HttpError(status_code = 400, message = "L'email fourni n'est pas valide.")
        return value
    
class JustificationCompetanceSchema(BaseModel):
    type: str
    nom_document: str
    lien: str = None
    
class LienExterneSchema(BaseModel):
    url: str