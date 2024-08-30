<template>
  <h1 class="mb-4 text-center fw-bolder">Sign Up</h1>
  <form @submit.prevent="register">
    <InputField
      id="username"
      type="text"
      label="Username"
      class="mb-3"
      size="lg"
      :required="true"
      v-model="username"
    />
    <InputField
      id="email"
      type="email"
      label="Email"
      class="mb-3"
      size="lg"
      :required="true"
      v-model="email"
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
      text="Register"
      type="submit"
      color="brand"
      size="lg"
      class="w-100"
      :disabled="btnDisabled"
      :is-loading="isLoading"
    />
  </form>
  <div class="mt-4">
    <p class="mb-1 text-center">Already have an account?</p>
    <RouterLink
      :to="{ name: 'login' }"
      text="Log in"
      class="btn btn-dark w-100"
      data-mdb-ripple-init
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import MyButton from '@/components/MyButton.vue'
import InputField from '@/components/InputField.vue'
import { notify } from '@/composables/bootstrap-utils'
import { fetchData } from '@/composables/data-fetcher'
import { APIs } from '@/apis'

const router = useRouter()
const username = ref()
const email = ref()
const password = ref()
const btnDisabled = ref(false)
const isLoading = ref(false)

async function register() {
  btnDisabled.value = true
  isLoading.value = true
  try {
    var data = { username: username.value, email: email.value, password: password.value }
    const response = await fetchData(
      APIs.register.url,
      false,
      null,
      data,
      'json',
      APIs.register.method
    )
    console.log(response)
    if (response.success) {
      notify('Successfully created a new account. Please Login to continue.')
      router.push({ name: 'login' })
    }
  } finally {
    btnDisabled.value = false
    isLoading.value = false
  }
}
</script>

<style scoped></style>
