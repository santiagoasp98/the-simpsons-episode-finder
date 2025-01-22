from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from finder import EpisodeFinder

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize the finder
MODEL_PATH = "models/sentence_transformer_model"
DATA_PATH = "models/finder_data.pkl"
finder = EpisodeFinder(MODEL_PATH, DATA_PATH)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/find_episode")
async def find_episode(description: str):
    results = finder.find_episode(description)
    return JSONResponse(content={"results": results})
