<template>
  <ViewContainer>
    <template v-slot:body>
      <div v-if="user" class="row row-gap-4 row-cols-lg-2 row-cols-1">
        <div class="col">
          <div class="card">
            <div class="card-header text-muted">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <span class="small" id="user-id">{{ data.id }}</span>
                  <CopyButton target="#user-id" class="ms-2" />
                </div>
                <div>
                  <span v-if="data.deleted" class="text-danger">
                    <i class="fa-duotone fa-solid fa-circle-xmark fa-xl"></i>
                  </span>
                  <span v-else class="text-success">
                    <i class="fa-duotone fa-solid fa-circle-check fa-xl"></i>
                  </span>
                </div>
              </div>
            </div>
            <div class="card-body">
              <div class="text-center mb-4">
                <Image
                  class="mb-3 rounded-circle"
                  :image="`${APIs.userAvatarURL}/${data.avatar}`"
                  width="100"
                  height="100"
                />
                <h5 class="card-title">{{ data.username }}</h5>
                <h6 class="card-subtitle text-muted">{{ data.email }}</h6>
              </div>
              <div class="row row-cols-2 row-gap-3 align-items-center">
                <div class="col small fw-medium">Created at</div>
                <div class="col small">{{ format_date(data.created_at, false, false, true) }}</div>
                <div class="col small fw-medium">Updated at</div>
                <div class="col small">{{ format_date(data.updated_at, false, false, true) }}</div>
                <div class="col small fw-medium" v-if="data.roles">Roles</div>
                <div class="col">
                  <div class="d-flex flex-wrap gap">
                    <span
                      v-for="role in data.roles"
                      :key="role.id"
                      class="fs-6 fw-normal badge badge-primary"
                      >{{ role.name }}</span
                    >
                    <span v-if="data.roles.length == 0">-</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col">
          <div class="card">
            <div class="card-header text-muted small">Update Account</div>
            <div class="card-body">
              <form @submit.prevent="updateProfile">
                <div class="d-flex flex-column gap-4">
                  <div>
                    <Action
                      type="modal"
                      modal-id="avatar-selector"
                      name="Change avatar"
                      class="btn btn-lg btn-outline-secondary"
                      icon="circle-user"
                      icon-type="regular"
                    />
                    <component
                      :is="AvatarSelectorModal"
                      @on-avatar-selection="changeAvatar"
                      :user="user"
                    ></component>
                  </div>
                  <div>
                    <InputField
                      id="username"
                      type="text"
                      label="Username"
                      size="lg"
                      v-model="data.username"
                      autocomplete="off"
                    />
                  </div>

                  <div>
                    <InputField
                      id="email"
                      type="email"
                      label="Email"
                      size="lg"
                      v-model="data.email"
                      autocomplete="off"
                    />
                  </div>

                  <div class="d-flex gap-2">
                    <InputField
                      id="password"
                      type="password"
                      label="New Password"
                      size="lg"
                      v-model="password"
                      autocomplete="off"
                      :disabled="isPasswordDiabled"
                    />
                    <MyButton
                      v-if="isPasswordDiabled"
                      icon="pen"
                      color="outline-secondary"
                      size="lg"
                      @click-event="isPasswordDiabled = false"
                    />
                  </div>

                  <MyButton
                    type="submit"
                    text="Save changes"
                    color="brand"
                    size="lg"
                    :disabled="isSaveDisabled || isLoading"
                    :is-loading="isLoading"
                  />
                </div>
              </form>
            </div>
          </div>

          <div class="card mt-3">
            <div class="card-header text-muted small">Delete Account</div>
            <div class="card-body">
              <Action
                type="modal"
                modal-id="delete-account"
                name="Delete Account"
                class="btn btn-lg btn-danger"
              />
              <Modal
                id="delete-account"
                size="sm"
                footer-action-btn-color="danger"
                footer-action-btn-text="Yes, Delete"
                footer-close-btn-text="Cancel"
                footer-close-btn-color="brand"
                header-class="border-0 mx-auto pb-0"
                footer-class="border-0 mx-auto pt-0"
                :show-header-close-btn="false"
                :header-visible="false"
                :footer-action-btn-disabled="isDeletingAccount"
                :footer-action-btn-loading="isDeletingAccount"
                @modal-action-event="deleteAccount"
              >
                <template v-slot:header>Delete Account</template>
                <template v-slot:body>
                  <div class="text-center">
                    <p class="fs-5 fw-medium text-danger">Are you sure?</p>
                    <Alert color="danger">
                      <div class="d-flex flex-column gap-3">
                        <span><i class="fa-solid fa-solid fa-circle-exclamation fa-2x"></i></span>
                        <span class="fs-6">This action is irreversible.</span>
                      </div>
                    </Alert>
                  </div>
                </template>
              </Modal>
            </div>
          </div>
        </div>
      </div>
    </template>
  </ViewContainer>
</template>

<script setup>
import { computed, ref } from 'vue'

import { APIs } from '@/apis'
import ViewContainer from './ViewContainer.vue'
import AvatarSelectorModal from './AvatarSelectorModal.vue'
import CopyButton from '@/components/CopyButton.vue'
import InputField from '@/components/InputField.vue'
import MyButton from '@/components/MyButton.vue'
import Action from '@/components/Action.vue'
import Modal from '@/components/Modal.vue'
import Alert from '@/components/Alert.vue'
import Image from '@/components/Image.vue'
import { getUser, logOutUser, saveUser } from '@/composables/auth-manager'
import { format_date } from '@/composables/utils'
import { fetchData } from '@/composables/data-fetcher'
import { hideModal, notify } from '@/composables/bootstrap-utils'

const user = ref(getUser())
const data = ref({ ...user.value })
const password = ref()
const isPasswordDiabled = ref(true)
const isLoading = ref(false)
const isSaveDisabled = computed(() => {
  var changesMade = false
  if (
    data.value.username != user.value.username ||
    data.value.email != user.value.email ||
    data.value.avatar != user.value.avatar
  ) {
    changesMade = true
  } else {
    changesMade = false
  }
  if (password.value) changesMade = true
  if (changesMade) return false
  return true
})

function changeAvatar(avatar) {
  data.value.avatar = avatar
  hideModal('avatar-selector')
}

async function updateProfile() {
  isLoading.value = true
  try {
    const changes = {}
    if (data.value.avatar) changes['avatar'] = data.value.avatar
    if (data.value.username) changes['username'] = data.value.username
    if (data.value.email) changes['email'] = data.value.email
    if (password.value) changes['password'] = password.value
    if (changes && !isSaveDisabled.value) {
      const response = await fetchData(
        APIs.accountUpdate.url,
        true,
        null,
        changes,
        'json',
        APIs.accountUpdate.method
      )
      user.value = response.data
      saveUser(user.value)
      notify(response.message)
      document
        .querySelector('.navbar .dropdown img')
        .setAttribute('src', `${APIs.userAvatarURL}/${data.value.avatar}`)
    }
  } finally {
    password.value = null
    isPasswordDiabled.value = true
    isLoading.value = false
  }
}

const isDeletingAccount = ref(false)

async function deleteAccount() {
  isDeletingAccount.value = true
  try {
    const response = await fetchData(
      APIs.accountDelete.url,
      true,
      null,
      null,
      null,
      APIs.accountDelete.method
    )
    notify(response.message)
    setTimeout(() => {
      hideModal('delete-account')
      logOutUser()
    }, 1000)
  } finally {
    isDeletingAccount.value = false
  }
}
</script>

<style scoped></style>
