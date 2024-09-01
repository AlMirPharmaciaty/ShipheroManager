<template>
  <ViewContainer>
    <template v-slot:actions v-if="canCreateRole">
      <Action
        type="modal"
        modal-id="create-role"
        name="Create Role"
        class="btn btn-brand"
        icon="plus"
      />
      <CreateRoleModal :is-coming-from-data-table="true" :data-table-func="getRoles" />
    </template>
    <template v-slot:body>
      <div
        class="card card-body px-1 px-md-3 px-lg-4 flex-row justify-content-center flex-wrap gap-3 mb-4"
      >
        <div>
          <InputField v-model="searchQuery" id="search" label="Search" @keyup.enter="getRoles" />
        </div>
        <div>
          <SelectField
            id="permissions"
            label="Permissions"
            :multiple="true"
            :options="permissionsFilterOptions"
            v-model="permissionsFilter"
            :searchable="true"
            :search-function="getPermissions"
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
          :data-table-func="getRoles"
        />
      </div>
      <div class="card card-body px-1 px-md-3 px-lg-4 py-3 mt-3 gap-3 text-center">
        <PaginationWrapper
          v-model:current-page="currentPage"
          v-model:per-page="perPage"
          :dataset-length="dataset.length"
          :total="total"
          :filtered="filtered"
          label="Roles"
          :is-loading="isDataLoading"
        />
      </div>
    </template>
  </ViewContainer>
</template>

<script setup>
import { ref, watchEffect } from 'vue'
import { useRoute } from 'vue-router'

import { APIs } from '@/apis'
import ViewContainer from '@/views/ViewContainer.vue'
import DataTable from '@/components/DataTable.vue'
import InputField from '@/components/InputField.vue'
import SelectField from '@/components/SelectField.vue'
import MyButton from '@/components/MyButton.vue'
import Action from '@/components/Action.vue'
import PaginationWrapper from '@/components/PaginationWrapper.vue'
import { isUserAuthorized } from '@/composables/auth-manager'
import { fetchData } from '@/composables/data-fetcher'

import CreateRoleModal from './CreateRoleModal.vue'
import EditRoleModal from './EditRoleModal.vue'
import DeleteRoleModal from './DeleteRoleModal.vue'

const route = useRoute()
const routeQuery = route.query

const columns = [
  { label: 'Id', field: 'id', key: true, wrapper: 'text-center', display: false, sortable: true },
  { label: 'Role', field: 'name', wrapper: 'text-center', sortable: true },
  {
    label: 'Permissions',
    field: 'permission_count',
    wrapper: 'text-center',
    type: 'component',
    component: Action,
    sortable: false
  },
  {
    label: 'Users',
    field: 'user_count',
    wrapper: 'text-center',
    type: 'component',
    component: Action,
    sortable: false
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
const searchQuery = ref(routeQuery.roles ? routeQuery.roles.split(',')[0] : '')
const sortBy = ref('created_at')
const sortOrder = ref('desc')
const sortOptions = columns.filter((col) => col.sortable)
const currentPage = ref(1)
const perPage = ref(10)
const permissionsFilter = ref(routeQuery.perms ? routeQuery.perms.split(',') : [])
const permissionsFilterOptions = ref([])
const total = ref(0)
const filtered = ref(0)
const dataActions = ref([])
const dataActionModals = [EditRoleModal, DeleteRoleModal]

function toggleSortOrder() {
  sortOrder.value = sortOrder.value == 'desc' ? 'asc' : 'desc'
}

function getPermissions(query = '', perms = '') {
  fetchData(APIs.permissionList.url, true, { query: query, perms: perms }).then((response) => {
    response.data.forEach((perm) => {
      if (!permissionsFilterOptions.value.find((p) => p.field == perm.id)) {
        permissionsFilterOptions.value.push({ label: perm.name, field: perm.id })
      }
    })
  })
}
getPermissions()

async function getRoles() {
  isDataLoading.value = true
  dataActions.value = []
  try {
    const params = {
      page: currentPage.value,
      perms: permissionsFilter.value,
      limit: perPage.value,
      query: searchQuery.value,
      sort_by: sortBy.value,
      sort_order: sortOrder.value
    }
    const response = await fetchData(APIs.roleList.url, true, params)
    const roles = response.data
    roles.forEach((role) => {
      role.permission_count = renderPermissions(role)
      role.user_count = renderUsers(role)
      setDataActions(role)
    })
    dataset.value = roles
    total.value = response.pagination.total
    filtered.value = response.pagination.filtered
  } finally {
    isDataLoading.value = false
  }
}

watchEffect(() => getRoles())

const canCreateRole = isUserAuthorized(APIs.roleCreate.permission)
const isActionsEnabled = ref(false)
function setDataActions(role) {
  const actions = []
  if (isUserAuthorized(APIs.roleEdit.permission)) {
    actions.push({
      name: 'Edit',
      type: 'modal',
      modalId: 'edit-role',
      icon: 'pen',
      class: 'text-primary'
    })
  }
  if (isUserAuthorized(APIs.roleDelete.permission)) {
    actions.push({
      name: 'Delete',
      type: 'modal',
      modalId: 'delete-role',
      icon: 'trash-can',
      class: 'text-danger'
    })
  }
  if (actions.length > 0) isActionsEnabled.value = true
  dataActions.value.push({ id: role.id, actions: actions })
}

function renderPermissions(role) {
  return {
    type: 'route',
    routeLink: {
      name: 'permission-list',
      query: { roles: role.id }
    },
    name: role.permissions.length,
    class: 'btn btn-link btn-rounded'
  }
}

function renderUsers(role) {
  return {
    type: 'route',
    routeLink: {
      name: 'user-list',
      query: { roles: role.id }
    },
    name: role.users.length,
    class: 'btn btn-link btn-rounded'
  }
}
</script>

<style scoped></style>
