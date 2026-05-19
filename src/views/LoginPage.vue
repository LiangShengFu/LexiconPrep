<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const email = ref('')
const password = ref('')
const error = ref('')

const handleLogin = async () => {
  error.value = ''
  try {
    await auth.login(email.value, password.value)
    router.push('/dashboard')
  } catch (e: any) {
    error.value = e.response?.data?.detail || '登录失败，请检查邮箱和密码'
  }
}
</script>

<template>
  <div class="min-h-screen bg-canvas pt-14 flex items-center justify-center">
    <div class="w-full max-w-[400px] px-6">
      <p class="eyebrow-mono mb-6 text-center">LexiconPrep</p>
      <h1 class="text-display-sm text-ink mb-8 text-center">登录你的账号。</h1>

      <div class="card-xai space-y-5">
        <div v-if="error" class="text-red-400 text-sm text-center bg-red-400/10 rounded-card py-3 px-4">
          {{ error }}
        </div>
        <div>
          <label class="block text-body text-sm mb-2">邮箱</label>
          <input
            v-model="email"
            type="email"
            placeholder="请输入邮箱地址"
            class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink transition-colors"
            @keyup.enter="handleLogin"
          />
        </div>
        <div>
          <label class="block text-body text-sm mb-2">密码</label>
          <input
            v-model="password"
            type="password"
            placeholder="请输入密码"
            class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink transition-colors"
            @keyup.enter="handleLogin"
          />
        </div>
        <button
          class="btn-pill-filled w-full text-base py-3"
          :disabled="auth.loading"
          @click="handleLogin"
        >
          {{ auth.loading ? '登录中...' : '登录' }}
        </button>
      </div>

      <p class="text-mute text-sm text-center mt-6">
        还没有账号？
        <button class="text-ink hover:text-body transition-colors" @click="router.push('/register')">
          立即注册
        </button>
      </p>

      <p class="text-mute text-xs text-center mt-4">
        测试账号: test@lexiconprep.com / test123
      </p>
    </div>
  </div>
</template>
