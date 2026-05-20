<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api/client'

interface User { id: string; email: string; nickname: string; role: string; streak_days: number; total_knowledge_points: number; created_at: string }

const users = ref<User[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await api.get('/admin/users')
    users.value = data
  } catch { /* */ }
  finally { loading.value = false }
})

const toggleRole = async (user: User) => {
  const newRole = user.role === 'admin' ? 'user' : 'admin'
  await api.put(`/admin/users/${user.id}/role`, { role: newRole })
  user.role = newRole
}
</script>

<template>
  <div class="p-8 space-y-6">
    <div>
      <p class="eyebrow-mono-sm mb-2">管理</p>
      <h1 class="text-display-sm text-ink">用户管理</h1>
    </div>

    <div v-if="loading" class="text-mute text-sm py-8">加载中...</div>
    <div v-else class="space-y-2">
      <div v-for="u in users" :key="u.id" class="card-xai flex items-center justify-between gap-4">
        <div>
          <span class="text-ink text-sm">{{ u.nickname }}</span>
          <span class="text-mute text-sm ml-3">{{ u.email }}</span>
        </div>
        <div class="flex items-center gap-3">
          <span class="text-mute text-xs">打卡 {{ u.streak_days }} 天</span>
          <span class="text-xs px-2 py-0.5 rounded-full border text-xs"
            :class="u.role === 'admin' ? 'border-accent-sunset/30 text-accent-sunset' : 'border-hairline text-mute'">
            {{ u.role === 'admin' ? '管理员' : '用户' }}
          </span>
          <button class="btn-pill-outline text-xs" @click="toggleRole(u)">切换角色</button>
        </div>
      </div>
      <div v-if="!users.length" class="card-xai text-center py-8 text-mute text-sm">暂无用户</div>
    </div>
  </div>
</template>
