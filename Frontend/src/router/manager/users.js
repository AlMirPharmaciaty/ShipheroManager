import { APIs, manager } from '@/apis'

export default {
  path: 'users',
  name: 'users',
  meta: { title: 'Users', icon: 'users', permission: manager.userManager.permission },
  children: [
    {
      path: '',
      name: 'user-list',
      meta: {
        title: 'User Manager',
        permission: APIs.userList.permission
      },
      component: () => import('@/views/manager/user/UserList.vue')
    },
    {
      path: 'view/:user_id',
      name: 'view-user',
      meta: {
        title: 'User Detail',
        permission: APIs.userGet.permission
      },
      component: () => import('@/views/manager/user/ViewUser.vue')
    },
    {
      path: 'edit/:user_id',
      name: 'edit-user',
      meta: {
        title: 'Edit User',
        permission: APIs.userEdit.permission
      },
      component: () => import('@/views/manager/user/EditUser.vue')
    }
  ]
}
