<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api/client'

interface Post { id: string; user_id: string; content: string; subject: string | null; likes: number; created_at: string; user_nickname: string | null; user_avatar_letters: string | null }
interface Leader { name: string; hours: number }

const posts = ref<Post[]>([])
const leaders = ref<Leader[]>([])
const newContent = ref('')
const newSubject = ref('')
const posting = ref(false)
const loading = ref(true)

const load = async () => {
  try {
    const [p, l] = await Promise.all([
      api.get('/community/posts'),
      api.get('/community/leaderboard'),
    ])
    posts.value = p.data
    leaders.value = l.data
  } catch { /* */ }
  finally { loading.value = false }
}

onMounted(load)

const createPost = async () => {
  if (!newContent.value.trim()) return
  posting.value = true
  try {
    await api.post('/community/posts', { content: newContent.value, subject: newSubject.value || null })
    newContent.value = ''
    newSubject.value = ''
    await load()
  } catch { /* */ }
  finally { posting.value = false }
}

const likePost = async (post: Post) => {
  await api.post(`/community/posts/${post.id}/like`)
  post.likes++
}

const timeAgo = (dateStr: string) => {
  const diff = Date.now() - new Date(dateStr).getTime()
  const hours = Math.floor(diff / 3600000)
  if (hours < 1) return '刚刚'
  if (hours < 24) return `${hours} 小时前`
  return `${Math.floor(hours / 24)} 天前`
}
</script>

<template>
  <div class="p-8 space-y-6">
    <div>
      <p class="eyebrow-mono-sm mb-2">学友社区</p>
      <h1 class="text-display-sm text-ink">社区</h1>
    </div>

    <div v-if="loading" class="text-mute text-sm py-8">加载中...</div>
    <template v-else>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 space-y-4">
          <!-- New Post -->
          <div class="card-xai space-y-3">
            <textarea v-model="newContent" placeholder="分享你的学习心得..." rows="2"
              class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink resize-none" />
            <div class="flex items-center justify-between">
              <input v-model="newSubject" placeholder="标签（如：考研经验）" class="bg-canvas-soft border border-hairline rounded-card px-3 py-1.5 text-ink text-xs placeholder:text-mute focus:outline-none focus:border-ink w-40" />
              <button class="btn-pill-filled text-sm" :disabled="posting || !newContent.trim()" @click="createPost">
                {{ posting ? '发布中...' : '发布' }}
              </button>
            </div>
          </div>

          <!-- Feed -->
          <div v-if="!posts.length" class="card-xai text-center py-12 text-mute text-sm">
            暂无动态，发布第一条吧
          </div>
          <div v-for="post in posts" :key="post.id" class="card-xai">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-8 h-8 rounded-full bg-canvas-soft border border-hairline flex items-center justify-center text-xs text-ink font-mono">
                {{ post.user_avatar_letters }}
              </div>
              <div>
                <span class="text-ink text-sm font-normal">{{ post.user_nickname }}</span>
                <span class="text-mute text-xs ml-2">{{ timeAgo(post.created_at) }}</span>
              </div>
              <span v-if="post.subject" class="ml-auto text-xs px-2 py-0.5 rounded-full border border-hairline text-mute font-mono uppercase">{{ post.subject }}</span>
            </div>
            <p class="text-body text-sm leading-relaxed">{{ post.content }}</p>
            <div class="flex items-center gap-4 mt-4 pt-3 border-t border-hairline">
              <button class="text-mute text-xs hover:text-ink transition-colors" @click="likePost(post)">{{ post.likes }} 赞</button>
            </div>
          </div>
        </div>

        <!-- Side Panel -->
        <div class="space-y-4">
          <div class="card-xai">
            <p class="eyebrow-mono-sm text-mute mb-4">排行榜（本周）</p>
            <div v-for="(l, i) in leaders" :key="l.name" class="flex items-center gap-3 py-2 border-b border-hairline last:border-b-0">
              <span class="text-xs text-mute font-mono w-4">{{ i + 1 }}</span>
              <div class="w-6 h-6 rounded-full bg-canvas-soft border border-hairline" />
              <span class="text-body text-sm">{{ l.name }}</span>
              <span class="ml-auto text-mute text-xs">{{ l.hours }} 题</span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
