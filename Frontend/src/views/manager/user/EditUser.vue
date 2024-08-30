<template>
  <ViewContainer>
    <template v-slot:actions>
      <div class="d-flex gap-2 flex-wrap">
        <Action
          name="Back"
          type="route"
          :route-link="{ name: 'user-list' }"
          icon="arrow-left"
          class="btn btn-light shadow-0"
        />
      </div>
    </template>

    <template v-slot:body>
      <div v-if="data" class="row row-cols-lg-2 row-cols-1 row-gap-4">
        <div class="col">
          <form @submit.prevent="updateData" class="card card-body">
            <div class="d-flex flex-column gap-4">
              <div class="d-flex gap-3 align-items-center">
                <img :src="`${APIs.userAvatarURL}/${data.avatar}`" width="60" height="60" />

                <Action
                  type="modal"
                  modal-id="avatar-selector"
                  name="Change avatar"
                  class="btn btn-outline-secondary"
                  icon="circle-user"
                  icon-type="regular"
                />
                <component
                  :is="AvatarSelectorModal"
                  @on-avatar-selection="changeAvatar"
                  :user="data"
                ></component>
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
                  id="password"
                  type="text"
                  label="Password"
                  size="lg"
                  v-model="data.password"
                  autocomplete="off"
                />
              </div>

              <div>
                <SelectField
                  id="roles"
                  label="Roles"
                  size="lg"
                  :multiple="true"
                  :options="rolesOptions"
                  v-model="data.roles"
                  :searchable="true"
                  :search-function="getRoles"
                />
              </div>

              <div v-once v-if="data.deleted">
                <ToggleSwitch id="deleted" label="Deleted" v-model="data.deleted" />
              </div>
            </div>

            <div class="d-flex gap-2 flex-wrap mt-4">
              <MyButton
                type="submit"
                text="Save changes"
                color="brand"
                size="lg"
                :disabled="isUpdatingUser"
                :is-loading="isUpdatingUser"
              />
              <template v-if="isUserAuthorized(APIs.userDelete.permission)">
                <Action
                  name="Delete User"
                  type="modal"
                  class="btn btn-danger btn-lg"
                  icon="trash-can"
                  modal-id="delete-user"
                />
                <component :is="DeleteUserModal" :data="data"></component>
              </template>
            </div>
          </form>
        </div>

        <div class="col">
          <div class="card card-body text-bg-white rounded-7">
            <code v-html="formattedData"></code>
          </div>
        </div>
      </div>

      <div v-else-if="!data && isDataLoading" class="d-flex justify-content-center">
        <div class="spinner-border text-brand" role="status"></div>
      </div>

      <Alert v-else color="danger">
        <i class="fa-regular fa-circle-xmark me-2 fa-fw fa-xl"></i>
        <span>User with id "{{ Object.values(route.params)[0] }}" not found.</span>
      </Alert>
    </template>
  </ViewContainer>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { APIs } from '@/apis'
import ViewContainer from '@/views/ViewContainer.vue'
import InputField from '@/components/InputField.vue'
import MyButton from '@/components/MyButton.vue'
import SelectField from '@/components/SelectField.vue'
import ToggleSwitch from '@/components/ToggleSwitch.vue'
import Alert from '@/components/Alert.vue'
import Action from '@/components/Action.vue'
import { isUserAuthorized } from '@/composables/auth-manager'
import { fetchData } from '@/composables/data-fetcher'
import { hideModal, notify } from '@/composables/bootstrap-utils'
import DeleteUserModal from '@/views/manager/user/DeleteUserModal.vue'
import AvatarSelectorModal from '@/views/AvatarSelectorModal.vue'

const route = useRoute()
const data = ref()
const isDataLoading = ref(true)
const isUpdatingUser = ref(false)
const rolesOptions = ref([])

const formattedData = computed(() =>
  data.value ? JSON.stringify(data.value).split(',').join('<br>') : ''
)

watch(data, () => {
  if (data.value) {
    getRoles()
    data.value.roles = data.value.roles.map((role) => role.id)
  }
})

async function getUser() {
  isDataLoading.value = true
  try {
    const response = await fetchData(APIs.userGet.url, true, route.params)
    if (response.data) {
      data.value = response.data
      getRoles('', data.value.roles.map((role) => role.id).join(','))
    }
  } finally {
    isDataLoading.value = false
  }
}

getUser()

function changeAvatar(avatar) {
  data.value.avatar = avatar
  hideModal('avatar-selector')
}

async function updateData() {
  isUpdatingUser.value = true
  try {
    const updateData = {
      avatar: data.value.avatar,
      username: data.value.username,
      email: data.value.email,
      password: data.value.password,
      roles: data.value.roles,
      deleted: data.value.deleted
    }
    const response = await fetchData(
      APIs.userEdit.url,
      true,
      route.params,
      updateData,
      'json',
      APIs.userEdit.method
    )
    data.value = response.data
    notify(response.message)
  } finally {
    isUpdatingUser.value = false
  }
}

function getRoles(query = '', roles = '') {
  fetchData(APIs.roleList.url, true, { query: query, roles: roles }).then((response) => {
    response.data.forEach((role) => {
      if (!rolesOptions.value.find((p) => p.field == role.id)) {
        rolesOptions.value.push({ label: role.name, field: role.id })
      }
    })
  })
}
</script>

<style scoped></style>
