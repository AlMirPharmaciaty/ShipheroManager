<template>
  <ViewContainer>
    <template v-slot:actions v-if="canCreateSnapshot">
      <!-- <Action
        type="modal"
        modal-id="create-role"
        name="Create Role"
        class="btn btn-brand"
        icon="plus"
      />
      <CreateRoleModal :is-coming-from-data-table="true" :data-table-func="getInventorySnapshots" /> -->
    </template>
    <template v-slot:body>
      <div
        class="card card-body px-1 px-md-3 px-lg-4 flex-row justify-content-center flex-wrap gap-3 mb-4"
      >
        <div>
          <InputField
            v-model="searchQuery"
            id="search"
            label="Search"
            @keyup.enter="getInventorySnapshots"
          />
        </div>
        <div>
          <SelectField
            id="inventory-snapshot-status"
            label="Status"
            :multiple="true"
            :options="statusFilterOptions"
            v-model="statusFilter"
          />
        </div>
        <div>
          <SelectField v-model="sortBy" id="sortBy" label="Sort by" :options="sortOptions" />
        </div>
        <MyButton
          @click-event="toggleSortOrder"
          :icon="`arrow-${sortOrder == 'asc' ? 'up' : 'down'}-wide-short`"
          color="brand"
        />
      </div>
      <div class="card card-body px-1 px-md-3 px-lg-4">
        <DataTable
          :columns="columns"
          :dataset="dataset"
          :is-data-loading="isDataLoading"
          :actions-enabled="isActionsEnabled"
          :data-actions="dataActions"
          :data-action-modals="dataActionModals"
          :data-table-func="getInventorySnapshots"
        />
      </div>
      <div class="card card-body px-1 px-md-3 px-lg-4 py-3 mt-3 gap-3 text-center">
        <PaginationWrapper
          v-model:current-page="currentPage"
          v-model:per-page="perPage"
          :dataset-length="dataset.length"
          :total="total"
          :filtered="filtered"
          label="Snapshots"
          :is-loading="isDataLoading"
        />
      </div>
    </template>
  </ViewContainer>
</template>

<script setup>
import { ref, watchEffect } from 'vue'

import { APIs } from '@/apis'
import ViewContainer from '@/views/ViewContainer.vue'
import DataTable from '@/components/DataTable.vue'
import InputField from '@/components/InputField.vue'
import SelectField from '@/components/SelectField.vue'
import MyButton from '@/components/MyButton.vue'
import PaginationWrapper from '@/components/PaginationWrapper.vue'
import { isUserAuthorized } from '@/composables/auth-manager'
import { fetchData } from '@/composables/data-fetcher'
import { notify } from '@/composables/bootstrap-utils'

const columns = [
  { label: 'Id', field: 'id', key: true, wrapper: 'text-center', sortable: true },
  { label: 'Snapshot Id', field: 'snapshot_id', wrapper: 'text-center', sortable: true },
  {
    label: 'Status',
    field: 'status',
    wrapper: 'text-center',
    type: 'html',
    sortable: true
  },
  {
    label: 'Created at',
    field: 'created_at',
    type: 'datetime',
    wrapper: 'text-center',
    sortable: true
  },
  {
    label: 'Updated at',
    field: 'updated_at',
    type: 'datetime',
    wrapper: 'text-center',
    sortable: true
  }
]

const dataset = ref([])
const isDataLoading = ref(true)
const searchQuery = ref('')
const sortBy = ref('created_at')
const sortOrder = ref('desc')
const sortOptions = columns.filter((col) => col.sortable)
const currentPage = ref(1)
const perPage = ref(10)
const statusFilter = ref([])
const statusFilterOptions = [
  { label: 'Enqueued', field: 'enqueued', color: 'primary' },
  { label: 'Pending', field: 'pending', color: 'info' },
  { label: 'Processing', field: 'processing', color: 'warning' },
  { label: 'Success', field: 'success', color: 'success' }
]
const total = ref(0)
const filtered = ref(0)
const dataActions = ref([])
const dataActionModals = []

function toggleSortOrder() {
  sortOrder.value = sortOrder.value == 'desc' ? 'asc' : 'desc'
}

async function getInventorySnapshots() {
  isDataLoading.value = true
  dataActions.value = []
  try {
    const params = {
      query: searchQuery.value,
      page: currentPage.value,
      limit: perPage.value,
      sort_by: sortBy.value,
      sort_order: sortOrder.value
    }
    const response = await fetchData(APIs.inventorySnapshotList.url, true, params)
    const snapshots = response.data
    snapshots.forEach((snapshot) => {
      snapshot.status = renderStatus(snapshot.status)
      setDataActions(snapshot)
    })
    dataset.value = snapshots
    total.value = response.pagination.total
    filtered.value = response.pagination.filtered
  } finally {
    isDataLoading.value = false
  }
}

watchEffect(() => getInventorySnapshots())

const canCreateSnapshot = isUserAuthorized(APIs.inventorySnapshotCreate.permission)
const isActionsEnabled = ref(false)
function setDataActions(snapshot) {
  const actions = []
  if (isUserAuthorized(APIs.inventorySnapshotEdit.permission)) {
    actions.push({
      name: 'Update status',
      type: 'button',
      icon: 'rotate',
      class: 'text-warning',
      buttonFunc: updateStatus,
      'data-id': snapshot.id
    })
  }
  if (actions.length > 0) isActionsEnabled.value = true
  dataActions.value.push({ id: snapshot.id, actions: actions })
}

function renderStatus(status) {
  const color = statusFilterOptions.find((s) => s.field == status)
  return `<span class="badge badge-${color.color}">${status}</span>`
}

function updateStatus(e) {
  try {
    var snapshotDbID = e.target.getAttribute('data-id')
    if (!snapshotDbID) {
      snapshotDbID = e.target.parentElement.getAttribute('data-id')
    }
    console.log(snapshotDbID)
  } catch (error) {
    notify('Failed to update status', 'danger')
  }
}
</script>

<style scoped></style>
