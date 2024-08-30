<template>
  <nav
    data-mdb-sidenav-init
    id="sidenav"
    class="sidenav text-bg-dark"
    data-mdb-mode="side"
    data-mdb-slim="true"
    :data-mdb-slim-collapsed="sideNavCollapsed"
    :data-mdb-content="`#${contentId}`"
    data-scroll-container=".sidenav-menu-scrollable"
    data-mdb-color="success"
    data-mdb-slim-width="64"
  >
    <ul class="sidenav-menu sidenav-menu-scrollable">
      <template v-for="route in routes" :key="route.path">
        <li class="sidenav-item my-1" v-if="canUserViewRoute(route)">
          <RouterLink
            v-if="route.components"
            :to="route.path"
            active-class="active text-bg-brand"
            class="sidenav-link fs-6"
          >
            <i :class="`fa-fw fa-regular fa-${route.meta.icon}`"></i>
            <span data-mdb-slim="false" class="ms-3">{{ route.meta.title }}</span>
          </RouterLink>
          <a v-else class="sidenav-link fs-6">
            <i :class="`fa-fw fa-regular fa-${route.meta.icon}`"></i>
            <span data-mdb-slim="false" class="ms-3">{{ route.meta.title }}</span>
          </a>
          <ul v-if="route.children.length > 0" class="sidenav-collapse">
            <template v-for="childRoute in route.children" :key="childRoute.meta.title">
              <li v-if="canUserViewRoute(childRoute)" class="sidenav-item my-1">
                <RouterLink
                  :to="`${route.path}/${childRoute.path}`"
                  active-class="active text-bg-brand"
                  class="sidenav-link fs-6"
                >
                  <i :class="`fa-fw fa-regular fa-${childRoute.meta.icon}`"></i>
                  <span data-mdb-slim="false" class="ms-3">{{ childRoute.meta.title }}</span>
                </RouterLink>
              </li>
            </template>
          </ul>
        </li>
      </template>
    </ul>
    <div class="text-center">
      <hr class="my-2" />
    </div>
    <ul class="sidenav-menu">
      <li class="sidenav-item">
        <RouterLink
          :to="profileRoute.path"
          active-class="active text-bg-brand"
          class="sidenav-link fs-6"
        >
          <i :class="`fa-fw fa-regular fa-${profileRoute.meta.icon}`"></i>
          <span data-mdb-slim="false" class="ms-3" v-text="profileRoute.meta.title"></span>
        </RouterLink>
      </li>
      <li class="sidenav-item" id="slim-toggler">
        <a class="sidenav-link fs-6" @click="$emit('logoutEvent')">
          <i class="fa-fw fa-regular fa-arrow-right-from-bracket"></i>
          <span data-mdb-slim="false" class="ms-3">Log out</span>
        </a>
      </li>
    </ul>
  </nav>
</template>

<script setup>
import { isUserAuthorized } from '@/composables/auth-manager'
import { onMounted, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

const router = useRouter()
const routes = router
  .getRoutes()
  .filter((r) => r.meta.authRequired && r.meta.displayOnNav && isUserAuthorized(r.meta.permission))

const props = defineProps({
  contentId: {},
  togglerId: {},
  profileRoute: {}
})

function canUserViewRoute(route) {
  return isUserAuthorized(route.meta.permission)
}

const sideNavCollapsed = ref(JSON.parse(localStorage.getItem('sideNavCollapsed')) ?? true)

onMounted(() => {
  const sidenav = mdb.Sidenav.getOrCreateInstance(document.getElementById('sidenav'))
  sidenav.show()

  document.getElementById(props.togglerId).addEventListener('click', () => {
    if (window.innerWidth < 768) {
      sidenav.toggle()
      if (sideNavCollapsed.value) {
        sidenav.toggleSlim()
        sideNavCollapsed.value = false
      }
    } else {
      sidenav.toggleSlim()
      sideNavCollapsed.value = !sideNavCollapsed.value
    }
    localStorage.setItem('sideNavCollapsed', sideNavCollapsed.value)
  })

  function handleSidenavOnWindowResize() {
    if (window.innerWidth < 768) {
      sidenav.changeMode('over')
      sidenav.hide()
    } else {
      sidenav.changeMode('side')
      sidenav.show()
    }
  }

  handleSidenavOnWindowResize()
  window.addEventListener('resize', handleSidenavOnWindowResize)
})
</script>

<style>
.sidenav {
  z-index: 10;
}

.sidenav-link.router-link-exact-active i {
  color: #fff !important;
}

.sidenav-collapse .sidenav-link {
  font-size: var(--mdb-sidenav-link-font-size);
  height: var(--mdb-sidenav-link-height);
}

.sidenav-slim .fas.fa-angle-down {
  display: none !important;
}

.sidenav-link i {
  transition: all 0.3s ease-in-out;
}

.sidenav-slim .sidenav-link {
  justify-content: center;
  padding: 0;
}

.sidenav-backdrop {
  z-index: 9;
}
</style>
