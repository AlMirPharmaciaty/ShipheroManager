<template>
  <img
    ref="imageRef"
    :class="[showPlaceholder ? 'placeholder' : '']"
    data-mdb-lazy-load-init
    :data-mdb-lazy-src="image"
    :data-mdb-lazy-delay="delay"
    :data-mdb-lazy-placeholder="placeholder"
    :data-mdb-lazy-animation="animation"
  />
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'

const imageRef = ref()

const props = defineProps({
  image: {},
  showPlaceholder: { default: true },
  placeholder: { default: 'https://place-hold.it/100?text=' },
  delay: { default: 500 },
  animation: { default: 'fade-in' }
})

watch(
  () => props.image,
  (newImg) => (imageRef.value.src = newImg)
)

onMounted(() => {
  mdb.LazyLoad.getOrCreateInstance(imageRef.value)
  imageRef.value.addEventListener('contentLoaded.mdb.lazyLoad', (e) => {
    e.target.classList.remove('placeholder')
  })
})
</script>

<style scoped></style>
