from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.controllers.user_controllers.auth import Authorize
from src.schemas.custom_response import CustomResponse, UserResponseModel
from src.schemas.user_schemas.user import UserUpdateAdmin
from src.controllers.user_controllers.user import UserController

user_manager = APIRouter()


@user_manager.get("/all", response_model=UserResponseModel)
def get_all_users(query: str = None,
                  exclude_deleted: bool = True,
                  roles: str | None = None,
                  sort_by: str = "created_at",
                  sort_order: str = "desc",
                  page: int = Query(1, ge=1),
                  limit: int = Query(10, ge=1, le=100),
                  db: Session = Depends(get_db),
                  _=Depends(Authorize(permission="user_read"))):
    try:
        controller = UserController(db=db)
        response = CustomResponse()
        response.data, response.pagination = controller.read_many(
            query=query,
            page=page,
            limit=limit,
            exclude_deleted=exclude_deleted,
            roles=roles,
            sort_by=sort_by,
            sort_order=sort_order
        )
        response.success = True
        return response

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Failed to retrieve user(s) - {str(e)}.') from e


@user_manager.get("/", response_model=UserResponseModel)
def get_user(user_id: int,
             db: Session = Depends(get_db),
             _=Depends(Authorize(permission="user_read"))):
    try:
        controller = UserController(db=db)
        user = controller.read(user_id=user_id, exclude_deleted=False)
        response = CustomResponse()
        response.data = user
        response.success = True
        if not user:
            response.message = "User not found."
        return response

    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f'Failed to get user - {str(e)}.') from e


@user_manager.put("/", response_model=UserResponseModel)
def update_user(user_id: int,
                new_details: UserUpdateAdmin,
                db: Session = Depends(get_db),
                _=Depends(Authorize(permission="user_update"))):
    try:
        controller = UserController(db=db)
        response = CustomResponse()
        response.data = controller.update(user_id, new_details)
        response.success = True
        response.message = 'User updated successfully'
        return response

    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f'Failed to update user - {str(e)}') from e


@user_manager.delete("/", response_model=UserResponseModel)
def delete_user(user_id: int,
                db: Session = Depends(get_db),
                _=Depends(Authorize(permission="user_delete"))):
    try:
        controller = UserController(db=db)
        response = CustomResponse()
        response.data = controller.delete(user_id)
        response.success = True
        response.message = 'User deleted successfully'
        return response

    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f'Failed to delete user - {str(e)}') from e
