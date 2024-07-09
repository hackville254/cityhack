from ninja import Router,Form
from ninja.files import UploadedFile
from ninja.errors import HttpError
from .models import *
from core.models import *
from .schemas import *
from core.token import *
from typing import List
router = Router()

@router.post('/competences/')
def create_competence(request, competence: Form[CompetenceSchema], fichier: UploadedFile = None):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = verify_token(token)
        user_id = payload.get('user_id')
        user = User.objects.get(id=user_id)
        client = Client.objects.get(user=user)

        new_competence = Competence(
            client=client,
            type_document=competence.type_document,
            nom_document=competence.nom_document,
            fichier_document=fichier,
            lien_document=competence.lien_document,
        )
        new_competence.save()
        
        return new_competence
    
    except:
        raise HttpError(404, "Client non trouvé")

@router.get('/competences/')
def read_competences(request):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = verify_token(token)
        user_id = payload.get('user_id')
        user = User.objects.get(id=user_id)
        client = Client.objects.get(user=user)

        competences = Competence.objects.filter(client=client)
        return competences
    
    except:
        raise HttpError(404, "Aucune compétence trouvée pour ce client")

@router.post('/competences/{competence_id}/')
def update_competence(request, competence_id: int, competence: Form[CompetenceSchema]):
    try:
        competence_to_update = Competence.objects.get(id=competence_id)
        competence_to_update.type_document = competence.type_document
        competence_to_update.nom_document = competence.nom_document
        competence_to_update.lien_document = competence.lien_document
        competence_to_update.save()

        return 200
    
    except:
        raise HttpError(404, "Compétence non trouvée")

@router.delete('/competences/{competence_id}/')
def delete_competence(request, competence_id: int):
    try:
        competence = Competence.objects.get(id=competence_id)
        competence.delete()

        return {"message": "Compétence supprimée avec succès"}
    
    except:
        raise HttpError(404, "Compétence non trouvée")

##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
realisation = Router() 

@realisation.post('/realisations/')
def create_realisation(request, realisation: Form[RealisationSchema], fichier: Optional[UploadedFile] = None):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = verify_token(token)
        user_id = payload.get('user_id')
        user = User.objects.get(id=user_id)
        client = Client.objects.get(user=user)

        new_realisation = Realisation(
            client=client,
            nom=realisation.nom,
            description=realisation.description,
        )
        new_realisation.save()

        if fichier or realisation.lien:
            new_piece_jointe = PieceJointeRealisation(
                realisation=new_realisation,
                fichier=fichier,
                lien=realisation.lien
            )
            new_piece_jointe.save()

        return 200
    
    except Client.DoesNotExist:
        raise HttpError(404, "Client non trouvé")


@realisation.get('/realisations/', response=List[RealisationSchema])
def read_realisations(request):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = verify_token(token)
        user_id = payload.get('user_id')
        user = User.objects.get(id=user_id)
        client = Client.objects.get(user=user)

        realisations = Realisation.objects.filter(client=client)
        return realisations
    
    except Client.DoesNotExist:
        raise HttpError(404, "Client non trouvé")


@realisation.post('/realisations/{realisation_id}/')
def update_realisation(request, realisation_id: int, realisation: Form[RealisationSchema], fichier: Optional[UploadedFile] = None):
    try:
        realisation_to_update = Realisation.objects.get(id=realisation_id)
        realisation_to_update.nom = realisation.nom
        realisation_to_update.description = realisation.description
        realisation_to_update.save()

        piece_jointe_to_update = PieceJointeRealisation.objects.filter(realisation=realisation_to_update).first()
        if piece_jointe_to_update:
            piece_jointe_to_update.fichier = fichier or piece_jointe_to_update.fichier
            piece_jointe_to_update.lien = realisation.lien or piece_jointe_to_update.lien
            piece_jointe_to_update.save()
        else:
            new_piece_jointe = PieceJointeRealisation(
                realisation=realisation_to_update,
                fichier=fichier,
                lien=realisation.lien
            )
            new_piece_jointe.save()

        return 200
    
    except:
        raise HttpError(404, "Réalisation non trouvée")

@realisation.delete('/realisations/{realisation_id}/')
def delete_realisation(request, realisation_id: int):
    try:
        realisation_to_delete = Realisation.objects.get(id=realisation_id)
        realisation_to_delete.delete()

        return {"message": "Réalisation supprimée avec succès"}
    
    except:
        raise HttpError(404, "Réalisation non trouvée")

#################################################
categorie = Router()
@categorie.get("/categories", auth=None)
def get_categories(request):
    categories = Categorie.objects.all()

    # Liste pour stocker les données finales à retourner
    categories_data = []

    for categorie in categories:
        # Récupérer l'URL de l'image
        image_url = request.build_absolute_uri(categorie.image.url)

        # Créer un dictionnaire avec les données requises
        categorie_data = {
            "id":categorie.id,
            "nom": categorie.nom,
            "image_url": image_url,
        }
        categories_data.append(categorie_data)

    return categories_data