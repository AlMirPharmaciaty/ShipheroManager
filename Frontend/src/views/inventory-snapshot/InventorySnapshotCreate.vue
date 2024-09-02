<template>
  <Modal
    :id="modalId"
    footer-action-btn-color="brand"
    footer-action-btn-text="Generate"
    footer-close-btn-text="Cancel"
    :show-header-close-btn="false"
    :header-visible="true"
    :footer-action-btn-disabled="isLoading"
    :footer-action-btn-loading="isLoading"
    @modal-action-event="generateInventorySnapshot"
    :func-on-modal-open="showModalContent"
  >
    <template v-slot:header>
      <span>Generate a new inventory snapshot</span>
    </template>
    <template v-slot:body v-if="isModalShown">
      <div class="mb-4">
        <InputField
          v-model="snapshot.warehouse_id"
          label="Warehouse Id"
          id="warehouse-id"
          size="lg"
          :readonly="isLoading"
          autocomplete="off"
          :autofocus="true"
          :required="true"
        />
      </div>

      <div class="mb-4">
        <InputField
          v-model="snapshot.customer_account_id"
          label="Customer Account Id"
          id="customer-account-id"
          size="lg"
          :readonly="isLoading"
          autocomplete="off"
          :autofocus="true"
          :required="true"
        />
      </div>

      <div class="mb-4">
        <SelectField
          v-model="snapshot.has_inventory"
          label="Has Inventory"
          id="has-inventory"
          size="lg"
          :options="[
            { label: 'Any', field: null },
            { label: 'Yes', field: true },
            { label: 'No', field: false }
          ]"
          :disabled="isLoading"
        />
      </div>

      <div>
        <DatePicker
          v-model="snapshot.updated_from"
          label="Updated From"
          id="updated-from"
          size="lg"
          :readonly="isLoading"
          :disable-future="true"
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
import SelectField from '@/components/SelectField.vue'
import DatePicker from '@/components/DatePicker.vue'
import { fetchData } from '@/composables/data-fetcher'
import { changeModalBackdrop, hideModal, notify } from '@/composables/bootstrap-utils'

const props = defineProps({
  isComingFromDataTable: { default: false, type: Boolean },
  dataTableFunc: { type: Function }
})

const modalId = 'create-inventory-snapshot'
const isLoading = ref(false)
const router = useRouter()
const snapshot = ref({
  warehouse_id: null,
  customer_account_id: null,
  has_inventory: null,
  updated_from: null
})
const isModalShown = ref(false)

function showModalContent() {
  isModalShown.value = true
}

async function generateInventorySnapshot() {
  isLoading.value = true
  changeModalBackdrop(modalId, 'static')
  try {
    const data = {
      warehouse_id: snapshot.value.warehouse_id,
      customer_account_id: snapshot.value.customer_account_id,
      has_inventory: snapshot.value.has_inventory,
      updated_from: snapshot.value.updated_from
    }
    const response = await fetchData(
      APIs.inventorySnapshotCreate.url,
      true,
      null,
      data,
      'json',
      APIs.inventorySnapshotCreate.method
    )
    notify(response.message)
    setTimeout(() => {
      snapshot.value = {}
      hideModal(modalId)
      if (props.isComingFromDataTable) {
        props.dataTableFunc()
      } else {
        router.push({ name: 'inventory-snapshot' })
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
