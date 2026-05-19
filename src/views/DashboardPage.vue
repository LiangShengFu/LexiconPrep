<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Chart, registerables } from 'chart.js'
import api from '@/api/client'

Chart.register(...registerables)

const overview = ref({ streak_days: 0, total_knowledge_points: 0, total_questions_answered: 0, average_accuracy: 0, total_study_minutes: 0 })
const trend = ref({ labels: [] as string[], values: [] as number[] })
const progress = ref({ subjects: {} as Record<string, number> })
const recentMistakes = ref<{ question_subject: string; wrong_count: number; question_content: string }[]>([])
const recentResources = ref<{ id: string; title: string }[]>([])

const progressChart = ref<HTMLCanvasElement | null>(null)
const radarChart = ref<HTMLCanvasElement | null>(null)

const kpiCards = ref([
  { label: '连续打卡', value: 0, unit: '天' },
  { label: '已掌握知识点', value: 0, unit: '' },
  { label: '累计做题', value: 0, unit: '道' },
  { label: '正确率', value: '0%', unit: '' },
])

const loadData = async () => {
  try {
    const [ov, tr, pr, mistakesRes, resourcesRes] = await Promise.all([
      api.get('/stats/overview'),
      api.get('/stats/trend'),
      api.get('/stats/progress'),
      api.get('/mistakes', { params: { limit: 5 } }),
      api.get('/resources', { params: { limit: 4 } }),
    ])
    overview.value = ov.data
    trend.value = tr.data
    progress.value = pr.data
    recentMistakes.value = mistakesRes.data
    recentResources.value = resourcesRes.data

    kpiCards.value = [
      { label: '连续打卡', value: ov.data.streak_days, unit: '天' },
      { label: '已掌握知识点', value: ov.data.total_knowledge_points, unit: '' },
      { label: '累计做题', value: ov.data.total_questions_answered, unit: '道' },
      { label: '正确率', value: ov.data.average_accuracy > 0 ? ov.data.average_accuracy + '%' : '0%', unit: '' },
    ]

    renderCharts()
  } catch (e) {
    console.error('Failed to load dashboard data', e)
  }
}

const renderCharts = () => {
  if (progressChart.value) {
    new Chart(progressChart.value, {
      type: 'line',
      data: {
        labels: trend.value.labels,
        datasets: [{
          data: trend.value.values,
          borderColor: '#ffffff',
          backgroundColor: 'rgba(255,255,255,0.05)',
          borderWidth: 1,
          pointRadius: 0,
          tension: 0.3,
          fill: true,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { color: '#7d8187' }, grid: { color: '#212327' } },
          y: { ticks: { color: '#7d8187' }, grid: { color: '#212327' }, min: 0 },
        },
      },
    })
  }

  if (radarChart.value) {
    const subjects = Object.keys(progress.value.subjects)
    const values = Object.values(progress.value.subjects)
    new Chart(radarChart.value, {
      type: 'radar',
      data: {
        labels: subjects,
        datasets: [{
          data: values,
          borderColor: '#ff7a17',
          backgroundColor: 'rgba(255,122,23,0.1)',
          borderWidth: 1,
          pointRadius: 2,
          pointBackgroundColor: '#ff7a17',
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          r: {
            angleLines: { color: '#212327' },
            grid: { color: '#212327' },
            pointLabels: { color: '#dadbdf', font: { size: 12, family: 'Inter' } },
            ticks: { color: '#7d8187', backdropColor: 'transparent', stepSize: 50 },
          },
        },
      },
    })
  }
}

onMounted(loadData)
</script>

<template>
  <div class="p-8 space-y-8">
    <div>
      <p class="eyebrow-mono-sm mb-2">欢迎回来</p>
      <h1 class="text-display-sm text-ink">仪表盘</h1>
    </div>

    <!-- KPI Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="kpi in kpiCards" :key="kpi.label" class="card-xai flex flex-col gap-2">
        <span class="text-mute text-xs font-normal">{{ kpi.label }}</span>
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
        <div class="h-[240px]">
          <canvas ref="progressChart" />
        </div>
      </div>
      <div class="card-xai">
        <p class="eyebrow-mono-sm text-mute mb-4">能力图谱</p>
        <div class="h-[240px]">
          <canvas ref="radarChart" />
        </div>
      </div>
    </div>

    <!-- Bottom Row -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div class="card-xai lg:col-span-2">
        <p class="eyebrow-mono-sm text-mute mb-4">错题本洞察</p>
        <div v-if="recentMistakes.length" class="space-y-3">
          <div v-for="m in recentMistakes" :key="m.question_content" class="flex items-center justify-between py-2 border-b border-hairline">
            <span class="text-body text-sm truncate mr-4">{{ m.question_subject }} — {{ m.question_content?.slice(0, 18) }}...</span>
            <span class="text-mute text-sm shrink-0">错 {{ m.wrong_count }} 次</span>
          </div>
        </div>
        <div v-else class="text-mute text-sm py-4 text-center">还没有错题，去做几道题吧</div>
        <button class="btn-pill-outline mt-4 text-sm" @click="$router.push('/library')">查看错题本</button>
      </div>

      <div class="card-xai">
        <p class="eyebrow-mono-sm text-mute mb-4">快捷入口</p>
        <div v-if="recentResources.length" class="space-y-2">
          <button v-for="r in recentResources" :key="r.id" class="btn-pill-outline w-full text-sm justify-start truncate">{{ r.title }}</button>
        </div>
        <div v-else class="text-mute text-sm py-4 text-center">暂无资源</div>
      </div>
    </div>
  </div>
</template>
