<template>
  <RouterLink :to="routeLink" v-if="type == 'route'" ref="action" active-class="active">
    <i v-if="icon" :class="`fa-fw fa-${iconType} fa-${icon} fa-fw me-2`"></i>
    <span v-text="name"></span>
  </RouterLink>
  <a v-else-if="type == 'modal'" @click="showModal(modalId)" role="button" ref="action">
    <i v-if="icon" :class="`fa-fw fa-${iconType} fa-${icon} fa-fw me-2`"></i>
    <span v-text="name"></span>
  </a>
  <a v-else-if="type == 'button'" role="button" ref="action" @click="buttonFunc">
    <i v-if="icon" :class="`fa-fw fa-${iconType} fa-${icon} fa-fw me-2`"></i>
    <span v-text="name"></span>
  </a>
</template>

<script setup>
import { initRipple, showModal } from '@/composables/bootstrap-utils'
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

const action = ref()

const props = defineProps({
  name: {},
  type: {},
  routeLink: {},
  modalId: {},
  icon: {},
  rippleColor: {},
  iconType: { default: 'solid' },
  buttonFunc: {}
})

onMounted(() => {
  try {
    initRipple(action.value.$el, props.rippleColor)
  } finally {
    initRipple(action.value, props.rippleColor)
  }
})
</script>

<style scoped></style>
