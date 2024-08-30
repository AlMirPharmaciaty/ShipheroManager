from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from fastapi.encoders import jsonable_encoder

from src.utils.encryption import encrypt
from src.utils.id_generator import generate_id
from src.models.user_models.user import User
from src.models.user_models.role import Role
from src.models.user_models.user_role import UserRole
from src.schemas.custom_response import Pagination
from src.schemas.user_schemas.user import UserCreate, UserUpdateAdmin


class UserController:
    """Handle user database operations"""

    def __init__(self, db: Session):
        self.db = db

    def get_user(self,
                 user_id: str = None,
                 email: str = None,
                 exclude_deleted: bool = True):
        """Get a single user"""
        user = self.db.query(User)
        if exclude_deleted:
            user = user.filter(User.deleted == False)
        if user_id:
            user = user.filter(User.id == user_id)
        if email:
            user = user.filter(User.email == email)
        return user.first()

    def is_email_duplicate(self, email: str, user_id: str | None = None):
        """Check whether email already exists"""
        user = self.db.query(User).filter(User.email == email)
        if user_id:
            user = user.filter(User.id != user_id)
        user = user.first()
        if user:
            return True
        return False

    def get_users(
        self,
        query: str = None,
        exclude_deleted: bool = True,
        roles: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        page: int = 1,
        limit: int = 10,
    ):
        """Get all or filtered user(s)"""
        try:
            users = self.db.query(User)
            pagination = Pagination()
            pagination.total = users.count()
            if exclude_deleted:
                users = users.filter(User.deleted == False)
            if query:
                users = users.filter(or_(
                    func.lower(User.username).contains(query.lower()),
                    func.lower(User.id).contains(query.lower()),
                    func.lower(User.email).contains(query.lower())))
            if roles:
                roles = roles.split(',')
                users = users.filter(and_(*[or_(
                    User.roles.any(Role.name == value),
                    User.roles.any(Role.id == value))
                    for value in roles]
                ))
            sort_field = getattr(User, sort_by)
            users = users.order_by(
                sort_field.asc() if sort_order == "asc" else sort_field.desc())
            pagination.filtered = users.count()
            users = users.offset((page - 1) * limit).limit(limit).all()
            return users, pagination

        except Exception as e:
            raise Exception(str(e)) from e

    def create(self, user: UserCreate):
        """Create a new user"""
        try:
            if self.is_email_duplicate(email=user.email):
                raise Exception('Email already exists.')
            user = User(**user.model_dump())
            user.id = generate_id(db=self.db, prefix="uu", model=User)
            user.password = encrypt(user.password)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise Exception(str(e)) from e

    def update(self, user_id: str, new_details: UserUpdateAdmin):
        """Update a user details"""
        try:
            exclude_deleted = True
            if 'deleted' in jsonable_encoder(new_details):
                exclude_deleted = False
            user = self.get_user(user_id=user_id,
                                 exclude_deleted=exclude_deleted)
            if not user:
                raise Exception("User not found")

            if 'deleted' in jsonable_encoder(new_details):
                user.deleted = new_details.deleted

            # Update avatar
            if new_details.avatar:
                user.avatar = new_details.avatar

            # Update username
            if new_details.username:
                user.username = new_details.username

            # Update email
            if new_details.email:
                # Check if email already exists
                if self.is_email_duplicate(email=new_details.email,
                                           user_id=user.id):
                    raise Exception('Email already exists.')
                user.email = new_details.email

            # Update password
            if new_details.password:
                if user.password != new_details.password:
                    # Encrypt new password
                    user.password = encrypt(new_details.password)

            # Update user roles
            if 'roles' in jsonable_encoder(new_details):
                # Remove all existing user roles
                user_roles = self.db.query(UserRole).filter(
                    UserRole.user_id == user.id).all()
                for role in user_roles:
                    self.db.delete(role)

                # Add new roles
                if new_details.roles:
                    for role_id in new_details.roles:
                        role = self.db.query(Role).filter(
                            Role.id == role_id).first()
                        if not role:
                            raise Exception(
                                f"Role with id '{role_id}' not found.")
                        user_role = UserRole(user_id=user.id,
                                             role_id=role.id)
                        self.db.add(user_role)

            self.db.commit()
            self.db.refresh(user)
            return user

        except Exception as e:
            self.db.rollback()
            raise Exception(str(e)) from e

    def delete(self, user_id: str):
        """Soft delete a user"""
        try:
            user = self.get_user(user_id=user_id)
            if not user:
                raise Exception("User doesn't exist or is already deleted.")

            user.deleted = True
            self.db.commit()
            self.db.refresh(user)
            return user

        except Exception as e:
            self.db.rollback()
            raise Exception(str(e)) from e
