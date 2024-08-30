<template>
  <div
    ref="modalRef"
    class="modal top fade"
    :id="id"
    data-mdb-backdrop="true"
    data-mdb-keyboard="false"
  >
    <div
      class="modal-dialog modal-dialog-centered modal-dialog-scrollable"
      :class="[size ? `modal-${size}` : '', scrollable ? 'modal-dialog-scrollable' : '']"
    >
      <div class="modal-content">
        <div class="modal-header" v-if="headerVisible" :class="headerClass">
          <h5 class="modal-title">
            <slot name="header"></slot>
          </h5>
          <button
            v-if="showHeaderCloseBtn"
            type="button"
            class="btn-close"
            data-mdb-dismiss="modal"
            :disabled="footerActionBtnDisabled"
          ></button>
        </div>
        <div class="modal-body" v-if="bodyVisible" :class="bodyClass">
          <slot name="body"></slot>
        </div>
        <div class="modal-footer" v-if="footerVisible" :class="footerClass">
          <slot name="footer">
            <MyButton
              :color="footerCloseBtnColor"
              :text="footerCloseBtnText"
              data-mdb-dismiss="modal"
              :disabled="footerActionBtnDisabled"
            />
            <MyButton
              @click="$emit('modalActionEvent')"
              :color="footerActionBtnColor"
              :text="footerActionBtnText"
              :disabled="footerActionBtnDisabled"
              :is-loading="footerActionBtnLoading"
            />
          </slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import MyButton from '@/components/MyButton.vue'
import { onMounted, ref } from 'vue'
const props = defineProps({
  id: {},
  size: {},
  scrollable: {},
  headerVisible: { default: true, type: Boolean },
  headerClass: {},
  bodyVisible: { default: true, type: Boolean },
  bodyClass: {},
  footerVisible: { default: true, type: Boolean },
  footerClass: {},
  footerActionBtnText: { default: 'Okay' },
  footerActionBtnColor: { default: 'brand' },
  footerActionBtnDisabled: { default: false, type: Boolean },
  footerActionBtnLoading: { default: false, type: Boolean },
  footerCloseBtnText: { default: 'Close' },
  footerCloseBtnColor: { default: 'secondary' },
  showHeaderCloseBtn: { default: true, type: Boolean },
  funcOnModalOpen: {}
})

const modalRef = ref()
onMounted(() => {
  if (props.funcOnModalOpen) {
    modalRef.value.addEventListener('show.mdb.modal', props.funcOnModalOpen)
  }
})
</script>

<style scoped></style>
