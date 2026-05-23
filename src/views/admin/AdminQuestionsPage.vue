<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUiStore } from '@/stores/ui'
import api from '@/api/client'

interface Question { id: string; type: string; content: string; options: string[]; answer: string[]; subject: string; difficulty: number; chapter: string | null; analysis?: string | null }

const questions = ref<Question[]>([])
const loading = ref(true)
const search = ref('')
const filterSubject = ref('')
const showEdit = ref(false)
const editMode = ref<'create' | 'edit'>('create')
const editId = ref('')
const form = ref({ type: 'SINGLE', content: '', options: ['', '', '', ''], answer: [''], analysis: '', difficulty: 1, subject: '政治', chapter: '' })
const saving = ref(false)

const showAiGenerate = ref(false)
const aiForm = ref({ subject: '政治', chapter: '', difficulty: 2, count: 5, type: 'SINGLE' })
const aiGenerating = ref(false)

const selectedIds = ref<Set<string>>(new Set())
const batchDeleting = ref(false)
const batchMode = ref(false)

const allSelected = computed(() => questions.value.length > 0 && questions.value.every(q => selectedIds.value.has(q.id)))

const load = async () => {
  loading.value = true
  try {
    const params: any = { limit: 100, _t: Date.now() }
    if (search.value) params.search = search.value
    if (filterSubject.value) params.subject = filterSubject.value
    const { data } = await api.get('/admin/questions', { params })
    questions.value = data
    selectedIds.value.clear()
  } catch {
    useUiStore().addToast('加载题目失败', 'error')
  } finally {
    loading.value = false
  }
}

onMounted(load)

const toggleSelect = (id: string) => {
  const next = new Set(selectedIds.value)
  if (next.has(id)) next.delete(id)
  else next.add(id)
  selectedIds.value = next
}

const toggleSelectAll = () => {
  if (allSelected.value) {
    selectedIds.value = new Set()
  } else {
    selectedIds.value = new Set(questions.value.map(q => q.id))
  }
}

const batchDelete = async () => {
  if (!selectedIds.value.size) return
  if (!confirm(`确定批量删除选中的 ${selectedIds.value.size} 道题目？关联的错题和学习记录也会被删除。`)) return
  batchDeleting.value = true
  try {
    await api.post('/admin/questions/batch-delete', { ids: [...selectedIds.value] })
    useUiStore().addToast(`已删除 ${selectedIds.value.size} 道题目`, 'success')
    await load()
  } catch {
    useUiStore().addToast('批量删除失败', 'error')
  } finally {
    batchDeleting.value = false
  }
}

const openCreate = () => {
  editMode.value = 'create'
  editId.value = ''
  form.value = { type: 'SINGLE', content: '', options: ['', '', '', ''], answer: [''], analysis: '', difficulty: 1, subject: '政治', chapter: '' }
  showEdit.value = true
}

const openEdit = (q: Question) => {
  editMode.value = 'edit'
  editId.value = q.id
  const opts = q.options || []
  const ans = q.answer || []
  form.value = { type: q.type, content: q.content, options: [...opts, ...Array(Math.max(0, 4 - opts.length)).fill('')].slice(0, 4), answer: [...ans], analysis: q.analysis || '', difficulty: q.difficulty, subject: q.subject, chapter: q.chapter || '' }
  showEdit.value = true
}

const save = async () => {
  saving.value = true
  const payload = { ...form.value, options: form.value.options.filter(o => o), answer: form.value.answer.filter(a => a) }
  try {
    if (editMode.value === 'create') {
      await api.post('/admin/questions', payload)
    } else {
      await api.put(`/admin/questions/${editId.value}`, payload)
    }
    showEdit.value = false
    await load()
    useUiStore().addToast('保存成功', 'success')
  } catch {
    useUiStore().addToast('保存失败', 'error')
  }
  finally { saving.value = false }
}

const deleteQuestion = async (id: string) => {
  if (!confirm('确定删除该题目？关联的错题和学习记录也会被删除。')) return
  try {
    await api.delete(`/admin/questions/${id}`)
    await load()
    useUiStore().addToast('已删除', 'success')
  } catch {
    useUiStore().addToast('删除失败', 'error')
  }
}

const generateAiQuestions = async () => {
  aiGenerating.value = true
  try {
    const payload: any = {
      subject: aiForm.value.subject,
      difficulty: aiForm.value.difficulty,
      count: aiForm.value.count,
      type: aiForm.value.type,
    }
    if (aiForm.value.chapter.trim()) payload.chapter = aiForm.value.chapter.trim()
    const { data } = await api.post('/ai/generate-questions', payload)
    showAiGenerate.value = false
    await load()
    useUiStore().addToast(`AI 已生成 ${data.generated} 道题目`, 'success')
  } catch (e: any) {
    const msg = e.response?.data?.detail || 'AI 出题失败'
    useUiStore().addToast(msg, 'error')
  } finally {
    aiGenerating.value = false
  }
}
</script>

