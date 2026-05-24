<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import api from '@/api/client'

interface Question {
  id: string
  type: string
  content: string
  options: string[]
  difficulty: number
  subject: string
  chapter: string | null
}

const phase = ref<'select' | 'exam' | 'result'>('select')
const selectedSubject = ref('政治')
const questions = ref<Question[]>([])
const answers = ref<Record<string, string[]>>({})
const feedback = ref<Record<string, { correct: boolean; analysis: string | null }>>({})
const currentIndex = ref(0)
const sheetOpen = ref(false)
const timeElapsed = ref(0)
const loading = ref(false)
const error = ref('')
const questionStartAt = ref<Record<string, number>>({})

const subjects = ref<string[]>([])
const loadingSubjects = ref(false)

const fetchSubjects = async () => {
  loadingSubjects.value = true
  try {
    const { data } = await api.get('/questions/subjects')
    subjects.value = data
  } catch {
    subjects.value = ['政治', '英语', '数学']
  } finally {
    loadingSubjects.value = false
  }
}

onMounted(() => { fetchSubjects() })

const totalQuestions = computed(() => questions.value.length)
const answeredCount = computed(() => Object.keys(answers.value).length)
const currentQuestion = computed(() => questions.value[currentIndex.value])
const score = computed(() => Object.values(feedback.value).filter(f => f.correct).length)

let timer: ReturnType<typeof setInterval> | null = null

onUnmounted(() => { if (timer) clearInterval(timer) })

const formatTime = (s: number) => {
  const m = Math.floor(s / 60)
  const sec = s % 60
  return `${m.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`
}

const startExam = async () => {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/questions', { params: { subject: selectedSubject.value, limit: 50 } })
    if (!data.length) {
      error.value = '该学科暂无题目'
      return
    }
    questions.value = data
    answers.value = {}
    feedback.value = {}
    questionStartAt.value = {}
    currentIndex.value = 0
    timeElapsed.value = 0
    phase.value = 'exam'
    timer = setInterval(() => { timeElapsed.value++ }, 1000)
    questionStartAt.value[data[0].id] = Date.now()
  } catch {
    error.value = '加载题目失败'
  } finally {
    loading.value = false
  }
}

const isMultiple = (q: Question) => q.type === 'MULTIPLE'

const toggleOption = (qId: string, label: string, multiple: boolean) => {
  if (feedback.value[qId]) return
  if (multiple) {
    const current = answers.value[qId] || []
    if (current.includes(label)) {
      answers.value[qId] = current.filter(l => l !== label)
    } else {
      answers.value[qId] = [...current, label]
    }
  } else {
    answers.value[qId] = [label]
  }
}

const submitAnswer = async (qId: string) => {
  const selected = answers.value[qId]
  if (!selected || !selected.length) return

  const now = Date.now()
  const start = questionStartAt.value[qId] || now
  const timeSpent = Math.round((now - start) / 1000)

  try {
    const { data } = await api.post(`/questions/${qId}/answer`, {
      user_answer: selected,
      time_spent: timeSpent,
    })
    feedback.value[qId] = { correct: data.is_correct, analysis: data.analysis }
  } catch {
    feedback.value[qId] = { correct: false, analysis: null }
  }
}

const prevQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
    if (currentQuestion.value && !questionStartAt.value[currentQuestion.value.id] && !feedback.value[currentQuestion.value.id]) {
      questionStartAt.value[currentQuestion.value.id] = Date.now()
    }
  }
}
const nextQuestion = () => {
  if (currentIndex.value < totalQuestions.value - 1) {
    currentIndex.value++
    if (currentQuestion.value && !questionStartAt.value[currentQuestion.value.id] && !feedback.value[currentQuestion.value.id]) {
      questionStartAt.value[currentQuestion.value.id] = Date.now()
    }
  }
}
const goToQuestion = (idx: number) => {
  currentIndex.value = idx
  if (currentQuestion.value && !questionStartAt.value[currentQuestion.value.id] && !feedback.value[currentQuestion.value.id]) {
    questionStartAt.value[currentQuestion.value.id] = Date.now()
  }
}

const finishExam = () => {
  if (timer) clearInterval(timer)
  phase.value = 'result'
}

const retry = () => {
  phase.value = 'select'
  if (timer) clearInterval(timer)
}

const optionLabel = (idx: number) => String.fromCharCode(65 + idx)

