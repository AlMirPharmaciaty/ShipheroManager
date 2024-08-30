import { createRouter, createWebHistory } from 'vue-router'

import AuthLayout from '@/layouts/AuthLayout.vue'
import MainLayout from '@/layouts/MainLayout.vue'
import { isUserAuthorized, isUserAuthenticated } from '@/composables/auth-manager'

import manager from './manager'
import { notify } from '@/composables/bootstrap-utils'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    meta: {
      title: 'Dashboard',
      icon: 'home',
      layout: MainLayout,
      authRequired: true,
      displayOnNav: true
    },
    component: () => import('@/views/DashboardView.vue')
  },
  {
    path: '/login',
    name: 'login',
    meta: { title: 'Login', layout: AuthLayout, authRequired: false },
    component: () => import('@/views/auth/LoginView.vue')
  },
  {
    path: '/register',
    name: 'register',
    meta: { title: 'Register', layout: AuthLayout, authRequired: false },
    component: () => import('@/views/auth/SignupView.vue')
  },
  {
    path: '/profile',
    name: 'profile',
    meta: {
      title: 'My Profile',
      icon: 'user',
      layout: MainLayout,
      authRequired: true,
      displayOnNav: false
    },
    component: () => import('@/views/UserProfile.vue')
  }
]

routes.push(manager)
routes.push({
  path: '/:catchAll(.*)',
  name: 'error',
  meta: { title: 'Page not found', layout: MainLayout, authRequired: true },
  component: () => import('@/views/ErrorView.vue')
})

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes
})

router.beforeEach((to, from, next) => {
  var title = to.meta.title ? ` - ${to.meta.title}` : ''
  document.title = `Shiphero Manager${title}` || 'Shiphero Manager'
  const isUserLoggedIn = isUserAuthenticated()

  // Check if route requires authentication
  if (to.meta.authRequired) {
    // Check if user is authenticated
    if (isUserLoggedIn) {
      // Check if user is authorized
      if (isUserAuthorized(to.meta.permission)) next()
      else {
        // Redirect to error route if unauthorized
        notify('Not authorized', 'danger')
        next({ name: 'dashboard' })
      }
    } else {
      // Redirect user to login if not authenticated
      notify('Please login to continue', 'info')
      next({ name: 'login', query: { redirect: to.fullPath } })
    }
  } else {
    // If route doesn't required auth
    // Check if user is authenticated and is trying to access login or register page
    // Redirect to home if true
    if (isUserLoggedIn && ['login', 'register'].includes(to.name)) next({ name: 'dashboard' })
    else next() // else process to the unprotected route
  }
})

export default router
