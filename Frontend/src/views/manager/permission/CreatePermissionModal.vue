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
    @modal-action-event="createPermission"
  >
    <template v-slot:header>
      <span>Create a new permission</span>
    </template>
    <template v-slot:body>
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import Modal from '@/components/Modal.vue'
import { fetchData } from '@/composables/data-fetcher'
import { changeModalBackdrop, hideModal, notify } from '@/composables/bootstrap-utils'
import InputField from '@/components/InputField.vue'
import { APIs } from '@/apis'

const props = defineProps({
  isComingFromDataTable: { default: false, type: Boolean },
  dataTableFunc: { type: Function }
})

const modalId = 'create-permission'
const isLoading = ref(false)
const router = useRouter()
const permissionName = ref()

async function createPermission() {
  isLoading.value = true
  changeModalBackdrop(modalId, 'static')
  try {
    const data = { name: permissionName.value }
    const response = await fetchData(
      APIs.permissionCreate.url,
      true,
      null,
      data,
      'json',
      APIs.permissionCreate.method
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
