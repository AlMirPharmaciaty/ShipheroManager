import { APIs } from '@/apis'
import MainLayout from '@/layouts/MainLayout.vue'

export default {
  path: '/inventory-snapshot',
  name: 'inventory-snapshot',
  meta: {
    title: 'Inventory Snapshots',
    icon: 'boxes-stacked',
    layout: MainLayout,
    displayOnNav: true,
    authRequired: true,
    permission: APIs.inventorySnapshotList.permission
  },
  component: () => import('@/views/inventory-snapshot/InventorySnapshotList.vue')
}
