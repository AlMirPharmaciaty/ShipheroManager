import router from '@/router'

export function getToken() {
  return localStorage.getItem('token')
}

export function getUser() {
  return JSON.parse(localStorage.getItem('user'))
}

export function saveToken(token) {
  localStorage.setItem('token', token)
}

export function saveUser(user) {
  localStorage.setItem('user', JSON.stringify(user))
}

export function saveUserCredentials(token, user) {
  saveToken(token)
  saveUser(user)
}

export function isUserAuthenticated() {
  return getToken() && getUser()
}

export function isUserAuthorized(permission = null) {
  if (!permission) return true
  if (typeof permission == 'string') permission = [permission]
  const user = getUser()
  return user.roles.some((role) => role.permissions.some((p) => permission.includes(p.name)))
}

export function logOutUser() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  return router.push({ name: 'login' })
}
