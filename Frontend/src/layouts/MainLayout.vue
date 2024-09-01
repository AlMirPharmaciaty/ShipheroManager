<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-brand fixed-top">
    <div class="container-fluid">
      <MyButton id="sidenav-collapse" icon="bars fa-xl" color="brand" class="shadow-0 px-3" />
      <RouterLink
        :to="{ name: 'dashboard' }"
        class="navbar-brand me-auto ms-3"
        text="Shiphero Manager"
      />
      <div class="collapse navbar-collapse justify-content-end">
        <Dropdown :custom-trigger="true">
          <template v-slot:trigger>
            <Image
              data-mdb-dropdown-init
              role="button"
              :image="`${APIs.userAvatarURL}/${user.avatar}`"
              :delay="0"
              width="40"
              height="40"
              class="border border-2 rounded-circle"
            />
          </template>
          <template v-slot:dropdownItems>
            <li>
              <Action
                :route-link="profileRoute.path"
                class="dropdown-item"
                :icon="profileRoute.meta.icon"
                :name="profileRoute.meta.title"
                type="route"
              />
            </li>
            <li>
              <Action
                :button-func="logOutUser"
                class="dropdown-item"
                icon="arrow-right-from-bracket fa-regular"
                name="Logout"
                type="button"
              />
            </li>
          </template>
        </Dropdown>
      </div>
    </div>
  </nav>
  <SideNav
    content-id="dashboard"
    toggler-id="sidenav-collapse"
    @logout-event="logOutUser"
    :profile-route="profileRoute"
  />
  <main id="dashboard" class="bg-secondary bg-opacity-10">
    <div class="container my-5">
      <slot />
    </div>
  </main>
</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router'

import SideNav from '@/components/SideNav.vue'
import MyButton from '@/components/MyButton.vue'
import Dropdown from '@/components/Dropdown.vue'
import Action from '@/components/Action.vue'
import Image from '@/components/Image.vue'
import { APIs } from '@/apis'
import { getUser, logOutUser } from '@/composables/auth-manager'

const router = useRouter()
const user = getUser()
const profileRoute = router.getRoutes().find((r) => r.name == 'profile')
</script>

<style>
html,
body,
#app {
  height: 100%;
  overflow: hidden;
}

.navbar {
  z-index: 11;
}

#sidenav .sidenav-menu:first-child {
  margin-top: 4.5rem;
}

main {
  height: 100%;
  overflow-y: auto;
}

main .container,
main .container-fluid {
  margin-top: 6rem !important;
}
</style>
