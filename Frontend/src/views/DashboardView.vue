<template>
  <ViewContainer>
    <template v-slot:body>
      <h2>Welcome, {{ user.username }}!</h2>
    </template>
  </ViewContainer>
</template>

<script setup>
ViewContainer
import { getUser } from '@/composables/auth-manager'
import ViewContainer from '@/views/ViewContainer.vue'

const user = getUser()
</script>

<style scoped></style>
