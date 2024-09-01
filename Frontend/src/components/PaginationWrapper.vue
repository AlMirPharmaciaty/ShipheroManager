<template>
  <div class="row row-gap-4 align-items-center">
    <div class="col-lg-3 col-12"><p class="mb-0" v-text="paginationInfo"></p></div>
    <div class="col-lg-6 col-12 d-flex justify-content-center">
      <div>
        <Pagination
          :current-page="currentPage"
          :total="filtered"
          :per-page="perPage"
          @page-event="changePage"
          :disabled="isLoading"
        />
      </div>
    </div>
    <div class="col-lg-3 col-12 d-flex justify-content-center">
      <div>
        <SelectField
          v-model="perPage"
          id="perPage"
          :label="`${label} per page`"
          :options="perPageOptions"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

import Pagination from '@/components/Pagination.vue'
import SelectField from '@/components/SelectField.vue'

const perPage = defineModel('perPage')
const currentPage = defineModel('currentPage')

const props = defineProps({
  datasetLength: { type: Number },
  total: { type: Number },
  filtered: { type: Number },
  label: { default: 'items' },
  isLoading: { default: false, type: Boolean }
})

const perPageOptions = [
  { label: '10', field: 10 },
  { label: '25', field: 25 },
  { label: '50', field: 50 },
  { label: '100', field: 100 }
]

const paginationInfo = computed(() =>
  getPaginationInfo(
    props.datasetLength,
    perPage.value,
    currentPage.value,
    props.total,
    props.filtered,
    props.label
  )
)

function changePage(nextPage) {
  currentPage.value = nextPage
}

function getPaginationInfo(
  dataset_length,
  per_page,
  current_page,
  total,
  filtered,
  label = 'items'
) {
  label = label.toLowerCase()
  const start = dataset_length > 0 ? per_page * (current_page - 1) + 1 : 0
  var end = start - 1 + dataset_length
  end = end < 0 ? 0 : end
  var info = `Showing ${start} to ${end} of ${filtered} ${label}`
  if (total != filtered) info += ` (filtered from ${total} ${label})`
  return info
}
</script>

<style scoped></style>