const isOptionSelected = (qId: string, label: string) => {
  return (answers.value[qId] || []).includes(label)
}

const getOptionClass = (qId: string, label: string) => {
  const fb = feedback.value[qId]
  const selected = isOptionSelected(qId, label)
  if (fb) {
    if (selected) {
      return fb.correct ? 'border-green-500 text-green-400 bg-green-500/10' : 'border-red-500 text-red-400 bg-red-500/10'
    }
    return 'border-4 border-dashed border-hairline text-mute opacity-50'
  }
  if (selected) return 'border-4 border-dashed border-ink text-ink bg-canvas-soft'
  return 'border-4 border-dashed border-hairline text-body hover:border-canvas-mid'
}
</script>

<template>
  <div class="p-8 h-full flex flex-col">
    <!-- ─── Subject Select ─── -->
    <div v-if="phase === 'select'" class="flex-1 flex items-center justify-center">
      <div class="card-xai max-w-[480px] w-full py-16 text-center">
        <p class="eyebrow-mono-sm mb-2">专注模式</p>
        <h1 class="text-display-sm text-ink mb-8">做题模式</h1>

        <div class="space-y-4 mb-8">
          <label class="block text-body text-sm mb-2">选择学科</label>
          <div class="flex justify-center gap-3">
            <button
              v-for="s in subjects"
              :key="s"
              class="btn-pill-outline cursor-target text-sm px-8"
              :class="{ 'border-ink bg-canvas-soft': selectedSubject === s }"
              @click="selectedSubject = s"
            >
              {{ s }}
            </button>
          </div>
        </div>

        <div v-if="error" class="text-red-400 text-sm mb-4">{{ error }}</div>
        <button class="btn-pill-filled cursor-target text-base px-10 py-3" :disabled="loading" @click="startExam">
          {{ loading ? '加载中...' : '开始做题' }}
        </button>
      </div>
    </div>

    <!-- ─── Exam Mode ─── -->
    <div v-else-if="phase === 'exam'" class="flex-1 flex flex-col">
      <div class="flex items-center justify-between mb-6">
        <div>
          <p class="eyebrow-mono-sm mb-1">{{ selectedSubject }} · 专注模式</p>
          <h1 class="text-display-sm text-ink">做题模式</h1>
        </div>
        <div class="flex items-center gap-4">
          <span class="text-mute text-sm">已答 {{ answeredCount }} / {{ totalQuestions }} 题</span>
          <span class="text-ink font-mono text-lg">{{ formatTime(timeElapsed) }}</span>
          <button class="btn-pill-filled cursor-target text-sm" @click="finishExam">提交</button>
        </div>
      </div>

      <div class="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-6 pb-16 lg:pb-0">
        <!-- Question Canvas -->
        <div class="lg:col-span-3 card-xai flex flex-col">
          <div class="flex items-center gap-3 mb-6">
            <span class="text-xs px-2 py-0.5 rounded-full border-4 border-dashed border-hairline text-mute font-mono uppercase">{{ currentQuestion.type === 'SINGLE' ? '单选' : '多选' }}</span>
            <span class="text-mute text-sm">第 {{ currentIndex + 1 }} 题 / 共 {{ totalQuestions }} 题</span>
            <span class="text-xs px-2 py-0.5 rounded-full border-4 border-dashed border-hairline text-mute">{{ currentQuestion.subject }} · {{ currentQuestion.chapter }}</span>
          </div>

          <p class="text-ink text-lg font-normal leading-relaxed mb-8">{{ currentQuestion.content }}</p>

          <div class="space-y-3" :role="isMultiple(currentQuestion) ? 'group' : 'radiogroup'" :aria-label="'第' + (currentIndex + 1) + '题选项'">
            <button
              v-for="(opt, idx) in currentQuestion.options"
              :key="idx"
              :role="isMultiple(currentQuestion) ? 'checkbox' : 'radio'"
              :aria-checked="isOptionSelected(currentQuestion.id, optionLabel(idx))"
              class="w-full text-left px-5 py-3 rounded-card border text-sm font-normal transition-colors"
              :class="getOptionClass(currentQuestion.id, optionLabel(idx))"
              @click="toggleOption(currentQuestion.id, optionLabel(idx), isMultiple(currentQuestion))"
            >
              <span class="text-mute mr-2">{{ optionLabel(idx) }}.</span>{{ opt }}
            </button>
          </div>

          <!-- Submit button for current question -->
          <div v-if="!feedback[currentQuestion.id] && answers[currentQuestion.id]?.length" class="mt-4">
            <button class="btn-pill-filled cursor-target text-sm" @click="submitAnswer(currentQuestion.id)">
              确认提交
            </button>
          </div>

          <!-- Feedback -->
          <div v-if="feedback[currentQuestion.id]" class="mt-4 p-4 rounded-card border text-sm" :class="feedback[currentQuestion.id].correct ? 'border-green-500/30 bg-green-500/5 text-green-400' : 'border-red-500/30 bg-red-500/5 text-red-400'">
            {{ feedback[currentQuestion.id].correct ? '回答正确' : '回答错误' }}
            <span v-if="feedback[currentQuestion.id].analysis" class="block mt-2 text-body">{{ feedback[currentQuestion.id].analysis }}</span>
          </div>

          <div class="flex items-center justify-between mt-8 pt-4 border-t-4 border-dashed border-hairline">
            <button class="btn-pill-outline cursor-target text-sm" :disabled="currentIndex === 0" @click="prevQuestion">上一题</button>
            <button
              v-if="currentIndex < totalQuestions - 1"
              class="btn-pill-filled cursor-target text-sm"
              @click="nextQuestion"
            >
              下一题
            </button>
          </div>
        </div>

        <!-- Answer Sheet (floating bottom on mobile, sidebar on desktop) -->
        <div class="fixed bottom-0 left-0 right-0 z-50 lg:static lg:z-auto rounded-t-2xl lg:rounded-card border-t lg:border-4 border-dashed border-hairline bg-white dark:bg-gray-900 p-4 lg:p-6 shadow-lg lg:shadow-none transition-transform duration-300 max-h-[60vh] lg:max-h-none overflow-y-auto" :class="sheetOpen ? 'translate-y-0' : 'translate-y-[calc(100%-40px)] lg:translate-y-0'">
          <div class="flex items-center justify-center lg:hidden mb-2 cursor-pointer" @click="sheetOpen = !sheetOpen">
            <div class="w-10 h-1.5 rounded-full bg-gray-300 dark:bg-gray-600" />
          </div>
          <p class="eyebrow-mono-sm text-mute mb-4">答题卡</p>
          <div class="grid grid-cols-5 gap-2">
            <button
              v-for="(q, idx) in questions"
              :key="q.id"
              class="w-10 h-10 rounded-card border text-xs font-mono transition-colors"
              :class="feedback[q.id]
                ? feedback[q.id].correct ? 'border-green-500 text-green-400 bg-green-500/10' : 'border-red-500 text-red-400 bg-red-500/10'
                : answers[q.id]?.length ? 'border-4 border-dashed border-ink text-ink bg-canvas-soft' : 'border-4 border-dashed border-hairline text-mute'"
              @click="goToQuestion(idx)"
            >
              {{ idx + 1 }}
            </button>
          </div>
          <div class="mt-6 pt-4 border-t-4 border-dashed border-hairline space-y-2 text-xs text-mute">
            <div class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-sm border border-dashed border-ink bg-canvas-soft" /> 已答</div>
            <div class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-sm border-4 border-dashed border-hairline" /> 未答</div>
            <div class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-sm bg-green-500/20 border-4 border-dashed border-green-500" /> 正确</div>
            <div class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-sm bg-red-500/20 border-4 border-dashed border-red-500" /> 错误</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ─── Results ─── -->
    <div v-else class="flex-1 flex items-center justify-center">
      <div class="card-xai text-center max-w-[480px] w-full py-16">
        <p class="eyebrow-mono mb-4">答题完成</p>
        <div class="text-display-xl text-ink mb-4">{{ score }} / {{ totalQuestions }}</div>
        <p class="text-body mb-4">
          {{ score >= totalQuestions * 0.8 ? '表现优秀，准备充分！' : score >= totalQuestions * 0.5 ? '继续努力，重点复习错题。' : '加油，集中攻克薄弱环节。' }}
        </p>
        <p class="text-mute text-sm mb-6">用时: {{ formatTime(timeElapsed) }}</p>
        <div class="flex items-center justify-center gap-3">
          <button class="btn-pill-outline cursor-target text-sm" @click="retry">重新选题</button>
          <button class="btn-pill-filled cursor-target text-sm" @click="phase = 'exam'; currentIndex = 0">查看答题</button>
        </div>
      </div>
    </div>
  </div>
</template>
