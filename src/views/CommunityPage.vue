<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api/client'

interface Post { id: string; user: string; avatar: string; subject: string; content: string; time: string; likes: number }
interface Group { name: string; online: number }
interface Leader { name: string; hours: number }

const posts = ref<Post[]>([])
const groups = ref<Group[]>([])
const leaders = ref<Leader[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await api.get('/stats/community')
    posts.value = data.posts
    groups.value = data.groups
    leaders.value = data.leaderboard
  } catch { /* fallback to empty */ }
  finally { loading.value = false }
})
</script>

<template>
  <div class="p-8 space-y-6">
    <div>
      <p class="eyebrow-mono-sm mb-2">学友社区</p>
      <h1 class="text-display-sm text-ink">社区</h1>
    </div>

    <div v-if="loading" class="text-mute text-sm py-12 text-center">加载中...</div>
    <template v-else>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Feed -->
        <div class="lg:col-span-2 space-y-4">
          <div v-for="post in posts" :key="post.id" class="card-xai">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-8 h-8 rounded-full bg-canvas-soft border border-hairline flex items-center justify-center text-xs text-ink font-mono">
                {{ post.avatar }}
              </div>
              <div>
                <span class="text-ink text-sm font-normal">{{ post.user }}</span>
                <span class="text-mute text-xs ml-2">{{ post.time }}</span>
              </div>
              <span class="ml-auto text-xs px-2 py-0.5 rounded-full border border-hairline text-mute font-mono uppercase">{{ post.subject }}</span>
            </div>
            <p class="text-body text-sm leading-relaxed">{{ post.content }}</p>
            <div class="flex items-center gap-4 mt-4 pt-3 border-t border-hairline">
              <button class="text-mute text-xs hover:text-ink transition-colors">{{ post.likes }} 赞</button>
              <button class="text-mute text-xs hover:text-ink transition-colors">回复</button>
            </div>
          </div>
        </div>

        <!-- Side Panel -->
        <div class="space-y-4">
          <div class="card-xai">
            <p class="eyebrow-mono-sm text-mute mb-4">学习小组</p>
            <div v-for="g in groups" :key="g.name" class="flex items-center justify-between py-2 border-b border-hairline last:border-b-0">
              <span class="text-body text-sm">{{ g.name }}</span>
              <span class="text-mute text-xs">{{ g.online }} 人在线</span>
            </div>
            <button class="btn-pill-outline mt-4 w-full text-sm">加入小组</button>
          </div>
          <div class="card-xai">
            <p class="eyebrow-mono-sm text-mute mb-4">排行榜</p>
            <div v-for="(l, i) in leaders" :key="l.name" class="flex items-center gap-3 py-2 border-b border-hairline last:border-b-0">
              <span class="text-xs text-mute font-mono w-4">{{ i + 1 }}</span>
              <div class="w-6 h-6 rounded-full bg-canvas-soft border border-hairline" />
              <span class="text-body text-sm">{{ l.name }}</span>
              <span class="ml-auto text-mute text-xs">{{ l.hours }} 小时</span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
