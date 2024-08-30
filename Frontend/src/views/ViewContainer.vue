<template>
  <div
    class="mb-4 d-flex justify-content-md-between justify-content-center align-items-center flex-wrap gap-3"
  >
    <div class="d-flex gap-2 align-items-center">
      <i :class="`fa-duotone fa-${route.meta.icon} fa-xl fa-fw`"></i>
      <h2 class="mb-0 fw-bold" v-text="route.meta.title"></h2>
    </div>
    <slot name="actions"></slot>
  </div>
  <slot name="body"></slot>
</template>

<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<style scoped></style>
