<template>
  <div class="form-outline" data-mdb-input-init ref="inputFieldOutline">
    <input
      ref="inputField"
      v-model="value"
      :type="type"
      :id="id"
      :name="id"
      :class="`form-control ${size ? `form-control-${size}` : ''}`"
      :required="required"
      :disabled="disabled"
      :readonly="readonly"
      :autocomplete="autocomplete"
      :autofocus="autofocus"
    />
    <label class="form-label" :for="id">{{ label }}</label>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'

const inputField = ref()
const inputFieldOutline = ref()
const value = defineModel()

const props = defineProps({
  id: {},
  type: { default: 'text' },
  label: {},
  size: {},
  required: { default: false, type: Boolean },
  disabled: { default: () => false, type: Boolean },
  readonly: { default: false, type: Boolean },
  autofocus: { default: false, type: Boolean },
  autocomplete: { default: 'off' },
  customAutoCompleteEnabled: { default: false, type: Boolean },
  customAutoCompleteOptions: { type: Array },
  container: { default: 'body' }
})

onMounted(() => {
  document.querySelectorAll('[data-mdb-input-init]').forEach((el) => {
    new mdb.Input(el).init()
  })

  if (props.customAutoCompleteEnabled) {
    const autoComplete = new mdb.Autocomplete(inputFieldOutline.value, {
      filter: (value) => {
        return props.customAutoCompleteOptions.filter((item) => {
          return item.toLowerCase().startsWith(value.toLowerCase())
        })
      },
      container: props.container
    })
    inputField.value.addEventListener('focus', () => {
      autoComplete.search('')
    })

    inputFieldOutline.value.addEventListener('itemSelect.mdb.autocomplete', (e) => {
      value.value = e.value
    })
  }
})

const userHasInput = ref(false)

watch(value, (newVal, oldVal) => {
  if (newVal != oldVal) {
    userHasInput.value = true
  }
})

watch(
  () => props.disabled,
  (newVal, oldVal) => {
    if (oldVal && !newVal && userHasInput.value) {
      setTimeout(() => {
        inputField.value.focus()
      }, 0)
      userHasInput.value = false
    }
  }
)
</script>
