import { APIs, manager } from '@/apis'

export default {
  path: 'roles',
  name: 'roles',
  meta: { title: 'Roles', icon: 'user-gear', permission: manager.roleManager.permission },
  children: [
    {
      path: '',
      name: 'role-list',
      meta: {
        title: 'Role Manager',
        permission: APIs.roleList.permission
      },
      component: () => import('@/views/manager/role/RoleList.vue')
    }
  ]
}
