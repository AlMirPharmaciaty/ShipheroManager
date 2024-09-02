<template>
  <ViewContainer>
    <template v-slot:actions> </template>

    <template v-slot:body>
      <div
        class="card card-body px-1 px-md-3 px-lg-4 flex-row justify-content-center flex-wrap gap-3 mb-4"
      >
        <div>
          <InputField v-model="searchQuery" id="search" label="Search" @keyup.enter="getUsers" />
        </div>
        <div>
          <SelectField
            v-model="excludeDeleted"
            id="exclude_deleted"
            label="Exclude Deleted Users"
            :options="excludeDeletedOptions"
          />
        </div>
        <div>
          <SelectField
            id="roles"
            label="Roles"
            :multiple="true"
            :options="rolesFilterOptions"
            v-model="rolesFilter"
            :searchable="true"
            :search-function="getRoles"
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
          :data-table-func="getUsers"
        />
      </div>
      <div class="card card-body px-1 px-md-3 px-lg-4 py-3 mt-3 gap-3 text-center">
        <PaginationWrapper
          v-model:current-page="currentPage"
          v-model:per-page="perPage"
          :dataset-length="dataset.length"
          :total="total"
          :filtered="filtered"
          label="Users"
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
import PaginationWrapper from '@/components/PaginationWrapper.vue'
import Action from '@/components/Action.vue'
import { isUserAuthorized } from '@/composables/auth-manager'
import { fetchData } from '@/composables/data-fetcher'

import deleteUserModal from './DeleteUserModal.vue'
import UserTableView from './UserTableView.vue'

const route = useRoute()
const routeQuery = route.query

const columns = [
  { label: 'Id', field: 'id', key: true, display: false, sortable: true },
  { label: 'Username', field: 'username', display: false },
  { label: 'Email', field: 'email', display: false },
  {
    label: 'User',
    field: 'user',
    type: 'component',
    component: UserTableView,
    sortable: false
  },
  {
    label: 'Roles',
    field: 'roles',
    wrapper: 'd-flex flex-wrap gap-1 justify-content-center',
    type: 'component-list',
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
  },
  {
    label: 'Active',
    field: 'deleted',
    type: 'bool',
    reverse: true,
    wrapper: 'text-center',
    sortable: true
  }
]

const dataset = ref([])
const isDataLoading = ref(true)
const searchQuery = ref('')
const excludeDeleted = ref(true)
const excludeDeletedOptions = [
  { label: 'Yes', field: true },
  { label: 'No', field: false }
]
const rolesFilter = ref(routeQuery.roles ? routeQuery.roles.split(',') : [])
const rolesFilterOptions = ref([])
const sortBy = ref('created_at')
const sortOrder = ref('desc')
const sortOptions = columns.filter((col) => col.sortable)
const currentPage = ref(1)
const total = ref(0)
const filtered = ref(0)
const perPage = ref(10)
const dataActions = ref([])
const dataActionModals = [deleteUserModal]

function toggleSortOrder() {
  sortOrder.value = sortOrder.value == 'desc' ? 'asc' : 'desc'
}

function getRoles(query = '', roles = '') {
  fetchData(APIs.roleList.url, true, { query: query, roles: roles }).then((response) => {
    response.data.forEach((role) => {
      if (!rolesFilterOptions.value.find((p) => p.field == role.id)) {
        rolesFilterOptions.value.push({ label: role.name, field: role.id })
      }
    })
  })
}
getRoles()

async function getUsers() {
  isDataLoading.value = true
  dataActions.value = []
  try {
    const params = {
      page: currentPage.value,
      limit: perPage.value,
      query: searchQuery.value,
      exclude_deleted: excludeDeleted.value,
      roles: rolesFilter.value ? rolesFilter.value.join(',') : null,
      sort_by: sortBy.value,
      sort_order: sortOrder.value
    }
    const response = await fetchData(APIs.userList.url, true, params)
    const users = response.data
    users.forEach((user) => {
      user.user = user
      user.roles = user.roles.map((role) => renderRoles(role))
      setDataActions(user)
    })
    dataset.value = users
    total.value = response.pagination.total
    filtered.value = response.pagination.filtered
  } finally {
    isDataLoading.value = false
  }
}

watchEffect(() => getUsers())

const isActionsEnabled = ref(false)
function setDataActions(user) {
  const actions = []
  if (isUserAuthorized(APIs.userGet.permission)) {
    actions.push({
      name: 'View',
      type: 'route',
      routeLink: { name: 'view-user', params: { user_id: user.id } },
      icon: 'eye',
      class: 'text-brand'
    })
  }
  if (isUserAuthorized(APIs.userEdit.permission)) {
    actions.push({
      name: 'Edit',
      type: 'route',
      routeLink: { name: 'edit-user', params: { user_id: user.id } },
      icon: 'pen',
      class: 'text-primary'
    })
  }
  if (isUserAuthorized(APIs.userDelete.permission) && !user.deleted) {
    actions.push({
      name: 'Delete',
      type: 'modal',
      modalId: 'delete-user',
      icon: 'trash-can',
      class: 'text-danger'
    })
  }
  if (actions.length > 0) isActionsEnabled.value = true
  dataActions.value.push({ id: user.id, actions: actions })
}

function renderRoles(role) {
  return {
    type: 'route',
    routeLink: {
      name: 'role-list',
      query: { roles: role.id }
    },
    name: role.name,
    class: 'badge badge-success text-brand'
  }
}
</script>

<style scoped></style>
