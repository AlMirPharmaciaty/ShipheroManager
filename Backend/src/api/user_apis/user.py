from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.controllers.user_controllers.auth import AuthController
from src.models.user_models.user import User
from src.schemas.custom_response import CustomResponse, UserResponseModel
from src.schemas.user_schemas.user import UserUpdate
from src.controllers.user_controllers.user import UserController

user = APIRouter()
auth = AuthController()


@user.get("/", response_model=UserResponseModel)
def get_user(db: Session = Depends(get_db),
             current_user: User = Depends(auth.get_current_user)):
    """API for user to get their details"""
    try:
        controller = UserController(db=db)
        user = controller.get_user(user_id=current_user.id)
        if not user:
            raise Exception('User not found.')
        response = CustomResponse()
        response.data = user
        response.success = True
        return response

    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f'Failed to get user - {str(e)}') from e


@user.put("/", response_model=UserResponseModel)
def update_user(new_details: UserUpdate,
                db: Session = Depends(get_db),
                current_user: User = Depends(auth.get_current_user)):
    """API for user to update their details"""
    try:
        controller = UserController(db=db)
        response = CustomResponse()
        response.data = controller.update(current_user.id, new_details)
        response.success = True
        response.message = 'User updated successfully'
        return response

    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f'Failed to update user - {str(e)}') from e


@user.delete("/", response_model=UserResponseModel)
def delete_user(db: Session = Depends(get_db),
                current_user: User = Depends(auth.get_current_user)):
    """API for user to delete their account"""
    try:
        controller = UserController(db=db)
        response = CustomResponse()
        response.data = controller.delete(current_user.id)
        response.success = True
        response.message = 'User updated successfully'
        return response

    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f'Failed to delete user - {str(e)}') from e
