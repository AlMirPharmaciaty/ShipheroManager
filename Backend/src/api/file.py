from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.controllers.user_controllers.auth import Authorize
from src.controllers.file import FileController
from src.schemas.custom_response import CustomResponse
from src.schemas.file import FileCreate, FileResponseModel
from src.models.file import File
from src.models.user_models.user import User

file = APIRouter()


@file.post("/", response_model=FileResponseModel)
def create_file(data: FileCreate,
                db: Session = Depends(get_db),
                user: User = Depends(Authorize(permission="file_create"))):
    """API to create a new file"""
    try:
        controller = FileController(db=db)
        response = CustomResponse()
        response.data = controller.create(data, user)
        response.success = True
        response.message = "File succesfully saved"
        return response

    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f'Failed to create file - {str(e)}') from e


@file.get("/")
def read_file_content(file_id: int,
                      db: Session = Depends(get_db),
                      _=Depends(Authorize(permission="file_read"))):
    """API to read file content"""
    try:
        controller = FileController(db=db)
        response = CustomResponse()
        response.data = controller.read_content(file_id)
        response.success = True
        return response
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Failed to get file content - {str(e)}') from e


@file.delete('/', response_model=FileResponseModel)
def delete_file(file_id: int,
                db: Session = Depends(get_db),
                _=Depends(Authorize(permission="file_delete"))):
    """API to delete a file by id"""
    try:
        controller = FileController(db=db)
        response = CustomResponse()
        file: File = controller.delete(file_id)
        response.data = file
        if file.deleted:
            response.message = "File deleted successfully!"
        response.success = True
        return response
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f'Failed to delete file - {str(e)}') from e
