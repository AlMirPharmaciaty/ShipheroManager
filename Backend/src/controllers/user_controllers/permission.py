from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_

from src.models.user_models.permission import Permission
from src.models.user_models.role import Role
from src.schemas.custom_response import Pagination
from src.schemas.user_schemas.permission import PermissionCreate, PermissionUpdate


class PermissionController:
    """Handle database operations for the permissions tables"""

    def __init__(self, db: Session):
        self.db = db

    def read(self, permission_id: int):
        return self.db.query(Permission).filter(Permission.id == permission_id).first()

    def is_permission_duplicate(self,
                                permission_name: str,
                                permission_id: int | None = None):
        permission = self.db.query(Permission).filter(
            Permission.name == permission_name)
        if permission_id:
            permission = permission.filter(Permission.id != permission_id)
        permission = permission.first()
        if permission:
            return True
        return False

    def read_many(
        self,
        query: str = None,
        roles: str = None,
        perms: str = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        page: int = 1,
        limit: int = 10,
    ):
        """Get all or filtered permission(s)"""
        try:
            data = self.db.query(Permission)
            pagination = Pagination()
            pagination.total = data.count()
            if query:
                data = data.filter(or_(
                    func.lower(Permission.name).contains(query.lower()),
                    func.lower(Permission.id).contains(query.lower())))
            if roles:
                roles = roles.split(',')
                data = data.filter(and_(*[or_(
                    Permission.roles.any(Role.name == value),
                    Permission.roles.any(Role.id == value))
                    for value in roles]
                ))
            if perms:
                perms = perms.split(',')
                data = data.filter(or_(Permission.name.in_(perms),
                                       Permission.id.in_(perms)))
            sort_field = getattr(Permission, sort_by)
            data = data.order_by(
                sort_field.asc() if sort_order == "asc" else sort_field.desc())
            pagination.filtered = data.count()
            data = data.offset((page - 1) * limit).limit(limit).all()
            return data, pagination

        except Exception as e:
            raise Exception(str(e)) from e

    def create(self, permission: PermissionCreate):
        """Create a new permission"""
        try:
            if self.is_permission_duplicate(permission_name=permission.name):
                raise Exception('Permission already exists.')
            permission = Permission(**permission.model_dump())
            self.db.add(permission)
            self.db.commit()
            self.db.refresh(permission)
            return permission

        except Exception as e:
            self.db.rollback()
            raise Exception(str(e)) from e

    def update(self,
               permission_id: int,
               new_details: PermissionUpdate):
        """Update a permission details"""
        try:
            permission = self.read(permission_id=permission_id)
            if not permission:
                raise Exception('Permission not found.')

            if self.is_permission_duplicate(permission_name=new_details.name,
                                            permission_id=permission.id):
                raise Exception('Permission already exists.')

            permission.name = new_details.name
            self.db.commit()
            self.db.refresh(permission)
            return permission

        except Exception as e:
            self.db.rollback()
            raise Exception(str(e)) from e

    def delete(self, permission_id: int):
        """Permanently delete a permission"""
        try:
            permission = self.read(permission_id=permission_id)
            if not permission:
                raise Exception('Permission not found.')

            self.db.delete(permission)
            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            raise Exception(str(e)) from e
