<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api/client'

interface Question { id: string; type: string; content: string; options: string[]; answer: string[]; subject: string; difficulty: number; chapter: string | null }

const questions = ref<Question[]>([])
const loading = ref(true)
const search = ref('')
const filterSubject = ref('')
const showEdit = ref(false)
const editMode = ref<'create' | 'edit'>('create')
const editId = ref('')
const form = ref({ type: 'SINGLE', content: '', options: ['', '', '', ''], answer: [''], analysis: '', difficulty: 1, subject: '政治', chapter: '' })
const saving = ref(false)

const load = async () => {
  loading.value = true
  const params: any = { limit: 100 }
  if (search.value) params.search = search.value
  if (filterSubject.value) params.subject = filterSubject.value
  const { data } = await api.get('/admin/questions', { params })
  questions.value = data
  loading.value = false
}

onMounted(load)

const openCreate = () => {
  editMode.value = 'create'
  editId.value = ''
  form.value = { type: 'SINGLE', content: '', options: ['', '', '', ''], answer: [''], analysis: '', difficulty: 1, subject: '政治', chapter: '' }
  showEdit.value = true
}

const openEdit = (q: Question) => {
  editMode.value = 'edit'
  editId.value = q.id
  form.value = { type: q.type, content: q.content, options: [...q.options, ...Array(4 - q.options.length).fill('')].slice(0, 4), answer: [...q.answer], analysis: q.analysis || '', difficulty: q.difficulty, subject: q.subject, chapter: q.chapter || '' }
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
  } catch { /* */ }
  finally { saving.value = false }
}

const deleteQuestion = async (id: string) => {
  await api.delete(`/admin/questions/${id}`)
  await load()
}
</script>

<template>
  <div class="p-8 space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="eyebrow-mono-sm mb-2">管理</p>
        <h1 class="text-display-sm text-ink">题目管理</h1>
      </div>
      <button class="btn-pill-filled cursor-target text-sm" @click="openCreate">添加题目</button>
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
      <div v-for="q in questions" :key="q.id" class="card-xai flex items-start justify-between gap-4">
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
  </div>
</template>
