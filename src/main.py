from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.api.routes.upload_documents import documents_router
from src.api.routes.ask_question import question_router


def create_app() -> FastAPI:
  """
  Main function to initialize the FastAPI application.
  
  Returns:
    FastAPI: An instance of the FastAPI application.
  """

  app = FastAPI()
  
  # Mount static files and templates
  app.mount("/frontend", StaticFiles(directory="src/frontend"), name="frontend")
  templates = Jinja2Templates(directory="src/frontend")

  # Define the root route
  @app.get("/", response_class=HTMLResponse)
  async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

  # Include the documents and qa router
  app.include_router(documents_router)
  app.include_router(question_router)
  
  return app

app = create_app()
