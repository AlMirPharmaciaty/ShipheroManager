<template>
  <Modal
    :id="modalId"
    size="sm"
    footer-action-btn-color="brand"
    footer-action-btn-text="Create"
    footer-close-btn-text="Cancel"
    :show-header-close-btn="false"
    :header-visible="true"
    :footer-action-btn-disabled="isLoading"
    :footer-action-btn-loading="isLoading"
    @modal-action-event="createRole"
    :func-on-modal-open="showModalContent"
  >
    <template v-slot:header>
      <span>Create a new role</span>
    </template>
    <template v-slot:body v-if="isModalShown">
      <div class="mb-4">
        <InputField
          v-model="role.name"
          label="Role Name"
          id="name"
          size="lg"
          :readonly="isLoading"
          autocomplete="off"
          :autofocus="true"
          :required="true"
        />
      </div>

      <div>
        <PermissionsSelector
          id="permissions-add"
          v-model="role.permissions"
          :is-loading="isLoading"
          :modal-id="modalId"
        />
      </div>
    </template>
  </Modal>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { APIs } from '@/apis'
import Modal from '@/components/Modal.vue'
import InputField from '@/components/InputField.vue'
import { fetchData } from '@/composables/data-fetcher'
import { changeModalBackdrop, hideModal, notify } from '@/composables/bootstrap-utils'
import PermissionsSelector from './PermissionsSelector.vue'

const props = defineProps({
  isComingFromDataTable: { default: false, type: Boolean },
  dataTableFunc: { type: Function }
})

const modalId = 'create-role'
const isLoading = ref(false)
const router = useRouter()
const role = ref({ name: null, permissions: [] })
const isModalShown = ref(false)

function showModalContent() {
  isModalShown.value = true
}

async function createRole() {
  isLoading.value = true
  changeModalBackdrop(modalId, 'static')
  try {
    const data = { name: role.value.name, permissions: role.value.permissions }
    const response = await fetchData(
      APIs.roleCreate.url,
      true,
      null,
      data,
      'json',
      APIs.roleCreate.method
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
