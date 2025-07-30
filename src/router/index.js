import { createRouter, createWebHistory } from 'vue-router'

import Dashboard from '@/components/Dashboard.vue'
import History from '@/components/History.vue'
import ChatDetail from '@/components/ChatDetail.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/history',
    name: 'History',
    component: History
  },
  {
    path: '/history/ChatDetail',
    name: 'ChatDetail',
    component: ChatDetail
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes,
})

import { createApp } from 'vue'
import App from '../App.vue'

const app = createApp(App)
app.use(router)
app.mount('#app')

export default router