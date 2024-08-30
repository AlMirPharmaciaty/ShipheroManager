<template>
  <div ref="alert" data-mdb-alert-init class="alert mb-0" role="alert" :data-mdb-color="color">
    <slot />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const alert = ref()
defineProps({
  color: { default: 'primary' }
})

onMounted(() => {
  new mdb.Alert(alert.value)
})
</script>

<style lang="scss" scoped></style>
