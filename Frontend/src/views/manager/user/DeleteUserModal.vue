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
    :header-visible="true"
    :footer-action-btn-disabled="isDeletingUser"
    :footer-action-btn-loading="isDeletingUser"
    @modal-action-event="deleteUser"
  >
    <template v-slot:header>
      <span>Delete User</span>
    </template>
    <template v-slot:body v-if="data">
      <div class="text-center">
        <div class="mb-3">
          <img class="mb-2" :src="`${APIs.userAvatarURL}/${data.avatar}`" width="50" height="50" />
          <h6 class="card-title" v-text="data.username"></h6>
          <h6 class="card-subtitle text-muted small" v-text="data.email"></h6>
        </div>
        <p class="mb-0 fs-5 text-center text-danger fw-medium">Are you sure?</p>
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

const modalId = 'delete-user'
const isDeletingUser = ref(false)
const router = useRouter()

async function deleteUser() {
  isDeletingUser.value = true
  changeModalBackdrop(modalId, 'static')
  try {
    const params = { user_id: props.data.id }
    const response = await fetchData(
      APIs.userDelete.url,
      true,
      params,
      null,
      null,
      APIs.userDelete.method
    )
    notify(response.message)
    setTimeout(() => {
      hideModal(modalId)
      if (props.isComingFromDataTable) {
        props.dataTableFunc()
      } else {
        router.push({ name: 'user-list' })
      }
    }, 1000)
  } finally {
    setTimeout(() => {
      isDeletingUser.value = false
    }, 1000)
  }
}
</script>

<style scoped></style>
