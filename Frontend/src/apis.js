const BASE_URL = 'http://127.0.0.1:8000'
export const manager = {
  userManager: {
    url: BASE_URL + '/manager/users',
    permission: 'user_read'
  },
  roleManager: {
    url: BASE_URL + '/manager/roles',
    permission: 'role_read'
  },
  permissionManager: {
    url: BASE_URL + '/manager/permissions',
    permission: 'permission_read'
  }
}

export const APIs = {
  baseURL: BASE_URL,
  userAvatarURL: BASE_URL + '/static/avatars',
  avatarGet: {
    url: BASE_URL + '/avatar',
    method: 'GET'
  },
  login: {
    url: BASE_URL + '/auth/login',
    method: 'POST'
  },
  register: {
    url: BASE_URL + '/auth/register',
    method: 'POST'
  },
  accountUpdate: {
    url: BASE_URL + '/user',
    method: 'PUT'
  },
  accountDelete: {
    url: BASE_URL + '/user',
    method: 'DELETE'
  },
  userList: {
    url: manager.userManager.url + '/all',
    method: 'GET',
    permission: manager.userManager.permission
  },
  userGet: {
    url: manager.userManager.url,
    method: 'GET',
    permission: manager.userManager.permission
  },
  userEdit: {
    url: manager.userManager.url,
    method: 'PUT',
    permission: 'user_update'
  },
  userDelete: {
    url: manager.userManager.url,
    method: 'DELETE',
    permission: 'user_delete'
  },
  roleList: {
    url: manager.roleManager.url,
    method: 'GET',
    permission: manager.roleManager.permission
  },
  roleCreate: {
    url: manager.roleManager.url,
    method: 'POST',
    permission: 'role_create'
  },
  roleEdit: {
    url: manager.roleManager.url,
    method: 'PUT',
    permission: 'role_update'
  },
  roleDelete: {
    url: manager.roleManager.url,
    method: 'DELETE',
    permission: 'role_delete'
  },
  permissionList: {
    url: manager.permissionManager.url,
    method: 'GET',
    permission: manager.permissionManager.permission
  },
  permissionCreate: {
    url: manager.permissionManager.url,
    method: 'POST',
    permission: 'permission_create'
  },
  permissionEdit: {
    url: manager.permissionManager.url,
    method: 'PUT',
    permission: 'permission_update'
  },
  permissionDelete: {
    url: manager.permissionManager.url,
    method: 'DELETE',
    permission: 'permission_delete'
  }
}
