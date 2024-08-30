<template>
  <div class="dropdown" ref="dropdown">
    <slot v-if="customTrigger" name="trigger"></slot>
    <MyButton
      v-if="!customTrigger"
      data-mdb-dropdown-init
      class="dropdown-toggle"
      :class="buttonClass"
      :text="text"
      :icon="icon"
      :color="color"
      :size="size"
      :disabled="disabled"
      :ripple-color="rippleColor"
      :data-mdb-boundary="boundary"
      :data-mdb-dropdown-animation="animation"
    />
    <ul class="dropdown-menu shadow-5 border border-2">
      <slot name="dropdownItems"></slot>
      <li v-for="item in items" :key="item.label">
        <component
          :is="item.component"
          v-bind="item.props"
          class="dropdown-item"
          :class="[item.disabled ? 'disabled' : '', item.active ? 'active' : '']"
        />
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import MyButton from '@/components/MyButton.vue'

const dropdown = ref()

defineProps({
  text: {},
  icon: {},
  color: { default: 'primary' },
  buttonClass: {},
  size: {},
  disabled: { default: false, type: Boolean },
  animation: { default: 'on' },
  boundary: { default: 'clippingParents' },
  rippleColor: {},
  items: { type: Array },
  customTrigger: { default: false, type: Boolean }
})

onMounted(() => {
  new mdb.Dropdown(dropdown.value.querySelector('[data-mdb-dropdown-init]'))
})
</script>

<style scoped></style>
