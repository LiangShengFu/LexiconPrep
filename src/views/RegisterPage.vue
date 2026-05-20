<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const nickname = ref('')
const email = ref('')
const password = ref('')
const error = ref('')

const parseError = (e: any): string => {
  const detail = e.response?.data?.detail
  if (!detail) return '注册失败，请稍后重试'
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    const msgs = detail.map((d: any) => d.msg || '').filter(Boolean)
    return msgs.join('；') || '输入格式有误'
  }
  return '注册失败，请稍后重试'
}

const handleRegister = async () => {
  error.value = ''
  if (!nickname.value.trim()) {
    error.value = '请输入昵称'
    return
  }
  if (!email.value.includes('@')) {
    error.value = '请输入有效的邮箱地址'
    return
  }
  if (password.value.length < 6) {
    error.value = '密码至少 6 位'
    return
  }
  try {
    await auth.register(email.value, password.value, nickname.value)
    router.push('/profile')
  } catch (e: any) {
    error.value = parseError(e)
  }
}
</script>

<template>
  <div class="min-h-screen bg-canvas pt-14 flex items-center justify-center">
    <div class="w-full max-w-[400px] px-6">
      <p class="eyebrow-mono mb-6 text-center">LexiconPrep</p>
      <h1 class="text-display-sm text-ink mb-8 text-center">创建你的账号。</h1>

      <div class="card-xai space-y-5">
        <div v-if="error" class="text-red-400 text-sm text-center bg-red-400/10 rounded-card py-3 px-4">
          {{ error }}
        </div>
        <div>
          <label class="block text-body text-sm mb-2">昵称</label>
          <input
            v-model="nickname"
            type="text"
            placeholder="请输入昵称"
            class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink transition-colors"
          />
        </div>
        <div>
          <label class="block text-body text-sm mb-2">邮箱</label>
          <input
            v-model="email"
            type="email"
            placeholder="请输入邮箱地址"
            class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink transition-colors"
          />
        </div>
        <div>
          <label class="block text-body text-sm mb-2">密码</label>
          <input
            v-model="password"
            type="password"
            placeholder="至少6位字符"
            class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink transition-colors"
            @keyup.enter="handleRegister"
          />
        </div>
        <button
          class="btn-pill-filled w-full text-base py-3"
          :disabled="auth.loading"
          @click="handleRegister"
        >
          {{ auth.loading ? '注册中...' : '注册' }}
        </button>
      </div>

      <p class="text-mute text-sm text-center mt-6">
        已有账号？
        <button class="text-ink hover:text-body transition-colors" @click="router.push('/login')">立即登录</button>
      </p>
    </div>
  </div>
</template>
