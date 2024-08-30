<template>
  <i ref="copyBtn" class="fa-regular fa-copy" role="button"></i>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { initClipboard } from '@/composables/bootstrap-utils'

const copyBtn = ref()

const props = defineProps({
  target: {}
})

onMounted(() => {
  initClipboard(copyBtn.value, props.target)
})
</script>

<style scoped></style>
