<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Chart, registerables } from 'chart.js'
import api from '@/api/client'

Chart.register(...registerables)

const trendChart = ref<HTMLCanvasElement | null>(null)
const subjectChart = ref<HTMLCanvasElement | null>(null)
const loading = ref(true)
const error = ref('')

const stats = ref([
  { label: '累计做题', value: '0' },
  { label: '平均正确率', value: '0%' },
  { label: '学习次数', value: '0' },
  { label: '当前连续', value: '0 天' },
])

onMounted(async () => {
  try {
    const [ov, tr, pr] = await Promise.all([
      api.get('/stats/overview'),
      api.get('/stats/trend'),
      api.get('/stats/progress'),
    ])

    stats.value = [
      { label: '累计做题', value: String(ov.data.total_questions_answered || 0) },
      { label: '平均正确率', value: (ov.data.average_accuracy || 0) + '%' },
      { label: '学习次数', value: String(ov.data.total_study_minutes ? Math.floor(ov.data.total_study_minutes / 25) : 0) },
      { label: '当前连续', value: (ov.data.streak_days || 0) + ' 天' },
    ]

    if (trendChart.value) {
      new Chart(trendChart.value, {
        type: 'bar',
        data: {
          labels: tr.data.labels,
          datasets: [{
            data: tr.data.values,
            backgroundColor: '#ffffff',
            borderRadius: 2,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { color: '#7d8187' }, grid: { display: false } },
            y: { ticks: { color: '#7d8187' }, grid: { color: '#212327' }, min: 0 },
          },
        },
      })
    }

    if (subjectChart.value) {
      const labels = Object.keys(pr.data.subjects)
      const values = Object.values(pr.data.subjects) as number[]
      new Chart(subjectChart.value, {
        type: 'doughnut',
        data: {
          labels,
          datasets: [{
            data: values,
            backgroundColor: ['#ffffff', '#dadbdf', '#7d8187', '#363a3f', '#212327'],
            borderColor: '#0a0a0a',
            borderWidth: 2,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: { color: '#dadbdf', font: { size: 12, family: 'Courier Prime' }, padding: 16 },
            },
          },
        },
      })
    }
  } catch {
    error.value = '加载失败'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="p-8 space-y-6">
    <div>
      <p class="eyebrow-mono-sm mb-2">数据分析</p>
      <h1 class="text-display-sm text-ink">学习进度</h1>
    </div>

    <div v-if="loading" class="text-mute text-sm py-12 text-center">加载中...</div>
    <div v-else-if="error" class="card-xai text-center py-12 text-red-400">{{ error }}</div>
    <template v-else>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="s in stats" :key="s.label" class="card-xai">
          <span class="text-mute text-xs font-normal">{{ s.label }}</span>
          <div class="text-display-xs text-ink mt-2">{{ s.value }}</div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div class="card-xai lg:col-span-2">
          <p class="eyebrow-mono-sm text-mute mb-4">每周趋势</p>
          <div class="h-[280px]">
            <canvas ref="trendChart" />
          </div>
        </div>
        <div class="card-xai">
          <p class="eyebrow-mono-sm text-mute mb-4">科目分布</p>
          <div class="h-[280px]">
            <canvas ref="subjectChart" />
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
