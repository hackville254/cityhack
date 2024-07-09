from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from ninja.errors import HttpError



class CompetenceSchema(BaseModel):
    type_document: str
    nom_document: str
    lien_document: str = None
    

class RealisationSchema(BaseModel):
    nom: str
    description: str
    lien:str