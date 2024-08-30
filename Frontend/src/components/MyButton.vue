<template>
  <button
    ref="myButton"
    :type="type"
    :class="`btn btn-${color} ${size ? `btn-${size}` : ''}`"
    data-mdb-ripple-init
    :disabled="disabled"
    @click="$emit('clickEvent')"
  >
    <div v-if="isLoading" class="d-flex align-items-center gap-2 justify-content-center">
      <span>Please wait...</span>
      <span class="spinner-border spinner-border-sm"></span>
    </div>
    <template v-else>
      <i v-if="icon" :class="`fa-${iconType} fa-${icon}`"></i>
      <span :class="[icon && text ? 'ms-2' : '']">{{ text }}</span>
    </template>
  </button>
</template>

<script setup>
import { initRipple } from '@/composables/bootstrap-utils'
import { onMounted, ref } from 'vue'

const myButton = ref()

const props = defineProps({
  text: {},
  icon: {},
  type: { default: 'button' },
  color: { default: 'primary' },
  size: {},
  disabled: { default: false, type: Boolean },
  isLoading: { default: false, type: Boolean },
  rippleColor: {},
  iconType: { default: 'regular' }
})

onMounted(() => {
  initRipple(myButton.value, props.rippleColor)
})
</script>

<style scoped></style>
