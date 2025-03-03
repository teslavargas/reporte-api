from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .scraping import scrape_full
from .normalization import normalize_full_episode

app = FastAPI(
    title="Reporte Minoritario API",
    description="Esta API permite obtener datos normalizados del Reporte Minoritario.",
    version="1.0.0",
    docs_url="/docs",    # Swagger UI
    redoc_url="/redoc"   # ReDoc
)

# Configuración de CORS para permitir cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montamos la carpeta de archivos estáticos (por ejemplo, para CSS o imágenes)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Página principal personalizada con UI mejorada
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint principal que expone los datos normalizados de un episodio
@app.get("/episode/{episode}")
def get_full_normalized_episode(episode: int):
    full_data = scrape_full(episode)
    normalized = normalize_full_episode(full_data)
    return normalized

# Ejecutar solo si el script se ejecuta directamente
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
