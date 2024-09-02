from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_

from src.models.user_models.role import Role
from src.models.user_models.permission import Permission
from src.models.user_models.role_permission import RolePermission
from src.schemas.custom_response import Pagination
from src.schemas.user_schemas.role import RoleCreate, RoleUpdate


class RoleController:
    """Handle database operations for the roles tables"""

    def __init__(self, db: Session):
        self.db = db

    def read(self, role_id: int):
        return self.db.query(Role).filter(Role.id == role_id).first()

    def is_role_duplicate(self, role_name: str, role_id: int | None = None):
        role = self.db.query(Role).filter(Role.name == role_name)
        if role_id:
            role = role.filter(Role.id != role_id)
        role = role.first()
        if role:
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
        """Get all or filtered role(s)"""
        try:
            data = self.db.query(Role)
            pagination = Pagination()
            pagination.total = data.count()
            if query:
                data = data.filter(or_(
                    func.lower(Role.name).contains(query.lower()),
                    func.lower(Role.id).contains(query.lower())))
            if roles:
                roles = roles.split(',')
                data = data.filter(or_(Role.name.in_(roles),
                                       Role.id.in_(roles)))
            if perms:
                perms = perms.split(',')
                data = data.filter(and_(*[or_(
                    Role.permissions.any(Permission.name == value),
                    Role.permissions.any(Permission.id == value))
                    for value in perms]
                ))
            sort_field = getattr(Role, sort_by)
            data = data.order_by(
                sort_field.asc() if sort_order == "asc" else sort_field.desc())
            pagination.filtered = data.count()
            data = data.offset((page - 1) * limit).limit(limit).all()
            return data, pagination

        except Exception as e:
            raise Exception(str(e)) from e

    def update_role_permissions(self, role: Role, new_details):
        # Update role permissions
        if 'permissions' in jsonable_encoder(new_details):
            # Remove all existing role permissions
            role_perms = self.db.query(RolePermission).filter(
                RolePermission.role_id == role.id).all()
            for perm in role_perms:
                self.db.delete(perm)

            # Add new permissions
            if new_details.permissions:
                for perm_id in new_details.permissions:
                    perm = self.db.query(Permission).filter(
                        Permission.id == perm_id).first()
                    if not perm:
                        raise Exception(
                            f"Permission with id '{perm_id}' not found.")
                    role_perm = RolePermission(permission_id=perm.id,
                                               role_id=role.id)
                    self.db.add(role_perm)

    def create(self, new_role: RoleCreate):
        """Create a new role"""
        try:
            if self.is_role_duplicate(role_name=new_role.name):
                raise Exception('Role already exists.')
            role = Role()
            role.name = new_role.name
            self.db.add(role)
            self.db.flush()
            self.update_role_permissions(role=role, new_details=new_role)
            self.db.commit()
            self.db.refresh(role)
            return role

        except Exception as e:
            self.db.rollback()
            raise Exception(str(e)) from e

    def update(self, role_id: int, new_details: RoleUpdate):
        """Update a role details"""
        try:
            role = self.read(role_id=role_id)
            if not role:
                raise Exception('Role not found.')

            if self.is_role_duplicate(role_name=new_details.name,
                                      role_id=role.id):
                raise Exception('Role already exists.')

            role.name = new_details.name
            self.update_role_permissions(role=role, new_details=new_details)
            self.db.commit()
            self.db.refresh(role)
            return role

        except Exception as e:
            self.db.rollback()
            raise Exception(str(e)) from e

    def delete(self, role_id: int):
        """Permanently delete a role"""
        try:
            role = self.read(role_id=role_id)
            if not role:
                raise Exception('Role not found.')

            self.db.delete(role)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(str(e)) from e
