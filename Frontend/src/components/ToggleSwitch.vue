<template>
  <div class="form-check form-switch">
    <input v-model="value" class="form-check-input" type="checkbox" role="switch" :id="id" />
    <label class="form-check-label" :for="id" v-text="label"></label>
  </div>
</template>

<script setup>
const value = defineModel()
defineProps({
  id: {},
  label: {},
  disabled: { default: () => false, type: Boolean }
})
</script>

<style scoped></style>
