<template>
  <select
    ref="selectField"
    data-mdb-select-init
    :data-mdb-size="size"
    :data-mdb-container="container"
    v-model="value"
    :id="id"
    :name="id"
    :class="`form-control ${size ? `form-control-${size}` : ''}`"
    :required="required"
    :disabled="disabled"
    :readonly="readonly"
    :multiple="multiple"
    :data-mdb-displayed-labels="displayedLabels"
    :data-mdb-options-selected-label="optionsSelectedLabel"
    :data-mdb-filter="searchable"
  >
    <option v-for="option in options" :value="option.field" :key="option.field">
      {{ option.label }}
    </option>
  </select>
  <label v-if="label" class="form-label select-label" :for="id">{{ label }}</label>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const selectField = ref()
const value = defineModel()

const props = defineProps({
  id: {},
  label: {},
  options: { type: Array },
  size: { default: 'default' },
  required: { default: false, type: Boolean },
  disabled: { default: false, type: Boolean },
  readonly: { default: false, type: Boolean },
  multiple: { default: false, type: Boolean },
  searchable: { default: false, type: Boolean },
  displayedLabels: { default: 5 },
  optionsSelectedLabel: { default: 'options selected' },
  container: { default: 'body' },
  searchFunction: {}
})

onMounted(() => {
  mdb.Select.getOrCreateInstance(selectField.value)
  if (props.searchable) {
    selectField.value.addEventListener('search.mdb.select', (e) => {
      props.searchFunction(e.value)
    })
  }
})
</script>
