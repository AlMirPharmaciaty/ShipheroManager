import { APIs, manager } from '@/apis'

export default {
  path: 'permissions',
  name: 'permissions',
  meta: { title: 'Permissions', icon: 'lock', permission: manager.permissionManager.permission },
  children: [
    {
      path: '',
      name: 'permission-list',
      meta: {
        title: 'Permission Manager',
        permission: APIs.permissionList.permission
      },
      component: () => import('@/views/manager/permission/PermissionList.vue')
    }
  ]
}
