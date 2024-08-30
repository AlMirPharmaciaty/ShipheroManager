from fastapi import APIRouter

from src.api.user_apis.auth import auth
from src.api.user_apis.avatar import avatar
from src.api.user_apis.user import user
from src.api.manager.user import user_manager
from src.api.manager.role import role_manager
from src.api.manager.permission import permission_manager

from src.api.etl import etl
from src.api.inventory_snapshot import inventory_snapshot
from src.api.file import file

routes = APIRouter()

routes.include_router(etl, prefix="/etl", tags=['ETL'])
routes.include_router(
    inventory_snapshot, prefix="/inventory-snapshot", tags=['Inventory Snapshot'])
routes.include_router(file, prefix="/file", tags=['File Handler'])

routes.include_router(auth, prefix="/auth", tags=['Auth'])
routes.include_router(user, prefix="/user", tags=['User'])
routes.include_router(user_manager,
                      prefix="/manager/users",
                      tags=['User Manager'])
routes.include_router(role_manager,
                      prefix="/manager/roles",
                      tags=['Role Manager'])
routes.include_router(permission_manager,
                      prefix="/manager/permissions",
                      tags=['Permission Manager'])
routes.include_router(avatar, prefix="/avatar", tags=['Avatar'])

tags_metadata = [
    {
        "name": "ETL",
        "description": "APIs for etl"
    },
    {
        "name": "Inventory Snapshot",
        "description": "APIs to manage Shiphero Inventory Snapshot"
    },
    {
        "name": "File Handler",
        "description": "APIs to handle ETL files"
    },
    {
        "name": "Auth",
        "description": "APIs for user account creation and login"
    },
    {
        "name": "User",
        "description": "APIs for users to manage their account"
    },
    {
        "name": "User Manager",
        "description": "APIs to manage users"
    },
    {
        "name": "Role Manager",
        "description": "APIs to manage roles"
    },
    {
        "name": "Permission Manager",
        "description": "APIs to manage permissions"
    }
]
