<template>
  <ViewContainer>
    <template v-slot:actions v-if="canCreatePermission">
      <Action
        type="modal"
        modal-id="create-permission"
        name="Add Permission"
        class="btn btn-brand"
        icon="plus"
      />
      <CreatePermissionModal :is-coming-from-data-table="true" :data-table-func="getPermissions" />
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
            @keyup.enter="getPermissions"
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
          :data-table-func="getPermissions"
        />
      </div>
      <div class="card card-body px-1 px-md-3 px-lg-4 py-3 mt-3 gap-3 text-center">
        <div class="row row-gap-4 align-items-center">
          <div class="col-lg-3 col-12"><p class="mb-0" v-text="dataInfo"></p></div>
          <div class="col-lg-6 col-12 d-flex justify-content-center">
            <div>
              <Pagination
                :current-page="currentPage"
                :total="filtered"
                :per-page="perPage"
                @page-event="changePage"
                :disabled="isDataLoading"
              />
            </div>
          </div>
          <div class="col-lg-3 col-12 d-flex justify-content-center">
            <div>
              <SelectField
                v-model="perPage"
                id="perPage"
                label="Perms per page"
                :options="perPageOptions"
              />
            </div>
          </div>
        </div>
      </div>
    </template>
  </ViewContainer>
</template>

<script setup>
import { computed, ref, watchEffect } from 'vue'
import { useRoute } from 'vue-router'

import { APIs } from '@/apis'
import ViewContainer from '@/views/ViewContainer.vue'
import DataTable from '@/components/DataTable.vue'
import InputField from '@/components/InputField.vue'
import SelectField from '@/components/SelectField.vue'
import MyButton from '@/components/MyButton.vue'
import Pagination from '@/components/Pagination.vue'
import Action from '@/components/Action.vue'
import { isUserAuthorized } from '@/composables/auth-manager'
import { fetchData } from '@/composables/data-fetcher'
import { getDataTableInfo } from '@/composables/get-datatable-info'
import EditPermissionModal from './EditPermissionModal.vue'
import DeletePermissionModal from './DeletePermissionModal.vue'
import CreatePermissionModal from './CreatePermissionModal.vue'

const columns = [
  { label: 'Id', field: 'id', key: true, wrapper: 'text-center', sortable: true },
  { label: 'Permission', field: 'name', wrapper: 'text-center', sortable: true },
  {
    label: 'Roles',
    field: 'role_count',
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

const route = useRoute()
const routeQuery = route.query

const dataset = ref([])
const isDataLoading = ref(true)
const searchQuery = ref('')
const sortBy = ref('created_at')
const sortOrder = ref('desc')
const sortOptions = columns.filter((col) => col.sortable)
const currentPage = ref(1)
const perPage = ref(10)
const perPageOptions = [
  { label: '10', field: 10 },
  { label: '25', field: 25 },
  { label: '50', field: 50 },
  { label: '100', field: 100 }
]
const rolesFilter = ref(routeQuery.roles ? routeQuery.roles.split(',') : [])
const rolesFilterOptions = ref([])
const total = ref(0)
const filtered = ref(0)
const dataActions = ref([])
const dataActionModals = [EditPermissionModal, DeletePermissionModal]

function toggleSortOrder() {
  sortOrder.value = sortOrder.value == 'desc' ? 'asc' : 'desc'
}

function changePage(nextPage) {
  currentPage.value = nextPage
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

async function getPermissions() {
  isDataLoading.value = true
  dataActions.value = []
  try {
    const params = {
      query: searchQuery.value,
      roles: rolesFilter.value,
      page: currentPage.value,
      limit: perPage.value,
      sort_by: sortBy.value,
      sort_order: sortOrder.value
    }
    const response = await fetchData(APIs.permissionList.url, true, params)
    const permissions = response.data
    permissions.forEach((permission) => {
      permission.role_count = renderRoles(permission)
      setDataActions(permission)
    })
    dataset.value = permissions
    total.value = response.pagination.total
    filtered.value = response.pagination.filtered
  } finally {
    isDataLoading.value = false
  }
}

const dataInfo = computed(() =>
  getDataTableInfo(
    dataset.value.length,
    perPage.value,
    currentPage.value,
    total.value,
    filtered.value,
    'permissions'
  )
)

watchEffect(() => getPermissions())

const canCreatePermission = isUserAuthorized(APIs.permissionCreate.permission)
const isActionsEnabled = ref(false)
function setDataActions(permission) {
  const actions = []
  if (isUserAuthorized(APIs.permissionEdit.permission)) {
    actions.push({
      name: 'Edit',
      type: 'modal',
      modalId: 'edit-permission',
      icon: 'pen',
      class: 'text-primary'
    })
  }
  if (isUserAuthorized(APIs.permissionDelete.permission)) {
    actions.push({
      name: 'Delete',
      type: 'modal',
      modalId: 'delete-permission',
      icon: 'trash-can',
      class: 'text-danger'
    })
  }
  if (actions.length > 0) isActionsEnabled.value = true
  dataActions.value.push({ id: permission.id, actions: actions })
}

function renderRoles(permission) {
  return {
    type: 'route',
    routeLink: {
      name: 'role-list',
      query: { perms: permission.id }
    },
    name: permission.roles.length,
    class: 'btn btn-link btn-rounded'
  }
}
</script>

<style scoped></style>
