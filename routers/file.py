import uuid
from fastapi import APIRouter, File, UploadFile, HTTPException, status
import shutil
from fastapi.responses import FileResponse
import os

# Declare APIRouter instance
router = APIRouter(
    prefix='/files',
    tags=['files']
)

# Function to upload text file
@router.post('/upload', summary='Upload text file', description='Upload text file to server and return lines')
async def upload_text_file(text_file: bytes = File(...)):
    content = text_file.decode('utf-8')
    lines = content.split('\n')
    return {
        'lines': lines
    }

# Function to upload any file
@router.post('/upload-file', summary='Upload file', description='Upload file to server and return it')
async def upload_file(file: UploadFile = File(...)):
    # Create unique filename for each file
    unique_filename = str(uuid.uuid4()) + '_' + file.filename

    # Maximum file size: 3MB
    max_size = 3 * 1024 * 1024

    if file.size > max_size:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='File size is too large')

    path = f'files/{unique_filename}'

    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        'file_name': path,
        'type': file.content_type
    }

# Function to download file
@router.get('/download/{file_name}', summary='Download file', description='Download file from server', response_class=FileResponse)
def download_file(file_name: str):
    path = f'files/{file_name}'
    files_in_folder = ['files/' + f for f in os.listdir('files')]
    is_file_name_exists = path in files_in_folder
    if not is_file_name_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File not found, make sure the file name is correct')
    return path