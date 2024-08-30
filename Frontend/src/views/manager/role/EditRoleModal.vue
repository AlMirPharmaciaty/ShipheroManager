<template>
  <Modal
    :id="modalId"
    size="sm"
    footer-action-btn-color="brand"
    footer-action-btn-text="Update"
    footer-close-btn-text="Cancel"
    :show-header-close-btn="false"
    :header-visible="true"
    :footer-action-btn-disabled="isLoading"
    :footer-action-btn-loading="isLoading"
    @modal-action-event="editRole"
  >
    <template v-slot:header>
      <span>Edit role</span>
    </template>
    <template v-slot:body v-if="role">
      <div class="mb-4">
        <InputField
          v-model="role.name"
          label="Role Name"
          id="name"
          size="lg"
          :readonly="isLoading"
          autocomplete="off"
          :required="true"
        />
      </div>

      <div>
        <PermissionsSelector
          id="permissions-edit"
          v-model="role.permissions"
          :is-loading="isLoading"
          :modal-id="modalId"
        />
      </div>
    </template>
  </Modal>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import { APIs } from '@/apis'
import Modal from '@/components/Modal.vue'
import { fetchData } from '@/composables/data-fetcher'
import { changeModalBackdrop, hideModal, notify } from '@/composables/bootstrap-utils'
import InputField from '@/components/InputField.vue'
import PermissionsSelector from './PermissionsSelector.vue'

const props = defineProps({
  data: {},
  isComingFromDataTable: { default: false, type: Boolean },
  dataTableFunc: { type: Function }
})

const modalId = 'edit-role'
const isLoading = ref(false)
const router = useRouter()
const role = ref()

watch(
  () => props.data,
  (newVal) => {
    role.value = { ...newVal }
    role.value.permissions = role.value.permissions.map((perm) => perm.id)
  }
)

async function editRole() {
  isLoading.value = true
  changeModalBackdrop(modalId, 'static')
  try {
    const params = { role_id: props.data.id }
    const data = { name: role.value.name, permissions: role.value.permissions }
    const response = await fetchData(
      APIs.roleEdit.url,
      true,
      params,
      data,
      'json',
      APIs.roleEdit.method
    )
    notify(response.message)
    setTimeout(() => {
      role.value = {}
      hideModal(modalId)
      if (props.isComingFromDataTable) {
        props.dataTableFunc()
      } else {
        router.push({ name: 'role-list' })
      }
    }, 1000)
  } finally {
    setTimeout(() => {
      isLoading.value = false
    }, 1000)
  }
}
</script>

<style scoped></style>
