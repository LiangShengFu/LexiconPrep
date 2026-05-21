<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUiStore } from '@/stores/ui'
import api from '@/api/client'

const stats = ref({ users: 0, questions: 0, answers: 0, subjects: {} as Record<string, number> })
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await api.get('/admin/stats')
    stats.value = data
  } catch { /* */ }
  finally { loading.value = false }
})
</script>

<template>
  <div class="p-8 space-y-6">
    <div>
      <p class="eyebrow-mono-sm mb-2">管理员</p>
      <h1 class="text-display-sm text-ink">系统概览</h1>
    </div>

    <div v-if="loading" class="text-mute text-sm py-8">加载中...</div>
    <template v-else>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="card-xai"><span class="text-mute text-xs">用户总数</span><div class="text-display-sm text-ink mt-2">{{ stats.users }}</div></div>
        <div class="card-xai"><span class="text-mute text-xs">题目总数</span><div class="text-display-sm text-ink mt-2">{{ stats.questions }}</div></div>
        <div class="card-xai"><span class="text-mute text-xs">答题总数</span><div class="text-display-sm text-ink mt-2">{{ stats.answers }}</div></div>
      </div>

      <div class="card-xai">
        <p class="eyebrow-mono-sm text-mute mb-4">科目分布</p>
        <div class="space-y-2">
          <div v-for="(count, subject) in stats.subjects" :key="subject" class="flex items-center justify-between py-2 border-b border-hairline last:border-b-0">
            <span class="text-body text-sm">{{ subject }}</span>
            <span class="text-mute text-sm">{{ count }} 题</span>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
