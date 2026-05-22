import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'landing', component: () => import('@/views/LandingPage.vue') },
    { path: '/login', name: 'login', component: () => import('@/views/LoginPage.vue') },
    { path: '/register', name: 'register', component: () => import('@/views/RegisterPage.vue') },
    { path: '/dashboard', redirect: '/profile' },
    { path: '/settings', redirect: '/profile' },
    { path: '/profile', name: 'profile', component: () => import('@/views/ProfilePage.vue'), meta: { requiresAuth: true } },
    { path: '/library', name: 'library', component: () => import('@/views/LibraryPage.vue'), meta: { requiresAuth: true } },
    { path: '/exam', name: 'exam', component: () => import('@/views/ExamPage.vue'), meta: { requiresAuth: true } },
    { path: '/flashcards', name: 'flashcards', component: () => import('@/views/FlashcardsPage.vue'), meta: { requiresAuth: true } },
    { path: '/progress', name: 'progress', component: () => import('@/views/ProgressPage.vue'), meta: { requiresAuth: true } },
    { path: '/pomodoro', name: 'pomodoro', component: () => import('@/views/PomodoroPage.vue') },
    { path: '/community', name: 'community', component: () => import('@/views/CommunityPage.vue'), meta: { requiresAuth: true } },
    { path: '/admin', name: 'adminOverview', component: () => import('@/views/admin/AdminOverviewPage.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/admin/questions', name: 'adminQuestions', component: () => import('@/views/admin/AdminQuestionsPage.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/admin/users', name: 'adminUsers', component: () => import('@/views/admin/AdminUsersPage.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: '/:pathMatch(.*)*', name: 'notFound', component: () => import('@/views/NotFoundPage.vue') },
  ],
})

function isTokenExpired(token: string): boolean {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.exp * 1000 < Date.now()
  } catch {
    return true
  }
}

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('access_token')

  if (to.meta.requiresAuth) {
    if (!token || isTokenExpired(token)) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      next('/login')
      return
    }
  }

  if (to.meta.requiresAdmin) {
    const userStr = localStorage.getItem('user')
    if (!userStr) { next('/profile'); return }
    try {
      if (JSON.parse(userStr).role !== 'admin') { next('/profile'); return }
    } catch { next('/profile'); return }
  }

  next()
})

export default router
