<template>
  <component :is="route.meta.layout || 'div'">
    <RouterView />
  </component>
</template>

<script setup>
import { RouterView, useRoute, useRouter } from 'vue-router'

import { hideModalAll, notify } from '@/composables/bootstrap-utils'
import { logOutUser } from '@/composables/auth-manager'

const route = useRoute()
const router = useRouter()

const { fetch: originalFetch } = window
window.fetch = async (...args) => {
  try {
    let [resource, config] = args
    let response = await originalFetch(resource, config)
    if (!response.ok) {
      var message = await response.json()
      message = 'detail' in message ? message.detail : JSON.stringify(message)
      notify(message.toString(), 'danger')
      if (response.status == 401) setTimeout(() => (hideModalAll(), logOutUser()), 500)
      if (response.status == 403)
        setTimeout(() => {
          hideModalAll()
          router.push({ name: 'dashboard' })
        }, 500)
      return Promise.reject(response)
    }
    return response
  } catch {
    notify('Failed to get a response from the server.', 'danger')
    if (!['register', 'login'].includes(route.name)) {
      setTimeout(() => (hideModalAll(), logOutUser()), 500)
    }
  }
}
</script>

<style></style>
