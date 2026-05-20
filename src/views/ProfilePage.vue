<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Chart, registerables } from 'chart.js'
import api from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

Chart.register(...registerables)

const auth = useAuthStore()
const ui = useUiStore()

// ─── Stats ───
const overview = ref({ streak_days: 0, total_knowledge_points: 0, total_questions_answered: 0, average_accuracy: 0, total_study_minutes: 0 })
const trend = ref({ labels: [] as string[], values: [] as number[] })
const progress = ref({ subjects: {} as Record<string, number> })
const recentMistakes = ref<{ question_subject: string; wrong_count: number; question_content: string }[]>([])
const progressChart = ref<HTMLCanvasElement | null>(null)
const radarChart = ref<HTMLCanvasElement | null>(null)

const kpiCards = ref([
  { label: '连续打卡', value: 0, unit: '天' },
  { label: '已掌握知识点', value: 0, unit: '' },
  { label: '累计做题', value: 0, unit: '道' },
  { label: '正确率', value: '0%', unit: '' },
])

// ─── Profile ───
const nickname = ref('')
const email = ref('')
const profileSaving = ref(false)

// ─── Password ───
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const passwordSaving = ref(false)

onMounted(async () => {
  if (auth.user) {
    nickname.value = auth.user.nickname
    email.value = auth.user.email
  }
  try {
    const [ov, tr, pr, mistakesRes] = await Promise.all([
      api.get('/stats/overview'),
      api.get('/stats/trend'),
      api.get('/stats/progress'),
      api.get('/mistakes', { params: { limit: 5 } }),
    ])
    overview.value = ov.data
    trend.value = tr.data
    progress.value = pr.data
    recentMistakes.value = mistakesRes.data

    kpiCards.value = [
      { label: '连续打卡', value: ov.data.streak_days, unit: '天' },
      { label: '已掌握知识点', value: ov.data.total_knowledge_points, unit: '' },
      { label: '累计做题', value: ov.data.total_questions_answered, unit: '道' },
      { label: '正确率', value: ov.data.average_accuracy > 0 ? ov.data.average_accuracy + '%' : '0%', unit: '' },
    ]

    if (progressChart.value) {
      new Chart(progressChart.value, {
        type: 'line',
        data: { labels: trend.value.labels, datasets: [{ data: trend.value.values, borderColor: '#ffffff', backgroundColor: 'rgba(255,255,255,0.05)', borderWidth: 1, pointRadius: 0, tension: 0.3, fill: true }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color: '#7d8187', font: { family: 'Courier Prime' } }, grid: { color: '#212327' } }, y: { ticks: { color: '#7d8187', font: { family: 'Courier Prime' } }, grid: { color: '#212327' }, min: 0 } } },
      })
    }

    if (radarChart.value) {
      const labels = Object.keys(progress.value.subjects)
      const values = Object.values(progress.value.subjects) as number[]
      new Chart(radarChart.value, {
        type: 'radar',
        data: { labels, datasets: [{ data: values, borderColor: '#ff7a17', backgroundColor: 'rgba(255,122,23,0.1)', borderWidth: 1, pointRadius: 2, pointBackgroundColor: '#ff7a17' }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { r: { angleLines: { color: '#212327' }, grid: { color: '#212327' }, pointLabels: { color: '#dadbdf', font: { size: 12, family: 'JetBrains Mono' } }, ticks: { color: '#7d8187', backdropColor: 'transparent', stepSize: 50 } } } },
      })
    }
  } catch { /* */ }
})

const saveProfile = async () => {
  profileSaving.value = true
  try {
    const { data } = await api.put('/users/me', { nickname: nickname.value })
    auth.user = data
    localStorage.setItem('user', JSON.stringify(data))
    ui.addToast('个人信息已保存', 'success')
  } catch { ui.addToast('保存失败', 'error') }
  finally { profileSaving.value = false }
}

