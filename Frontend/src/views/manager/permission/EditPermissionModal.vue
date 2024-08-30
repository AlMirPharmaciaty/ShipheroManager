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
    @modal-action-event="editPermission"
  >
    <template v-slot:header>
      <span>Edit Permission</span>
    </template>
    <template v-slot:body v-if="data">
      <InputField
        v-model="permissionName"
        label="Permission Name"
        id="name"
        :readonly="isLoading"
        autocomplete="off"
        :autofocus="true"
        :required="true"
      />
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

const props = defineProps({
  data: { default: '' },
  isComingFromDataTable: { default: false, type: Boolean },
  dataTableFunc: { type: Function }
})

const modalId = 'edit-permission'
const isLoading = ref(false)
const router = useRouter()
const permissionName = ref()

watch(
  () => props.data,
  (newVal) => {
    permissionName.value = newVal.name
  }
)

async function editPermission() {
  isLoading.value = true
  changeModalBackdrop(modalId, 'static')
  try {
    const params = { permission_id: props.data.id }
    const data = { name: permissionName.value }
    const response = await fetchData(
      APIs.permissionEdit.url,
      true,
      params,
      data,
      'json',
      APIs.permissionEdit.method
    )
    notify(response.message)
    setTimeout(() => {
      permissionName.value = ''
      hideModal(modalId)
      if (props.isComingFromDataTable) {
        props.dataTableFunc()
      } else {
        router.push({ name: 'permission-list' })
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
