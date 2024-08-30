from fastapi import APIRouter, Depends

from src.controllers.user_controllers.auth import AuthController
from src.utils.avatar_picker import get_avatars_list

auth_controller = AuthController()
avatar = APIRouter(dependencies=[Depends(auth_controller.get_current_user)])


@avatar.get('/')
def get_avatars():
    return get_avatars_list()