const changePassword = async () => {
  if (newPassword.value !== confirmPassword.value) {
    ui.addToast('两次输入的新密码不一致', 'error')
    return
  }
  if (newPassword.value.length < 6) {
    ui.addToast('新密码至少 6 位', 'error')
    return
  }
  passwordSaving.value = true
  try {
    await api.put('/users/me/password', { current_password: currentPassword.value, new_password: newPassword.value })
    ui.addToast('密码已修改', 'success')
    currentPassword.value = ''; newPassword.value = ''; confirmPassword.value = ''
  } catch (e: any) {
    ui.addToast(e.response?.data?.detail || '修改失败', 'error')
  }
  finally { passwordSaving.value = false }
}
</script>

<template>
  <div class="p-8 space-y-8">
    <div>
      <p class="eyebrow-mono-sm mb-2">{{ auth.user?.nickname }}</p>
      <h1 class="text-display-sm text-ink">个人主页</h1>
    </div>

    <!-- KPI Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="kpi in kpiCards" :key="kpi.label" class="card-xai flex flex-col gap-2">
        <span class="text-mute text-xs">{{ kpi.label }}</span>
        <div class="flex items-baseline gap-1.5">
          <span class="text-display-sm text-ink">{{ kpi.value }}</span>
          <span v-if="kpi.unit" class="text-mute text-sm">{{ kpi.unit }}</span>
        </div>
      </div>
    </div>

    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div class="card-xai lg:col-span-2">
        <p class="eyebrow-mono-sm text-mute mb-4">学习进度轨迹</p>
        <div class="h-[240px]"><canvas ref="progressChart" /></div>
      </div>
      <div class="card-xai">
        <p class="eyebrow-mono-sm text-mute mb-4">能力图谱</p>
        <div class="h-[240px]"><canvas ref="radarChart" /></div>
      </div>
    </div>

    <!-- Mistake insights -->
    <div class="card-xai">
      <p class="eyebrow-mono-sm text-mute mb-4">错题本洞察</p>
      <div v-if="recentMistakes.length" class="space-y-3">
        <div v-for="m in recentMistakes" :key="m.question_content" class="flex items-center justify-between py-2 border-b border-hairline last:border-b-0">
          <span class="text-body text-sm truncate mr-4">{{ m.question_subject }} — {{ m.question_content?.slice(0, 20) }}...</span>
          <span class="text-mute text-sm shrink-0">错 {{ m.wrong_count }} 次</span>
        </div>
      </div>
      <p v-else class="text-mute text-sm py-4">还没有错题，去做几道题吧</p>
    </div>

    <!-- Profile + Password (2 columns) -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Profile edit -->
      <div class="card-xai space-y-4">
        <p class="eyebrow-mono-sm text-mute mb-2">个人信息</p>
        <div>
          <label class="block text-body text-sm mb-2">昵称</label>
          <input v-model="nickname" type="text" placeholder="你的昵称" class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" />
        </div>
        <div>
          <label class="block text-body text-sm mb-2">邮箱</label>
          <input :value="email" type="email" disabled class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-mute text-sm opacity-60 cursor-not-allowed" />
        </div>
        <button class="btn-pill-filled text-sm px-6 py-2.5" :disabled="profileSaving" @click="saveProfile">{{ profileSaving ? '保存中...' : '保存' }}</button>
      </div>

      <!-- Password change -->
      <div class="card-xai space-y-4">
        <p class="eyebrow-mono-sm text-mute mb-2">修改密码</p>
        <div>
          <label class="block text-body text-sm mb-2">当前密码</label>
          <input v-model="currentPassword" type="password" placeholder="输入当前密码" class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" />
        </div>
        <div>
          <label class="block text-body text-sm mb-2">新密码</label>
          <input v-model="newPassword" type="password" placeholder="至少 6 位" class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" />
        </div>
        <div>
          <label class="block text-body text-sm mb-2">确认新密码</label>
          <input v-model="confirmPassword" type="password" placeholder="再次输入新密码" class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" />
        </div>
        <button class="btn-pill-filled text-sm px-6 py-2.5" :disabled="passwordSaving" @click="changePassword">{{ passwordSaving ? '修改中...' : '修改密码' }}</button>
      </div>
    </div>
  </div>
</template>
