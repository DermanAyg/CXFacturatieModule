import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import TabsPage from '../views/tabs/Tabs.vue'
import login from '../views/login/login.vue'
import registreer from '../views/registreer/registreer.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login/',
    component: login,
  },
  {
    path: '/registreer/',
    component: registreer,
  },
  {
    path: '/tabs/',
    component: TabsPage,
    children: [
      {
        path: '',
        redirect: '/tabs/home'
      },
      {
        path: 'Settings',
        component: () => import('@/views/tabs/settings.vue')
      },
      {
        path: 'historie',
        component: () => import('@/views/tabs/historie.vue')
      },
      {
        path: 'home',
        component: () => import('@/views/tabs/home.vue')
      },
      {
        path: 'facturen',
        component: () => import('@/views/tabs/facturen.vue')
      },
      {
        path: 'profiel',
        component: () => import('@/views/tabs/profiel.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
