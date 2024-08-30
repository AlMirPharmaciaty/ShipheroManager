<template>
  <Modal
    id="avatar-selector"
    size="lg"
    footer-action-btn-text="Select"
    footer-close-btn-text="Cancel"
    :show-header-close-btn="true"
    :header-visible="true"
    @modal-action-event="$emit('onAvatarSelection', selectedAvatar)"
    :func-on-modal-open="getAvatars"
  >
    <template v-slot:header>Select Avatar</template>
    <template v-slot:body>
      <div class="d-flex flex-wrap gap-3 justify-content-center" v-if="avatars">
        <template v-for="avatar in avatars" :key="avatar">
          <div
            role="button"
            class="position-relative border border-3 rounded-circle"
            :class="[avatar == selectedAvatar ? 'border-success' : '']"
            @click="changeAvatar(avatar)"
          >
            <Image class="avatar rounded-circle" :image="`${APIs.userAvatarURL}/${avatar}`" />
          </div>
        </template>
      </div>
    </template>
  </Modal>
</template>

<script setup>
import { ref } from 'vue'

import { APIs } from '@/apis'
import Modal from '@/components/Modal.vue'
import Image from '@/components/Image.vue'
import { fetchData } from '@/composables/data-fetcher'

const props = defineProps({
  user: {}
})

const avatars = ref()
const selectedAvatar = ref(props.user.avatar)
const avatarsRetrieved = ref(false)

function changeAvatar(avatar) {
  selectedAvatar.value = avatar
}

async function getAvatars() {
  if (!avatarsRetrieved.value) {
    avatars.value = await fetchData(
      APIs.avatarGet.url,
      true,
      null,
      null,
      null,
      APIs.avatarGet.method
    )
    avatarsRetrieved.value = true
  }
}
</script>

<style scoped>
.avatar {
  width: 80px;
  height: 80px;
}

@media (max-width: 575.98px) {
  .avatar {
    width: 70px;
    height: 70px;
  }
}
</style>
