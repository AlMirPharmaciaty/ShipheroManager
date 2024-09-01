import { manager } from '@/apis'
import MainLayout from '@/layouts/MainLayout.vue'
import roles from './roles'
import users from './users'
import permissions from './permissions'

export default {
  path: '/manager',
  name: 'manager',
  meta: {
    title: 'Manager',
    icon: 'gear',
    layout: MainLayout,
    authRequired: true,
    permission: Object.values(manager).map((m) => m.permission),
    displayOnNav: true
  },
  children: [users, roles, permissions]
}
