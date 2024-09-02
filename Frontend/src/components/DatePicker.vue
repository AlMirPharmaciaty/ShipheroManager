<template>
  <div
    ref="datePicker"
    class="form-outline"
    data-mdb-input-init
    :data-mdb-container="container"
    :data-mdb-format="format"
  >
    <input
      data-mdb-toggle="datepicker"
      :id="id"
      :name="id"
      :class="`form-control ${size ? `form-control-${size}` : ''}`"
      type="text"
      :required="required"
      :disabled="disabled"
      :readonly="readonly"
    />
    <label :for="id" class="form-label" v-text="label"></label>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const datePicker = ref()
const value = defineModel()

const props = defineProps({
  id: {},
  label: { default: 'Select a date' },
  size: {},
  required: { default: false, type: Boolean },
  disabled: { default: () => false, type: Boolean },
  readonly: { default: false, type: Boolean },
  container: { default: 'body' },
  format: { default: 'yyyy-mm-dd' },
  disablePast: { default: false },
  disableFuture: { default: false }
})

onMounted(() => {
  const options = {
    disablePast: props.disablePast,
    disableFuture: props.disableFuture
  }
  new mdb.Datepicker(datePicker.value, options)
  datePicker.value.addEventListener('valueChanged.mdb.datepicker', (e) => {
    value.value = e.target.querySelector(`#${props.id}`).value
  })
})
</script>

<style>
.datepicker-toggle-button:hover {
  color: var(--color-brand) !important;
}

.datepicker-toggle-button:focus {
  color: var(--color-brand) !important;
}
</style>
