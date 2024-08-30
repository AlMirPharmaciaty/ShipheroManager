<template>
  <h1 class="mb-4 text-center fw-bolder">Login</h1>
  <form @submit.prevent="login">
    <InputField
      id="email"
      type="email"
      label="Email"
      class="mb-3"
      size="lg"
      :required="true"
      v-model="email"
      autocomplete="on"
    />
    <InputField
      id="password"
      type="password"
      label="Password"
      class="mb-3"
      size="lg"
      :required="true"
      v-model="password"
    />
    <MyButton
      text="Log in"
      type="submit"
      color="brand"
      size="lg"
      class="w-100"
      :disabled="btnDisabled"
      :is-loading="isLoading"
    />
  </form>
  <div class="mt-4">
    <p class="mb-1 text-center">Don't have an account?</p>
    <RouterLink
      :to="{ name: 'register' }"
      text="Create a new account"
      class="btn btn-dark w-100"
      data-mdb-ripple-init
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import MyButton from '@/components/MyButton.vue'
import InputField from '@/components/InputField.vue'
import { notify } from '@/composables/bootstrap-utils'
import { saveUserCredentials } from '@/composables/auth-manager'
import { fetchData } from '@/composables/data-fetcher'
import { APIs } from '@/apis'

const route = useRoute()
const router = useRouter()

const email = ref('')
const password = ref('')
const btnDisabled = ref(false)
const isLoading = ref(false)

async function login() {
  btnDisabled.value = true
  isLoading.value = true
  try {
    var data = new FormData()
    data.append('username', email.value)
    data.append('password', password.value)
    const response = await fetchData(APIs.login.url, false, null, data, 'form', APIs.login.method)
    var token = `${response.token_type} ${response.access_token}`
    saveUserCredentials(token, response.user)
    notify('Successfully logged in')
    const redirectURL = route.query.redirect || { name: 'dashboard' }
    router.push(redirectURL)
  } finally {
    btnDisabled.value = false
    isLoading.value = false
  }
}
</script>

<style scoped></style>
