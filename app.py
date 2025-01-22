# ------------------------------------------------- #
# Imports
# ------------------------------------------------- #

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from finder import EpisodeFinder

# ------------------------------------------------- #
# Constants
# ------------------------------------------------- #

# Initialize the finder
MODEL_PATH = 'models/sentence_transformer_model'
DATA_PATH = 'models/finder_data.pkl'
finder = EpisodeFinder(MODEL_PATH, DATA_PATH)

# ------------------------------------------------- #
# FastAPI Application Setup
# ------------------------------------------------- #

app = FastAPI(
    title='Simpsons Episode Finder',
    description='A web application to find Simpsons episodes based on a description.',
    version='1.0.0')

# Mount static files
app.mount('/static',
          StaticFiles(directory='static'), 
          name='static')

# Templates
templates = Jinja2Templates(directory='templates')

# ------------------------------------------------- #
# API Endpoints
# ------------------------------------------------- #

@app.get('/')
async def home(request: Request):
    '''
    Renders the home page.

    Args:
        request (Request): The request object.
    
    Returns:
        TemplateResponse: The rendered home page template.
    '''
    return templates.TemplateResponse('index.html', 
                                      {'request': request})

@app.post('/find_episode')
async def find_episode(description: str):
    '''
    Finds episodes based on the provided description

    Args:
        description (str): The description of the episode.
    
    Returns:
        JSONResponse: A JSON response containing the
        search results.
    '''
    results = finder.find_episode(description)
    return JSONResponse(content={'results': results})
