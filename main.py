from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from auth import authentication
from routers import blog_get, blog_post, user, article, product, file
from db import models
from db.database import engine
from exceptions import StoryException
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI instance
app = FastAPI(
    title='Test API'
)

# Include routers in FastAPI instance
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)

# Function to get index page
@app.get('/', tags=['index'], summary='Index page', description='This is the index page')
async def index():
    return 'Index page'

# Exception handler for StoryException class
@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={
            'detail': exc.name
        }
    )

# Create tables in database
models.Base.metadata.create_all(bind=engine)

# Define origins for CORS
origins = [
    'http://localhost:3000',
]

# Add CORS middleware to FastAPI instance
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

app.mount('/files', StaticFiles(directory='files'), name='files')