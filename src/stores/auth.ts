import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/client'

export interface User {
  id: string
  email: string
  nickname: string
  avatar: string | null
  streak_days: number
  total_knowledge_points: number
  created_at: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)

  function initFromStorage() {
    const token = localStorage.getItem('access_token')
    const refresh = localStorage.getItem('refresh_token')
    const userStr = localStorage.getItem('user')
    if (token && userStr) {
      accessToken.value = token
      refreshToken.value = refresh
      try {
        user.value = JSON.parse(userStr)
      } catch {
        logout()
      }
    }
  }

  async function login(email: string, password: string) {
    loading.value = true
    try {
      const { data } = await api.post('/auth/login', { email, password })
      accessToken.value = data.access_token
      refreshToken.value = data.refresh_token
      user.value = data.user
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      return data
    } finally {
      loading.value = false
    }
  }

  async function register(email: string, password: string, nickname: string) {
    loading.value = true
    try {
      const { data } = await api.post('/auth/register', { email, password, nickname })
      accessToken.value = data.access_token
      refreshToken.value = data.refresh_token
      user.value = data.user
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      return data
    } finally {
      loading.value = false
    }
  }

  function logout() {
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  }

  return { user, accessToken, refreshToken, loading, isAuthenticated, initFromStorage, login, register, logout }
})
