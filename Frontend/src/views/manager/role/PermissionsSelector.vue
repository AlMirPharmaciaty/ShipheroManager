<template>
  <SelectField
    v-model="rolePermissions"
    :container="`#${modalId}`"
    :id="id"
    label="Permissions"
    :multiple="true"
    size="lg"
    :options="permissionOptions"
    :disabled="isLoading"
    :searchable="true"
    :search-function="getPermissions"
    :displayed-labels="2"
    options-selected-label="permissions selected"
  />
</template>

<script setup>
import { ref } from 'vue'

import { APIs } from '@/apis'
import SelectField from '@/components/SelectField.vue'
import { fetchData } from '@/composables/data-fetcher'

const rolePermissions = defineModel()
defineProps({
  modalId: {},
  id: {},
  isLoading: { default: false, type: Boolean }
})

const permissionOptions = ref([])

function getPermissions(query = '', perms = '', page = 1) {
  const params = { query: query, perms: perms, page: page }
  fetchData(APIs.permissionList.url, true, params).then((response) => {
    response.data.forEach((perm) => {
      if (!permissionOptions.value.find((p) => p.field == perm.id)) {
        permissionOptions.value.push({ label: perm.name, field: perm.id })
      }
    })
    if (
      response.pagination.total != permissionOptions.value.length &&
      response.pagination.filtered > response.data.length
    ) {
      getPermissions(query, perms, page + 1)
    }
  })
}

if (rolePermissions.value.length > 0) {
  getPermissions('', rolePermissions.value.join(','))
  if (!(rolePermissions.value.length >= 10)) {
    getPermissions()
  }
} else {
  getPermissions()
}
</script>

<style scoped></style>
