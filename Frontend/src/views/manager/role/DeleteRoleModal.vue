<template>
  <Modal
    :id="modalId"
    size="sm"
    footer-action-btn-color="danger"
    footer-action-btn-text="Yes, Delete"
    footer-close-btn-text="Cancel"
    footer-close-btn-color="brand"
    header-class="border-0 mx-auto pb-0"
    footer-class="border-0 mx-auto pt-0"
    :show-header-close-btn="false"
    :header-visible="false"
    :footer-action-btn-disabled="isLoading"
    :footer-action-btn-loading="isLoading"
    @modal-action-event="deleteRole"
  >
    <!-- <template v-slot:header>
      <span>Delete Role</span>
    </template> -->
    <template v-slot:body v-if="data">
      <div class="text-center">
        <p class="mb-0 fs-5 text-center text-danger fw-medium">
          <span>Are you sure you want to delete the role</span>
          <span class="fs-6 fw-normal badge badge-primary mx-1">{{ data.name }}</span>
          <span>?</span>
        </p>
      </div>
    </template>
  </Modal>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { APIs } from '@/apis'
import Modal from '@/components/Modal.vue'
import { fetchData } from '@/composables/data-fetcher'
import { changeModalBackdrop, hideModal, notify } from '@/composables/bootstrap-utils'

const props = defineProps({
  data: {},
  isComingFromDataTable: { default: false, type: Boolean },
  dataTableFunc: { type: Function }
})

const modalId = 'delete-role'
const isLoading = ref(false)
const router = useRouter()

async function deleteRole() {
  isLoading.value = true
  changeModalBackdrop(modalId, 'static')
  try {
    const params = { role_id: props.data.id }
    const response = await fetchData(
      APIs.roleDelete.url,
      true,
      params,
      null,
      null,
      APIs.roleDelete.method
    )
    notify(response.message)
    setTimeout(() => {
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
