import { createRouter, createWebHistory } from 'vue-router'
import CreativeView from '../views/CreativeView.vue'
import PerformanceView from '../views/PerformanceView.vue'
import AudienceView from '../views/AudienceView.vue'
import AdManagementView from '../views/AdManagementView.vue'

const routes = [
  { path: '/creatives', component: CreativeView },
  { path: '/performance', component: PerformanceView },
  { path: '/audience', component: AudienceView },
  { path: '/ads', component: AdManagementView },
  { path: '/', redirect: '/creatives' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router