from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.custom_response import CustomResponse, RoleResponseModel
from src.schemas.user_schemas.role import RoleCreate, RoleUpdate
from src.controllers.user_controllers.auth import Authorize
from src.controllers.user_controllers.role import RoleController

role_manager = APIRouter()


@role_manager.get("/", response_model=RoleResponseModel)
def get_roles(query: str = None,
              roles: str = None,
              perms: str = None,
              sort_by: str = "created_at",
              sort_order: str = "desc",
              page: int = Query(1, ge=1),
              limit: int = Query(10, ge=1, le=100),
              db: Session = Depends(get_db),
              _=Depends(Authorize(permission="role_read"))):
    try:
        controller = RoleController(db=db)
        response = CustomResponse()
        response.data, response.pagination = controller.get_roles(
            query=query,
            roles=roles,
            perms=perms,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            limit=limit
        )
        response.success = True
        print(response)
        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@role_manager.post("/", response_model=RoleResponseModel)
def create_role(role: RoleCreate,
                db: Session = Depends(get_db),
                _=Depends(Authorize(permission="role_create"))):
    try:
        controller = RoleController(db=db)
        response = CustomResponse()
        response.data = controller.create(new_role=role)
        response.success = True
        response.message = "Role created successfully"
        return response

    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Failed to create role - {str(e)}") from e


@role_manager.put("/", response_model=RoleResponseModel)
def update_role(role_id: str,
                new_details: RoleUpdate,
                db: Session = Depends(get_db),
                _=Depends(Authorize(permission="role_update"))):

    try:
        controller = RoleController(db=db)
        response = CustomResponse()
        response.data = controller.update(role_id, new_details)
        response.success = True
        response.message = "Role updated successfully"
        return response

    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Failed to update role - {str(e)}") from e


@role_manager.delete("/", response_model=RoleResponseModel)
def delete_role(role_id: str,
                db: Session = Depends(get_db),
                _=Depends(Authorize(permission="role_delete"))):
    try:
        controller = RoleController(db=db)
        response = CustomResponse()
        controller.delete(role_id)
        response.success = True
        response.message = "Role deleted successfully"
        return response

    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Failed to delete role - {str(e)}") from e