<template>
  <div class="p-8 space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="eyebrow-mono-sm mb-2">管理</p>
        <h1 class="text-display-sm text-ink">题目管理</h1>
      </div>
      <div class="flex gap-3">
        <button
          class="btn-pill-outline cursor-target text-sm"
          :class="batchMode ? 'border-accent-sunset/30 text-accent-sunset' : ''"
          @click="batchMode = !batchMode; if (!batchMode) selectedIds.clear()"
        >
          {{ batchMode ? '退出批量管理' : '批量管理' }}
        </button>
        <button v-if="batchMode && selectedIds.size" class="btn-pill-outline cursor-target text-sm border-red-500/30 text-red-400 hover:border-red-500" :disabled="batchDeleting" @click="batchDelete">
          {{ batchDeleting ? '删除中...' : `删除选中 (${selectedIds.size})` }}
        </button>
        <button class="btn-pill-outline cursor-target text-sm" @click="showAiGenerate = true">AI 批量出题</button>
        <button class="btn-pill-filled cursor-target text-sm" @click="openCreate">添加题目</button>
      </div>
    </div>

    <div class="flex gap-3">
      <input v-model="search" placeholder="搜索题目..." class="flex-1 bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" @keyup.enter="load" />
      <select v-model="filterSubject" class="bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm" @change="load">
        <option value="">全部学科</option>
        <option value="政治">政治</option>
        <option value="英语">英语</option>
        <option value="数学">数学</option>
      </select>
    </div>

    <div v-if="loading" class="text-mute text-sm py-8">加载中...</div>
    <div v-else class="space-y-2">
      <div v-if="batchMode" class="flex items-center gap-2 px-2 pb-1">
        <input type="checkbox" :checked="allSelected" class="cursor-target" @change="toggleSelectAll" />
        <span class="text-mute text-xs cursor-pointer" @click="toggleSelectAll">{{ allSelected ? '取消全选' : '全选' }}</span>
        <span v-if="selectedIds.size" class="text-mute text-xs">已选 {{ selectedIds.size }} 项</span>
      </div>
      <div v-for="q in questions" :key="q.id" class="card-xai flex items-start gap-4">
        <input v-if="batchMode" type="checkbox" :checked="selectedIds.has(q.id)" class="cursor-target mt-0.5 shrink-0" @change="toggleSelect(q.id)" />
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-1">
            <span class="text-xs px-2 py-0.5 rounded-full border border-hairline text-mute">{{ q.subject }}</span>
            <span class="text-xs px-2 py-0.5 rounded-full border border-hairline text-mute">{{ q.type === 'SINGLE' ? '单选' : '多选' }}</span>
            <span class="text-xs text-mute">难度 {{ q.difficulty }}</span>
          </div>
          <p class="text-body text-sm truncate">{{ q.content }}</p>
        </div>
        <div class="flex items-center gap-2 shrink-0">
          <button class="btn-pill-outline cursor-target text-xs" @click="openEdit(q)">编辑</button>
          <button class="btn-pill-outline cursor-target text-xs border-red-500/30 text-red-400 hover:border-red-500" @click="deleteQuestion(q.id)">删除</button>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEdit" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60" @click.self="showEdit = false">
      <div class="card-xai w-full max-w-[640px] mx-4 max-h-[90vh] overflow-auto space-y-4">
        <p class="eyebrow-mono-sm text-mute">{{ editMode === 'create' ? '添加题目' : '编辑题目' }}</p>
        <div class="grid grid-cols-3 gap-3">
          <div>
            <label class="block text-body text-xs mb-1">题型</label>
            <select v-model="form.type" class="w-full bg-canvas-soft border border-hairline rounded-card px-3 py-2 text-ink text-sm">
              <option value="SINGLE">单选</option>
              <option value="MULTIPLE">多选</option>
            </select>
          </div>
          <div>
            <label class="block text-body text-xs mb-1">学科</label>
            <select v-model="form.subject" class="w-full bg-canvas-soft border border-hairline rounded-card px-3 py-2 text-ink text-sm">
              <option value="政治">政治</option>
              <option value="英语">英语</option>
              <option value="数学">数学</option>
            </select>
          </div>
          <div>
            <label class="block text-body text-xs mb-1">难度</label>
            <select v-model.number="form.difficulty" class="w-full bg-canvas-soft border border-hairline rounded-card px-3 py-2 text-ink text-sm">
              <option v-for="d in 5" :key="d" :value="d">{{ d }}</option>
            </select>
          </div>
        </div>
        <div>
          <label class="block text-body text-xs mb-1">章节</label>
          <input v-model="form.chapter" placeholder="如：马克思主义哲学" class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" />
        </div>
        <div>
          <label class="block text-body text-xs mb-1">题目内容</label>
          <textarea v-model="form.content" rows="3" class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" />
        </div>
        <div>
          <label class="block text-body text-xs mb-1">选项（{{ form.type === 'SINGLE' ? '单选' : '多选' }}）</label>
          <div v-for="(_, i) in 4" :key="i" class="flex items-center gap-2 mb-1">
            <span class="text-mute text-xs w-5">{{ String.fromCharCode(65 + i) }}</span>
            <input v-model="form.options[i]" :placeholder="`选项 ${String.fromCharCode(65 + i)}`" class="flex-1 bg-canvas-soft border border-hairline rounded-card px-3 py-1.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" />
          </div>
        </div>
        <div>
          <label class="block text-body text-xs mb-1">正确答案（填入选项字母，如 {{ form.type === 'SINGLE' ? 'A' : 'A, B, C' }}）</label>
          <input v-model="form.answer[0]" placeholder="用逗号分隔，如 A,B" class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" @change="form.answer = form.answer[0]?.split(',').map(s => s.trim()).filter(Boolean) || []" />
        </div>
        <div>
          <label class="block text-body text-xs mb-1">答案解析（可选）</label>
          <textarea v-model="form.analysis" rows="2" class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" />
        </div>
        <div class="flex gap-3 pt-2">
          <button class="btn-pill-outline cursor-target flex-1 text-sm" @click="showEdit = false">取消</button>
          <button class="btn-pill-filled cursor-target flex-1 text-sm" :disabled="saving" @click="save">{{ saving ? '保存中...' : '保存' }}</button>
        </div>
      </div>
    </div>

    <!-- AI Generate Modal -->
    <div v-if="showAiGenerate" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60" @click.self="showAiGenerate = false">
      <div class="card-xai w-full max-w-[520px] mx-4 space-y-5">
        <div>
          <p class="eyebrow-mono-sm text-mute mb-1">AI 出题</p>
          <h2 class="text-body-lg text-ink">批量生成题目</h2>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-body text-xs mb-1">学科</label>
            <select v-model="aiForm.subject" class="w-full bg-canvas-soft border border-hairline rounded-card px-3 py-2 text-ink text-sm">
              <option value="政治">政治</option>
              <option value="英语">英语</option>
              <option value="数学">数学</option>
            </select>
          </div>
          <div>
            <label class="block text-body text-xs mb-1">题型</label>
            <select v-model="aiForm.type" class="w-full bg-canvas-soft border border-hairline rounded-card px-3 py-2 text-ink text-sm">
              <option value="SINGLE">单选题</option>
              <option value="MULTIPLE">多选题</option>
            </select>
          </div>
          <div>
            <label class="block text-body text-xs mb-1">难度</label>
            <select v-model.number="aiForm.difficulty" class="w-full bg-canvas-soft border border-hairline rounded-card px-3 py-2 text-ink text-sm">
              <option :value="1">1 - 基础</option>
              <option :value="2">2 - 中等</option>
              <option :value="3">3 - 较难</option>
              <option :value="4">4 - 困难</option>
              <option :value="5">5 - 极难</option>
            </select>
          </div>
          <div>
            <label class="block text-body text-xs mb-1">数量</label>
            <select v-model.number="aiForm.count" class="w-full bg-canvas-soft border border-hairline rounded-card px-3 py-2 text-ink text-sm">
              <option v-for="n in [3, 5, 10, 15, 20]" :key="n" :value="n">{{ n }} 道</option>
            </select>
          </div>
        </div>

        <div>
          <label class="block text-body text-xs mb-1">章节（可选，留空则随机覆盖）</label>
          <input v-model="aiForm.chapter" placeholder="如：马克思主义哲学、词汇、导数与微分" class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" />
        </div>

        <div class="bg-canvas-soft border border-hairline rounded-card p-3 text-xs text-mute space-y-1">
          <p>AI 将基于 DeepSeek 大模型自动生成符合考研大纲的题目，每道题包含：</p>
          <p>题干 + 4个选项 + 正确答案 + 详细解析</p>
          <p>生成后自动入库，可在列表中编辑或删除。</p>
        </div>

        <div class="flex gap-3 pt-1">
          <button class="btn-pill-outline cursor-target flex-1 text-sm" @click="showAiGenerate = false">取消</button>
          <button class="btn-pill-filled cursor-target flex-1 text-sm" :disabled="aiGenerating" @click="generateAiQuestions">
            {{ aiGenerating ? '生成中...（约10秒）' : '开始生成' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
