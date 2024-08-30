<template>
  <div class="d-flex flex-row gap-2 align-items-start">
    <Image
      class="rounded-circle"
      :image="`${APIs.userAvatarURL}/${user.avatar}`"
      :delay="0"
      width="40"
      height="40"
    />
    <div class="d-flex flex-column">
      <span class="fw-medium">{{ user.username }}</span>
      <span class="text-muted">{{ user.email }}</span>
    </div>
  </div>
</template>

<script setup>
import { APIs } from '@/apis'
import Image from '@/components/Image.vue'

defineProps({
  user: {}
})
</script>

<style scoped></style>
