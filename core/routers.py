from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from ninja import Router,Form
from ninja.files import UploadedFile
from ninja.errors import HttpError
from pydantic import BaseModel
from .models import *
from .schemas import *
from .token import *
from django.shortcuts import get_object_or_404

router = Router()

@router.post("/register-utilisateur", response={201: str, 400: str}, auth=None)
def register_client(request, payload: UserCreateSchema):
    if User.objects.filter(email=payload.email).exists():
        return 400, "L'email est déjà utilisé"

    user = User.objects.create(
        username=payload.email,
        first_name=payload.nom,
        last_name=payload.prenom,
        password=make_password(payload.password),
        email=payload.email
    )
    client = Client.objects.create(
        user=user,
        pays=payload.pays,
        ville=payload.ville,
        categorie = payload.categorie
    )
    Wallet.objects.create(client = client)
    return 201, "Client créé avec succès"


@router.post("/register-entreprise", response={201: str, 400: str}, auth=None)
def register_travailleur(request, payload: EntrepriseCreateSchema):
    if User.objects.filter(email=payload.email).exists():
        return 400, "L'email est déjà utilisé"

    user = User.objects.create(
        username=payload.email,
        first_name=payload.nom,
        password=make_password(payload.password),
        email=payload.email
    )
    entreprise = Entreprise.objects.create(
        user=user,
        pays=payload.pays,
        ville=payload.ville,
        secteur_activite=payload.secteur_activite
    )
    return 201, "Entreprise créé avec succès"


@router.post("/login", auth=None)
def login(request, payload: LoginSchema):
    try:
        user = get_object_or_404(User, username=payload.email)
        print(user)
        t = user.check_password(payload.password)
        print(t)
        if not t:
            raise HttpError(401, "Mot de passe incorrect")
        
        # Générer un token d'authentification pour l'utilisateur  
        token = create_token(user.id)
        
        # Vérifier si l'utilisateur est un client ou une entreprise
        is_client = Client.objects.filter(user=user).exists()
        is_entreprise = Entreprise.objects.filter(user=user).exists()

        return 200, {"token": token, "is_client": is_client, "is_entreprise": is_entreprise}
    
    except User.DoesNotExist:
        raise HttpError(401, "Email incorrect")
    except Exception as e:
        raise HttpError(500, str(e))



@router.get('get-user/')
def getUser(request):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = verify_token(token)
        user_id = payload.get('user_id')
        user = User.objects.get(id = user_id)
        client = Client.objects.get(user = user)
        # Construire la réponse JSON
        response_data = {
            "user": {
                "id": user.id,
                "username": user.username,
                "first_name":user.first_name,
                "last_name":user.last_name,
                "last_login":user.last_login
            },
            "client": {
                "id": client.id,
                "pays":client.pays,
                "ville":client.ville,
                "categorie":client.categorie,
                "date_creation":client.date_creation
            }
        }
        
        return response_data

    except:
        raise HttpError(status_code=404, message="veillez vous connectez svp")


@router.get('get-entreprise/')
def getEntreprise(request):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = verify_token(token)
        user_id = payload.get('user_id')
        user = User.objects.get(id = user_id)
        entreprise = Entreprise.objects.get(user = user)
        # Construire la réponse JSON
        response_data = {
            "user": {
                "id": user.id,
                "username": user.username,
                "first_name":user.first_name,
                "last_name":user.last_name,
                "last_login":user.last_login
            },
            "entreprise": {
                "id": entreprise.id,
                "pays":entreprise.pays,
                "ville":entreprise.ville,
                "secteur_activite":entreprise.secteur_activite,
                "date_creation":entreprise.date_creation
            }
        }
        
        return response_data

    except:
        raise HttpError(status_code=404, message="veillez vous connectez svp")
    
    
###############JUSTIFICATION COMPETANCE

""" @router.post('/justifications/')
def create_justification(request, justification: Form[JustificationCompetanceSchema],fichier: UploadedFile = None):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = verify_token(token)
        user_id = payload.get('user_id')
        user = User.objects.get(id = user_id)
        client = Client.objects.get(user=user)
        new_justification = JustificationCompetance(
            client=client,
            type=justification.type,
            nom_document=justification.nom_document,
            fichier=fichier,
            lien=justification.lien,
        )
        new_justification.save()
        return new_justification
        
    except Client.DoesNotExist:
        raise HttpError(404, "Client non trouvé")

@router.get('/justifications/{justification_id}/')
def read_justification(request, justification_id: int):
    try:
        justification = JustificationCompetance.objects.get(id=justification_id)
        return justification
        
    except:
        raise HttpError(404, "Justification non trouvée")

@router.post('/justifications/{justification_id}/')
def update_justification(request, justification_id: int, justification: Form[JustificationCompetanceSchema],fichier: UploadedFile = None):
    try:
        justification_to_update = JustificationCompetance.objects.get(id=justification_id)
        justification_to_update.type = justification.type
        justification_to_update.nom_document = justification.nom_document
        justification_to_update.fichier = justification.fichier
        justification_to_update.lien = justification.lien
        justification_to_update.date_modification = datetime.now()
        justification_to_update.save()
        return justification_to_update
        
    except:
        raise HttpError(404, "justification non trouvée")

@router.delete('/justifications/{justification_id}/')
def delete_justification(request, justification_id: int):
    try:
        justification = JustificationCompetance.objects.get(id=justification_id)
        justification.delete()
        return {"message": "Justification supprimée avec succès"}
        
    except JustificationCompetance.DoesNotExist:
        raise HttpError(404, "Justification non trouvée")
 """

######## Lien externe
@router.post('/liens-externes/')
def create_lien_externe(request, lien: LienExterneSchema):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = verify_token(token)
        user_id = payload.get('user_id')
        user = User.objects.get(id = user_id)
        client = Client.objects.get(user=user)
        new_lien = LienExterne(
            client=client,
            url=lien.url,
        )
        new_lien.save()
        return 200
        
    except Client.DoesNotExist:
        raise HttpError(404, "Client non trouvé")

@router.get('/liens-externes/')
def read_lien_externe(request):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = verify_token(token)
        user_id = payload.get('user_id')
        user = User.objects.get(id = user_id)
        client = Client.objects.get(user=user)
        liens = LienExterne.objects.filter(client=client).values()
        return list(liens)
        
    except LienExterne.DoesNotExist:
        raise HttpError(404, "Lien externe non trouvé")

@router.post('/liens-externes/{lien_id}/')
def update_lien_externe(request, lien_id: int, lien: LienExterneSchema):
    try:
        lien_to_update = LienExterne.objects.get(id=lien_id)
        lien_to_update.url = lien.url
        lien_to_update.save()
        return lien_to_update
        
    except (LienExterne.DoesNotExist):
        raise HttpError(404, "Lien externe non trouvé")

@router.delete('/liens-externes/{lien_id}/')
def delete_lien_externe(request, lien_id: int):
    try:
        lien = LienExterne.objects.get(id=lien_id)
        lien.delete()
        return {"message": "Lien externe supprimé avec succès"}
        
    except LienExterne.DoesNotExist:
        raise HttpError(404, "Lien externe non trouvé")
