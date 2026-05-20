<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'
import api from '@/api/client'

const auth = useAuthStore()

const nickname = ref('')
const email = ref('')
const saving = ref(false)

onMounted(() => {
  if (auth.user) {
    nickname.value = auth.user.nickname
    email.value = auth.user.email
  }
})

const saveProfile = async () => {
  saving.value = true
  try {
    const { data } = await api.put('/users/me', { nickname: nickname.value })
    auth.user = data
    localStorage.setItem('user', JSON.stringify(data))
    useUiStore().addToast('个人信息已保存', 'success')
  } catch {
    useUiStore().addToast('保存失败，请稍后重试', 'error')
  } finally {
    saving.value = false
  }
}

</script>

<template>
  <div class="p-8 space-y-6">
    <div>
      <p class="eyebrow-mono-sm mb-2">个人偏好</p>
      <h1 class="text-display-sm text-ink">设置</h1>
    </div>

    <div class="max-w-[600px] space-y-6">
      <!-- Profile -->
      <div class="card-xai space-y-4">
        <p class="eyebrow-mono-sm text-mute mb-2">个人信息</p>

        <!-- Avatar -->
        <div class="flex items-center gap-4 mb-2">
          <div class="w-16 h-16 rounded-full bg-canvas-soft border border-hairline flex items-center justify-center text-2xl text-mute font-normal">
            {{ nickname.value?.[0] || '?' }}
          </div>
          <div>
            <p class="text-ink text-sm font-normal">{{ nickname.value }}</p>
            <p class="text-mute text-xs">{{ email.value }}</p>
          </div>
        </div>

        <div>
          <label class="block text-body text-sm mb-2">显示名称</label>
          <input
            v-model="nickname"
            type="text"
            placeholder="你的昵称"
            class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink transition-colors"
          />
        </div>
        <div>
          <label class="block text-body text-sm mb-2">邮箱</label>
          <input
            v-model="email"
            type="email"
            disabled
            class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-mute text-sm opacity-60 cursor-not-allowed"
          />
          <p class="text-mute text-xs mt-1">邮箱暂不支持修改</p>
        </div>
        <button class="btn-pill-filled cursor-target text-sm px-6 py-2.5" :disabled="saving" @click="saveProfile">
          {{ saving ? '保存中...' : '保存个人信息' }}
        </button>
      </div>

    </div>
  </div>
</template>
