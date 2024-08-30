from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.custom_response import CustomResponse, PermissionResponseModel
from src.schemas.user_schemas.permission import PermissionCreate, PermissionUpdate
from src.controllers.user_controllers.auth import Authorize
from src.controllers.user_controllers.permission import PermissionController

permission_manager = APIRouter()


@permission_manager.get("/", response_model=PermissionResponseModel)
def get_permissions(query: str = None,
                    roles: str = None,
                    perms: str = None,
                    sort_by: str = "created_at",
                    sort_order: str = "desc",
                    page: int = Query(1, ge=1),
                    limit: int = Query(10, ge=1, le=100),
                    db: Session = Depends(get_db),
                    _=Depends(Authorize(permission="permission_read"))):
    try:
        controller = PermissionController(db=db)
        data, pagination = controller.get_permissions(
            query=query,
            roles=roles,
            perms=perms,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            limit=limit,
        )
        return CustomResponse(success=True, data=data, pagination=pagination)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@permission_manager.post("/", response_model=PermissionResponseModel)
def create_permission(permission: PermissionCreate,
                      db: Session = Depends(get_db),
                      _=Depends(Authorize(permission="permission_create"))):
    try:
        controller = PermissionController(db=db)
        response = CustomResponse()
        response.data = controller.create(permission)
        response.success = True
        response.message = "Permission created successfully"
        return response

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create permission - {str(e)}") from e


@permission_manager.put("/", response_model=PermissionResponseModel)
def update_permission(permission_id: str,
                      new_details: PermissionUpdate,
                      db: Session = Depends(get_db),
                      _=Depends(Authorize(permission="permission_update"))):

    try:
        controller = PermissionController(db=db)
        response = CustomResponse()
        response.data = controller.update(permission_id, new_details)
        response.success = True
        response.message = "Permission updated successfully"
        return response

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to update permission - {str(e)}") from e


@permission_manager.delete("/", response_model=PermissionResponseModel)
def delete_permission(permission_id: str,
                      db: Session = Depends(get_db),
                      _=Depends(Authorize(permission="permission_delete"))):
    try:
        controller = PermissionController(db=db)
        response = CustomResponse()
        controller.delete(permission_id)
        response.success = True
        response.message = "Permission deleted successfully"
        return response

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to delete permission - {str(e)}") from e
