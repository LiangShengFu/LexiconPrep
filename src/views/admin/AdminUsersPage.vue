<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUiStore } from '@/stores/ui'
import api from '@/api/client'

interface User { id: string; email: string; nickname: string; avatar: string | null; role: string; streak_days: number; total_knowledge_points: number; created_at: string }

const users = ref<User[]>([])
const loading = ref(true)
const expandedId = ref<string | null>(null)

onMounted(async () => {
  try {
    const { data } = await api.get('/admin/users')
    users.value = data
  } catch {
    useUiStore().addToast('加载用户列表失败', 'error')
  } finally { loading.value = false }
})

const toggleExpand = (id: string) => {
  expandedId.value = expandedId.value === id ? null : id
}

const toggleRole = async (user: User) => {
  const newRole = user.role === 'admin' ? 'user' : 'admin'
  try {
    await api.put(`/admin/users/${user.id}/role`, { role: newRole })
    user.role = newRole
    useUiStore().addToast(`已将 ${user.nickname} 角色切换为 ${newRole === 'admin' ? '管理员' : '普通用户'}`, 'success')
  } catch {
    useUiStore().addToast('角色切换失败', 'error')
  }
}

const resetPassword = async (user: User) => {
  const pw = prompt(`请输入 ${user.nickname} (${user.email}) 的新密码（至少8位，含大小写字母和数字）：`)
  if (!pw) return
  if (pw.length < 8 || !/[a-z]/.test(pw) || !/[A-Z]/.test(pw) || !/[0-9]/.test(pw)) {
    useUiStore().addToast('密码必须至少8位，包含大小写字母和数字', 'error')
    return
  }
  try {
    await api.put(`/admin/users/${user.id}/password`, { new_password: pw })
    useUiStore().addToast(`${user.nickname} 的密码已重置`, 'success')
  } catch {
    useUiStore().addToast('密码重置失败', 'error')
  }
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
      <div v-for="u in users" :key="u.id">
        <div class="card-xai flex items-center justify-between gap-4 cursor-pointer" @click="toggleExpand(u.id)">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-canvas-soft border border-hairline flex items-center justify-center overflow-hidden shrink-0">
              <img v-if="u.avatar" :src="u.avatar" class="w-full h-full object-cover" />
              <span v-else class="text-mute text-xs font-mono">{{ u.nickname?.charAt(0) || '?' }}</span>
            </div>
            <div>
              <span class="text-ink text-sm">{{ u.nickname }}</span>
              <span class="text-mute text-sm ml-3">{{ u.email }}</span>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <span class="text-mute text-xs">打卡 {{ u.streak_days }} 天</span>
            <span class="text-xs px-2 py-0.5 rounded-full border text-xs"
              :class="u.role === 'admin' ? 'border-accent-sunset/30 text-accent-sunset' : 'border-hairline text-mute'">
              {{ u.role === 'admin' ? '管理员' : '用户' }}
            </span>
            <button class="btn-pill-outline cursor-target text-xs" @click.stop="toggleRole(u)">切换角色</button>
          </div>
        </div>
        <!-- expanded detail -->
        <div v-if="expandedId === u.id" class="card-xai mt-1 space-y-3">
          <div class="grid grid-cols-2 gap-3 text-sm">
            <div>
              <span class="text-mute text-xs">用户 ID</span>
              <p class="text-ink font-mono text-xs mt-0.5">{{ u.id }}</p>
            </div>
            <div>
              <span class="text-mute text-xs">注册时间</span>
              <p class="text-ink text-xs mt-0.5">{{ new Date(u.created_at).toLocaleString('zh-CN') }}</p>
            </div>
            <div>
              <span class="text-mute text-xs">邮箱</span>
              <p class="text-ink text-xs mt-0.5">{{ u.email }}</p>
            </div>
            <div>
              <span class="text-mute text-xs">昵称</span>
              <p class="text-ink text-xs mt-0.5">{{ u.nickname }}</p>
            </div>
            <div>
              <span class="text-mute text-xs">角色</span>
              <p class="text-ink text-xs mt-0.5">{{ u.role === 'admin' ? '管理员' : '普通用户' }}</p>
            </div>
            <div>
              <span class="text-mute text-xs">积分</span>
              <p class="text-ink text-xs mt-0.5">{{ u.total_knowledge_points }}</p>
            </div>
            <div>
              <span class="text-mute text-xs">连续打卡</span>
              <p class="text-ink text-xs mt-0.5">{{ u.streak_days }} 天</p>
            </div>
            <div>
              <span class="text-mute text-xs">头像</span>
              <div class="mt-1">
                <img v-if="u.avatar" :src="u.avatar" class="w-16 h-16 rounded-card border border-hairline object-cover" />
                <span v-else class="text-mute text-xs">未设置</span>
              </div>
            </div>
          </div>
          <div class="border-t border-hairline pt-3">
            <button class="btn-pill-outline cursor-target text-xs border-amber-500/30 text-amber-400 hover:border-amber-500" @click="resetPassword(u)">重置密码</button>
            <span class="text-mute text-xs ml-3">密码已加密存储，只能重置不能查看</span>
          </div>
        </div>
      </div>
      <div v-if="!users.length" class="card-xai text-center py-8 text-mute text-sm">暂无用户</div>
    </div>
  </div>
</template>
