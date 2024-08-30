<template>
  <div class="d-flex flex-column align-items-center gap-3">
    <h1 class="display-5 fw-bold mb-0">Page Not Found</h1>
    <img src="/src/assets/img/error.png" width="350" />
    <p class="fs-5 mb-0">Oops! The page you're looking for no longer exists or never existed.</p>

    <div class="d-flex flex-wrap gap-2">
      <Action
        type="route"
        :route-link="{ name: 'dashboard' }"
        name="Go to dashboard"
        class="btn btn-brand btn-lg"
      />
      <Action
        type="button"
        @click="router.go(-1)"
        name="Go back"
        class="btn btn-secondary btn-lg"
      />
    </div>
  </div>
</template>

<script setup>
import Action from '@/components/Action.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped></style>
