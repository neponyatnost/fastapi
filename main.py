from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers import blog_get, blog_post, user, article, product, file
from auth import authentication
from db import models
from db.database import engine
from exceptions import StoryException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={
            'detail': exc.name
        }
    )


models.Base.metadata.create_all(bind=engine)


origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

app.mount('/files', StaticFiles(directory='files'), name='files')