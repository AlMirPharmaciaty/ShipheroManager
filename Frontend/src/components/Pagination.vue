<template>
  <nav>
    <ul class="pagination mb-0 flex-wrap justify-content-center">
      <!-- Previous Button -->
      <li class="page-item" :class="[currentPage <= 1 || disabled ? 'disabled' : '']">
        <span v-if="currentPage <= 1 || disabled" class="page-link" v-text="prevText"></span>
        <a
          v-else
          class="page-link"
          href="#"
          v-text="prevText"
          @click="$emit('pageEvent', currentPage - 1)"
        ></a>
      </li>
      <li
        v-for="page in range"
        :key="page"
        class="page-item"
        :class="{ active: page == currentPage, disabled: page == ellipsis }"
      >
        <a
          v-if="page != currentPage && page != ellipsis"
          class="page-link"
          :class="[disabled ? 'disabled' : '']"
          href="#"
          v-text="page"
          @click="$emit('pageEvent', page)"
        ></a>
        <span v-else class="page-link" v-text="page"></span>
      </li>
      <!-- Next Button -->
      <li class="page-item" :class="[currentPage >= totalPages || disabled ? 'disabled' : '']">
        <span
          v-if="currentPage >= totalPages || disabled"
          class="page-link"
          v-text="nextText"
        ></span>
        <a
          v-else
          class="page-link"
          href="#"
          v-text="nextText"
          @click="$emit('pageEvent', currentPage + 1)"
        ></a>
      </li>
    </ul>
  </nav>
</template>

<script setup>
import { computed, watch } from 'vue'

const props = defineProps({
  ellipsis: { default: '...' },
  btnCount: { default: 6, type: Number },
  total: { default: 10, type: Number },
  perPage: { default: 10, type: Number },
  currentPage: { default: 1, type: Number },
  prevText: { default: 'Prev' },
  nextText: { default: 'Next' },
  disabled: { default: false, type: Boolean }
})

function createRange(length, start = 0) {
  return Array.from({ length }, (_, k) => start + k)
}

const totalPages = computed(() => {
  return Math.ceil(props.total / props.perPage) || 1
})

const range = computed(() => {
  if (
    totalPages.value <= 0 ||
    isNaN(totalPages.value) ||
    totalPages.value > Number.MAX_SAFE_INTEGER
  )
    return []

  if (props.btnCount <= 0) return []
  else if (props.btnCount === 1) return [props.currentPage]

  if (totalPages.value <= props.btnCount) {
    return createRange(totalPages.value, 1)
  }

  const even = props.btnCount % 2 === 0
  const middle = even ? props.btnCount / 2 : Math.floor(props.btnCount / 2)
  const left = even ? middle : middle + 1
  const right = totalPages.value - middle

  if (left - props.currentPage >= 0) {
    return [...createRange(Math.max(1, props.btnCount - 1), 1), props.ellipsis, totalPages.value]
  } else if (props.currentPage - right >= (even ? 1 : 0)) {
    const rangeLength = props.btnCount - 1
    const rangeStart = totalPages.value - rangeLength + 1
    return [1, props.ellipsis, ...createRange(rangeLength, rangeStart)]
  } else {
    const rangeLength = Math.max(1, props.btnCount - 3)
    const rangeStart =
      rangeLength === 1 ? props.currentPage : props.currentPage - Math.ceil(rangeLength / 2) + 1
    return [
      1,
      props.ellipsis,
      ...createRange(rangeLength, rangeStart),
      props.ellipsis,
      totalPages.value
    ]
  }
})
const emit = defineEmits(['pageEvent'])
watch(
  () => [props.perPage, props.total],
  () => {
    emit('pageEvent', 1)
  }
)
</script>

<style scoped></style>
