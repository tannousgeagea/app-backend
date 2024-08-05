import os
import math
import uuid
import time
import django
import shutil
django.setup()
from datetime import datetime, timedelta
from datetime import date, timezone
from typing import Callable
from fastapi import Request
from fastapi import Response
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from fastapi import status
from fastapi import File, UploadFile
from pathlib import Path
from django.conf import settings

from database.models import ProjectType, Project, Image, ImageMode

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler


router = APIRouter(
    prefix="/api/v1",
    tags=["Images"],
    route_class=TimedRoute,
    responses={404: {"description": "Not found"}},
)

@router.api_route(
    "/images/metadata", methods=["GET"], tags=["Images"]
)
def get_images_metadata(response: Response):
    results = {}
    try:
        
        image_meta = Image._meta.get_fields()
        results = {
            'metadata': {
                'columns': [i.name for i in image_meta]
            }
        }
        
        return results
    
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    
@router.api_route(
    "/images/{project_name}", methods=["POST"], tags=["Images"]
)
def upload_images(response: Response, project_name:str, files: list[UploadFile] = File(...)):
    results = {}
    try:
        if not files:
            results['error'] = {
                'status_code': 'bad-request',
                'status_description': f'No files included in the request',
                'details': f'No files included in the request',
            }
            
            response.status_code = status.HTTP_400_BAD_REQUEST
            return results
        
        if not Project.objects.filter(project_name=project_name).exists():
            results['error'] = {
                'status_code': "non-matching-query",
                'status_description': f'Prject name {project_name} was not found',
                'detail': f"Project {project_name} does not exist."
            }

            response.status_code = status.HTTP_404_NOT_FOUND
            return results
            
        saved_images = []
        for file in files:
            
            if Image.objects.filter(image_name=file.filename).exists():
                continue
            
            project = Project.objects.get(project_name=project_name)
            image = Image()
            image.project = project
            image.image_name = file.filename
            image.image_file = 'images/' + file.filename
            image.image_id = str(uuid.uuid4())
            image.mode = ImageMode.objects.get(mode='train')
            
            file_path = Path('images/' + file.filename)
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        
            saved_images.append(file.filename)
            image.save()
        
        results = {
            'status_code': 'ok',
            'status_description': f'{len(saved_images)} uploaded successfully',
            'detail': f'{len(saved_images)} uploaded successfully!',
        }
        
    except HTTPException as e:
        results['error'] = {
            "status_code": "not found",
            "status_description": "Request not Found",
            "detail": f"{e}",
        }
        
        response.status_code = status.HTTP_404_NOT_FOUND
    
    except Exception as e:
        results['error'] = {
            'status_code': 'server-error',
            "status_description": f"Internal Server Error",
            "detail": str(e),
        }
        
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    return results

