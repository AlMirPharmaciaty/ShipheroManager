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
      <div v-if="data" class="row row-gap-4 row-cols-lg-2 row-cols-1">
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
                <img
                  class="mb-3"
                  :src="`${APIs.userAvatarURL}/${data.avatar}`"
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
            <div class="card-header fw-bold">Actions</div>
            <div class="card-body d-flex flex-row flex-wrap gap-2">
              <template
                v-if="
                  isUserAuthorized(APIs.userEdit.permission) ||
                  isUserAuthorized(APIs.userDelete.permission)
                "
              >
                <Action
                  v-if="isUserAuthorized(APIs.userEdit.permission)"
                  name="Edit User"
                  :route-link="{ name: 'edit-user' }"
                  type="route"
                  class="btn btn-brand btn-lg"
                  icon="pen"
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
              </template>
              <span v-else>You can't take any action.</span>
            </div>
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
import { ref } from 'vue'
import { useRoute } from 'vue-router'

import { APIs } from '@/apis'
import ViewContainer from '@/views/ViewContainer.vue'
import Alert from '@/components/Alert.vue'
import Action from '@/components/Action.vue'
import CopyButton from '@/components/CopyButton.vue'
import { isUserAuthorized } from '@/composables/auth-manager'
import { fetchData } from '@/composables/data-fetcher'
import { format_date } from '@/composables/utils'
import DeleteUserModal from '@/views/manager/user/DeleteUserModal.vue'

const route = useRoute()
const data = ref()
const isDataLoading = ref(true)

async function getUser() {
  isDataLoading.value = true
  try {
    const response = await fetchData(APIs.userGet.url, true, route.params)
    data.value = response.data
  } finally {
    isDataLoading.value = false
  }
}

getUser()
</script>

<style scoped></style>
