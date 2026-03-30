import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/auth/login',
    name: 'Login',
    component: () => import('../views/auth/LoginView.vue')
  },
  {
    path: '/auth/register',
    name: 'Register',
    component: () => import('../views/auth/RegisterView.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/ProfileView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/pets',
    name: 'PetList',
    component: () => import('../views/pets/PetListView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/pets/:id',
    name: 'PetDetail',
    component: () => import('../views/pets/PetDetailView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/pets/:id/edit',
    name: 'PetEdit',
    component: () => import('../views/pets/PetEditView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/pets/:id/predictions',
    name: 'PetPredictions',
    component: () => import('../views/pets/PetPredictionsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/assistant',
    name: 'Assistant',
    component: () => import('../views/AssistantView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/reminders',
    name: 'ReminderList',
    component: () => import('../views/ReminderListView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !token) {
    next('/auth/login')
  } else {
    next()
  }
})

export default router