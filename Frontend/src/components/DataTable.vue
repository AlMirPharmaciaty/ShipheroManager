<template>
  <div class="table-responsive">
    <table class="table align-middle text-nowrap table-sm mb-0 table-hover">
      <thead class="text-center">
        <tr>
          <th v-if="actionsEnabled">Actions</th>
          <th
            :class="col.headWrapper"
            v-for="(col, colIndex) in filteredColumns"
            :key="colIndex"
            v-html="col.label"
          ></th>
        </tr>
        <tr>
          <th :colspan="columnsCount" class="border-0 p-0">
            <div class="table-loader">
              <span class="table-loader-inner" v-show="isDataLoading">
                <span class="table-progress bg-brand"></span>
              </span>
            </div>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="dataset.length == 0 && isDataLoading">
          <td :colspan="columnsCount" class="text-center">Loading data...</td>
        </tr>
        <tr v-if="dataset.length == 0 && !isDataLoading">
          <td :colspan="columnsCount" class="text-center">No data.</td>
        </tr>
        <tr v-for="(row, rowIndex) in dataset" :key="rowIndex">
          <td v-if="actionsEnabled" class="text-center">
            <Dropdown
              class="position-static"
              text="actions"
              size="sm"
              color="light"
              :items="actions"
              @click="getActions(row)"
              animation="off"
            />
          </td>
          <td v-for="(col, colIndex) in filteredColumns" :key="colIndex">
            <div :class="col.wrapper" v-if="col.type == 'component'">
              <component :is="col.component" v-bind="row[col.field]"></component>
            </div>
            <div :class="col.wrapper" v-else-if="col.type == 'component-list'">
              <template v-for="(props, index) in row[col.field]" :key="index">
                <component :is="col.component" v-bind="props"></component>
              </template>
            </div>
            <div :class="col.wrapper" v-else-if="col.type == 'html'" v-html="row[col.field]"></div>
            <div :class="col.wrapper" v-else-if="col.type == 'datetime'">
              {{ get_timelapse(row[col.field], false) }}
            </div>
            <div :class="col.wrapper" v-else-if="col.type == 'bool'">
              <span v-if="row[col.field]" :class="[col.reverse ? 'text-danger' : 'text-success']">
                <i
                  class="fa-duotone fa-solid fa-xl"
                  :class="[col.reverse ? 'fa-circle-xmark' : 'fa-circle-check']"
                ></i>
              </span>
              <span v-else :class="[col.reverse ? 'text-success' : 'text-danger']">
                <i
                  class="fa-duotone fa-solid fa-xl"
                  :class="[col.reverse ? 'fa-circle-check' : 'fa-circle-xmark']"
                ></i>
              </span>
            </div>
            <div :class="col.wrapper" v-else v-text="row[col.field]"></div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <template v-for="(modal, index) in dataActionModals" :key="index">
    <component :is="modal" v-bind="modalData"></component>
  </template>
</template>

<script setup>
import { computed, ref, shallowRef } from 'vue'

import Dropdown from '@/components/Dropdown.vue'
import Action from '@/components/Action.vue'
import { get_timelapse } from '@/composables/utils'

const props = defineProps({
  columns: { type: Array },
  dataset: { type: Array },
  isDataLoading: { default: true, type: Boolean },
  actionsEnabled: { default: false, type: Boolean },
  dataActions: { type: Array },
  dataActionModals: { type: Array },
  dataTableFunc: { type: Function }
})

const filteredColumns = computed(() => {
  return props.columns.filter((col) => col.display != false)
})

const columnsCount = computed(() => {
  return filteredColumns.value.length + (props.actionsEnabled ? 1 : 0)
})

const actions = shallowRef([])
const modalData = ref()

function getActions(row) {
  actions.value = []
  modalData.value = { data: row, isComingFromDataTable: true, dataTableFunc: props.dataTableFunc }
  const key = props.columns.filter((col) => col.key == true)[0].field
  const dataActions = props.dataActions.filter((i) => i.id == row[key])[0].actions
  dataActions.forEach((action) => {
    actions.value.push({ component: Action, props: { ...action } })
  })
}
</script>

<style scoped>
.table-loader {
  width: 100%;
  height: 2px;
  position: relative;
  overflow: hidden;
}

.table-loader-inner {
  display: block;
  height: 100%;
}

.table-progress {
  animation: datatableProgress 1.5s ease-in-out;
  animation-fill-mode: both;
  animation-iteration-count: infinite;
  width: 45%;
  position: relative;
  opacity: 0.5;
  border-radius: 1px;
  display: block;
  height: 100%;
}

@keyframes datatableProgress {
  0% {
    left: -45%;
  }

  100% {
    left: 100%;
  }
}
</style>
