<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { Chart, BarController, DoughnutController, ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js'
import { useUiStore } from '@/stores/ui'
import api from '@/api/client'

Chart.register(BarController, DoughnutController, ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend)

const trendChart = ref<HTMLCanvasElement | null>(null)
const subjectChart = ref<HTMLCanvasElement | null>(null)
const loading = ref(true)
const error = ref('')
let trendInstance: Chart | null = null
let subjectInstance: Chart | null = null

const showDiagnosis = ref(false)
const diagnosisLoading = ref(false)
const diagnosisText = ref('')

const showStudyPlan = ref(false)
const studyPlanLoading = ref(false)
const studyPlanForm = ref({ days: 7, daily_minutes: 60, target_subjects: '' as string })
const studyPlanData = ref<any>(null)

onBeforeUnmount(() => {
  trendInstance?.destroy()
  subjectInstance?.destroy()
})

const stats = ref([
  { label: '累计做题', value: '0' },
  { label: '平均正确率', value: '0%' },
  { label: '学习次数', value: '0' },
  { label: '当前连续', value: '0 天' },
])

const fetchData = async () => {
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
      trendInstance?.destroy()
      trendInstance = new Chart(trendChart.value, {
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
      subjectInstance?.destroy()
      subjectInstance = new Chart(subjectChart.value, {
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
}

onMounted(fetchData)

const fetchDiagnosis = async () => {
  diagnosisLoading.value = true
  diagnosisText.value = ''
  showDiagnosis.value = true
  try {
    const { data } = await api.get('/ai/diagnosis')
    diagnosisText.value = data.diagnosis
  } catch (e: any) {
    const msg = e.response?.data?.detail || 'AI 诊断失败'
    useUiStore().addToast(msg, 'error')
    showDiagnosis.value = false
  } finally {
    diagnosisLoading.value = false
  }
}

const fetchStudyPlan = async () => {
  studyPlanLoading.value = true
  studyPlanData.value = null
  showStudyPlan.value = true
  try {
    const payload: any = {
      days: studyPlanForm.value.days,
      daily_minutes: studyPlanForm.value.daily_minutes,
    }
    const subjects = studyPlanForm.value.target_subjects.split(/[,，]/).map(s => s.trim()).filter(Boolean)
    if (subjects.length > 0) payload.target_subjects = subjects
    const { data } = await api.post('/ai/study-plan', payload)
    studyPlanData.value = data
  } catch (e: any) {
    const msg = e.response?.data?.detail || 'AI 学习计划生成失败'
    useUiStore().addToast(msg, 'error')
    showStudyPlan.value = false
  } finally {
    studyPlanLoading.value = false
  }
}

const renderMarkdown = (text: string) => {
  return text
    .replace(/^### (.+)$/gm, '<h3 class="text-ink text-sm font-bold mt-4 mb-2">$1</h3>')
    .replace(/^## (.+)$/gm, '<h2 class="text-ink text-base font-bold mt-5 mb-2">$1</h2>')
    .replace(/^\*\*(.+?)\*\*/g, '<strong class="text-ink">$1</strong>')
    .replace(/^- (.+)$/gm, '<li class="text-body text-sm ml-4">$1</li>')
    .replace(/^(\d+)\. (.+)$/gm, '<li class="text-body text-sm ml-4">$1. $2</li>')
    .replace(/\n\n/g, '<br/><br/>')
    .replace(/\n/g, '<br/>')
}
</script>

<template>
  <div class="p-8 space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="eyebrow-mono-sm mb-2">数据分析</p>
        <h1 class="text-display-sm text-ink">学习进度</h1>
      </div>
      <div class="flex gap-3">
        <button class="btn-pill-outline cursor-target text-sm" @click="showStudyPlan = true; studyPlanData = null">AI 学习计划</button>
        <button class="btn-pill-filled cursor-target text-sm" @click="fetchDiagnosis">AI 诊断</button>
      </div>
    </div>

    <div v-if="loading" class="text-mute text-sm py-12 text-center">加载中...</div>
    <div v-else-if="error" class="card-xai text-center py-12">
      <p class="text-red-400 mb-4">{{ error }}</p>
      <button class="btn-pill-outline cursor-target text-sm" @click="() => { error = ''; loading = true; fetchData() }">重试</button>
    </div>
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

    <!-- AI Diagnosis Modal -->
    <div v-if="showDiagnosis" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60" @click.self="showDiagnosis = false">
      <div class="card-xai w-full max-w-[680px] mx-4 max-h-[85vh] overflow-auto space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <p class="eyebrow-mono-sm text-mute mb-1">AI 学习诊断</p>
            <h2 class="text-body-lg text-ink">个性化诊断报告</h2>
          </div>
          <button class="text-mute text-sm hover:text-ink transition-colors" @click="showDiagnosis = false">✕</button>
        </div>

        <div v-if="diagnosisLoading" class="py-16 text-center space-y-4">
          <div class="inline-block w-8 h-8 border-2 border-ink border-t-transparent rounded-full animate-spin" />
          <p class="text-mute text-sm">AI 正在分析你的学习数据...</p>
          <p class="text-mute text-xs">约需 10-15 秒</p>
        </div>

        <div v-else class="prose prose-invert max-w-none" v-html="renderMarkdown(diagnosisText)" />
      </div>
    </div>

    <!-- AI Study Plan Modal -->
    <div v-if="showStudyPlan" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60" @click.self="showStudyPlan = false">
      <div class="card-xai w-full max-w-[720px] mx-4 max-h-[90vh] overflow-auto space-y-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="eyebrow-mono-sm text-mute mb-1">AI 学习计划</p>
            <h2 class="text-body-lg text-ink">个性化学习规划</h2>
          </div>
          <button class="text-mute text-sm hover:text-ink transition-colors" @click="showStudyPlan = false">✕</button>
        </div>

        <!-- Plan Config (shown when no plan yet) -->
        <div v-if="!studyPlanData && !studyPlanLoading" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-body text-xs mb-1">计划天数</label>
              <select v-model.number="studyPlanForm.days" class="w-full bg-canvas-soft border border-hairline rounded-card px-3 py-2 text-ink text-sm">
                <option v-for="d in [3, 5, 7, 10, 14, 21, 30]" :key="d" :value="d">{{ d }} 天</option>
              </select>
            </div>
            <div>
              <label class="block text-body text-xs mb-1">每日学习时间</label>
              <select v-model.number="studyPlanForm.daily_minutes" class="w-full bg-canvas-soft border border-hairline rounded-card px-3 py-2 text-ink text-sm">
                <option :value="30">30 分钟</option>
                <option :value="60">1 小时</option>
                <option :value="90">1.5 小时</option>
                <option :value="120">2 小时</option>
                <option :value="180">3 小时</option>
                <option :value="240">4 小时</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block text-body text-xs mb-1">重点学科（可选，逗号分隔）</label>
            <input v-model="studyPlanForm.target_subjects" placeholder="如：政治, 英语" class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" />
          </div>
          <div class="bg-canvas-soft border border-hairline rounded-card p-3 text-xs text-mute space-y-1">
            <p>AI 将基于你的错题记录、正确率趋势和薄弱章节，生成包含以下内容的学习计划：</p>
            <p>每日学习重点 + 具体任务 + 复习安排 + 预估提升空间</p>
          </div>
          <div class="flex gap-3 pt-1">
            <button class="btn-pill-outline cursor-target flex-1 text-sm" @click="showStudyPlan = false">取消</button>
            <button class="btn-pill-filled cursor-target flex-1 text-sm" @click="fetchStudyPlan">生成学习计划</button>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="studyPlanLoading" class="py-16 text-center space-y-4">
          <div class="inline-block w-8 h-8 border-2 border-ink border-t-transparent rounded-full animate-spin" />
          <p class="text-mute text-sm">AI 正在为你制定学习计划...</p>
          <p class="text-mute text-xs">约需 15-20 秒</p>
        </div>

        <!-- Plan Result -->
        <div v-if="studyPlanData && !studyPlanLoading" class="space-y-4">
          <div v-if="studyPlanData.summary" class="bg-canvas-soft border border-hairline rounded-card p-4">
            <p class="text-ink text-sm font-bold mb-1">规划概述</p>
            <p class="text-body text-sm">{{ studyPlanData.summary }}</p>
            <p v-if="studyPlanData.estimated_accuracy_gain" class="text-mute text-xs mt-2">预估正确率提升：{{ studyPlanData.estimated_accuracy_gain }}</p>
          </div>

          <div class="space-y-3">
            <div v-for="day in studyPlanData.plan" :key="day.day" class="border border-hairline rounded-card p-4 space-y-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-ink text-canvas text-xs font-bold">D{{ day.day }}</span>
                  <span class="text-ink text-sm font-bold">{{ day.focus }}</span>
                </div>
                <span class="text-mute text-xs">{{ day.duration_minutes }} 分钟</span>
              </div>

              <div>
                <p class="text-mute text-xs mb-1.5">学习任务</p>
                <ul class="space-y-1">
                  <li v-for="(task, ti) in day.tasks" :key="ti" class="flex items-start gap-2 text-body text-sm">
                    <span class="text-mute text-xs mt-0.5 shrink-0">•</span>
                    <span>{{ task }}</span>
                  </li>
                </ul>
              </div>

              <div v-if="day.review_topics && day.review_topics.length > 0">
                <p class="text-mute text-xs mb-1.5">复习要点</p>
                <div class="flex flex-wrap gap-1.5">
                  <span v-for="(topic, ti) in day.review_topics" :key="ti" class="text-xs px-2 py-0.5 rounded-full border border-hairline text-mute">{{ topic }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="flex gap-3 pt-2">
            <button class="btn-pill-outline cursor-target flex-1 text-sm" @click="studyPlanData = null">重新配置</button>
            <button class="btn-pill-filled cursor-target flex-1 text-sm" @click="fetchStudyPlan">重新生成</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
