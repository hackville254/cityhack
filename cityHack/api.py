from core.token import verify_token
from ninja import NinjaAPI
from ninja.security import HttpBearer
from core.routers import router as AuthRouter
from folio.routers import router as FolioRouter
from folio.routers import realisation as RealisationRouter
from folio.routers import categorie as CategorieRouter
class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        t = verify_token(token=token)
        return t
    
app = NinjaAPI(
    title='city hack',
    version="1.0.0",
    auth=GlobalAuth(),
)

app.add_router("authenticate/",AuthRouter,tags=["Authentification"])
app.add_router("folio/",FolioRouter,tags=["Folio (JUSTIFICATION COMPETANCE)"])
app.add_router("realisation/",RealisationRouter,tags=["COMPETANCE"])
app.add_router("categorie/",CategorieRouter,tags=["CATEGORIE"])
