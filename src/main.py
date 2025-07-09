from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.api.upload_documents import router as documents_router


def create_app() -> FastAPI:
  """Função principal para iniciar o aplicativo FastAPI com a rota '/'."""
  
  app = FastAPI()
  
  # Monta a pasta única com HTML e CSS
  app.mount("/frontend", StaticFiles(directory="src/frontend"), name="frontend")

  # Usa a mesma pasta para os templates
  templates = Jinja2Templates(directory="src/frontend")

  # Rota da página inicial
  @app.get("/", response_class=HTMLResponse)
  async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

  app.include_router(documents_router)
  
  return app

app = create_app()
