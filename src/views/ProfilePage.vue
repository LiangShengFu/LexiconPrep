<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import api from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

const auth = useAuthStore()

const nickname = ref('')
const email = ref('')
const avatar = ref('')
const streakDays = ref(0)
const profileSaving = ref(false)
const checkedIn = ref(false)

// Calendar
const today = new Date()
const currentMonth = ref(today.getMonth())
const currentYear = ref(today.getFullYear())
const checkinDates = ref<Set<string>>(new Set())
const monthNames = ['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月']
const daysInMonth = computed(() => new Date(currentYear.value, currentMonth.value + 1, 0).getDate())
const firstDayOfMonth = computed(() => new Date(currentYear.value, currentMonth.value, 1).getDay())
const calendarDays = computed(() => {
  const days = []
  for (let i = 0; i < firstDayOfMonth.value; i++) days.push(null)
  for (let d = 1; d <= daysInMonth.value; d++) {
    const ds = `${currentYear.value}-${String(currentMonth.value + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`
    days.push({ day: d, date: ds, checked: checkinDates.value.has(ds), isToday: ds === today.toISOString().slice(0, 10) })
  }
  return days
})
const prevMonth = () => { if (currentMonth.value === 0) { currentMonth.value = 11; currentYear.value-- } else currentMonth.value-- }
const nextMonth = () => { if (currentMonth.value === 11) { currentMonth.value = 0; currentYear.value++ } else currentMonth.value++ }

// Password
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const passwordSaving = ref(false)

const passwordStrength = computed(() => {
  const p = newPassword.value
  if (!p) return { level: 0, label: '', color: '' }
  let score = 0
  if (p.length >= 8) score++
  if (p.length >= 12) score++
  if (/[A-Z]/.test(p)) score++
  if (/[0-9]/.test(p)) score++
  if (/[^A-Za-z0-9]/.test(p)) score++
  if (score <= 1) return { level: 1, label: '弱', color: '#ee0000' }
  if (score <= 2) return { level: 2, label: '一般', color: '#f5a623' }
  if (score <= 3) return { level: 3, label: '较好', color: '#50e3c2' }
  return { level: 4, label: '强', color: '#00d992' }
})

const changePassword = async () => {
  if (newPassword.value !== confirmPassword.value) { useUiStore().addToast('两次密码不一致', 'error'); return }
  if (newPassword.value.length < 6) { useUiStore().addToast('新密码至少6位', 'error'); return }
  passwordSaving.value = true
  try {
    await api.put('/users/me/password', { current_password: currentPassword.value, new_password: newPassword.value })
    useUiStore().addToast('密码已修改', 'success')
    currentPassword.value = ''; newPassword.value = ''; confirmPassword.value = ''
  } catch (e: any) { useUiStore().addToast(e.response?.data?.detail || '修改失败', 'error') }
  finally { passwordSaving.value = false }
}

// Avatar upload
const avatarUploading = ref(false)
const handleAvatarUpload = async (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  avatarUploading.value = true
  try {
    const reader = new FileReader()
    reader.onload = async (ev) => {
      const base64 = ev.target?.result as string
      const { data } = await api.put('/users/me', { avatar: base64 })
      auth.user = data; localStorage.setItem('user', JSON.stringify(data))
      avatar.value = base64; useUiStore().addToast('头像已更新', 'success')
      avatarUploading.value = false
    }
    reader.readAsDataURL(file)
  } catch { avatarUploading.value = false; useUiStore().addToast('上传失败', 'error') }
}

onMounted(async () => {
  if (auth.user) { nickname.value = auth.user.nickname; email.value = auth.user.email; avatar.value = auth.user.avatar || '' }
  try {
    const { data } = await api.get('/stats/overview')
    streakDays.value = data.streak_days
  } catch { /* */ }
  const stored = localStorage.getItem('checkin_dates')
  if (stored) checkinDates.value = new Set(JSON.parse(stored))
  checkedIn.value = checkinDates.value.has(today.toISOString().slice(0, 10))
})

const saveProfile = async () => {
  profileSaving.value = true
  try {
    const { data } = await api.put('/users/me', { nickname: nickname.value })
    auth.user = data; localStorage.setItem('user', JSON.stringify(data))
    useUiStore().addToast('已保存', 'success')
  } catch { useUiStore().addToast('保存失败', 'error') }
  finally { profileSaving.value = false }
}

const checkIn = () => {
  const tds = today.toISOString().slice(0, 10)
  if (checkinDates.value.has(tds)) return
  const updated = new Set(checkinDates.value); updated.add(tds)
  checkinDates.value = updated
  localStorage.setItem('checkin_dates', JSON.stringify([...updated]))
  streakDays.value++; checkedIn.value = true
  useUiStore().addToast('打卡成功！连续 ' + streakDays.value + ' 天', 'success')
}
</script>

<template>
  <div class="p-8 space-y-8">
    <div>
      <p class="eyebrow-mono-sm mb-2">{{ auth.user?.nickname }}</p>
      <h1 class="text-display-sm text-ink">个人主页</h1>
    </div>

    <!-- Row 1: Avatar + Calendar -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Avatar + Check-in -->
      <div class="card-xai space-y-4 flex flex-col items-center text-center">
        <label class="cursor-target relative group">
          <div v-if="avatar" class="w-24 h-24 rounded-full border-2 border-hairline overflow-hidden">
            <img :src="avatar" class="w-full h-full object-cover" />
          </div>
          <div v-else class="w-24 h-24 rounded-full bg-canvas-soft border-2 border-hairline flex items-center justify-center text-3xl text-mute">
            {{ nickname?.[0] || '?' }}
          </div>
          <div class="absolute inset-0 rounded-full bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
            <span class="text-white text-xs">{{ avatarUploading ? '上传中...' : '更换' }}</span>
          </div>
          <input type="file" accept="image/*" class="hidden" @change="handleAvatarUpload" />
        </label>
        <div>
          <p class="text-ink text-lg">{{ nickname }}</p>
          <p class="text-mute text-sm">{{ email }}</p>
          <p class="text-mute text-xs mt-2">连续打卡 <span class="text-ink">{{ streakDays }}</span> 天</p>
        </div>
        <button class="btn-pill-filled cursor-target text-sm px-6 py-2.5" :class="{ 'opacity-50': checkedIn }" :disabled="checkedIn" @click="checkIn">
          {{ checkedIn ? '已打卡' : '今日打卡' }}
        </button>
      </div>

      <!-- Calendar -->
      <div class="card-xai lg:col-span-2">
        <div class="flex items-center justify-between mb-4">
          <span class="eyebrow-mono-sm text-mute">打卡日历</span>
          <div class="flex items-center gap-4">
            <button class="text-mute text-sm hover:text-ink cursor-target" @click="prevMonth">&larr;</button>
            <span class="text-ink text-sm">{{ currentYear }} {{ monthNames[currentMonth] }}</span>
            <button class="text-mute text-sm hover:text-ink cursor-target" @click="nextMonth">&rarr;</button>
          </div>
        </div>
        <div class="grid grid-cols-7 gap-1 text-center mb-2">
          <span v-for="d in ['日','一','二','三','四','五','六']" :key="d" class="text-mute text-xs py-1">{{ d }}</span>
        </div>
        <div class="grid grid-cols-7 gap-1">
          <div v-for="(d, i) in calendarDays" :key="i" class="aspect-square flex items-center justify-center">
            <div v-if="d" class="w-9 h-9 rounded-full flex items-center justify-center text-xs transition-colors"
              :class="d.checked ? 'bg-ink text-canvas' : d.isToday ? 'border border-ink text-ink' : 'text-body'">
              {{ d.day }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Row 2: Profile + Password -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="card-xai space-y-4">
        <p class="eyebrow-mono-sm text-mute">个人信息</p>
        <div>
          <label class="block text-body text-sm mb-2">昵称</label>
          <input v-model="nickname" type="text" placeholder="你的昵称" class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" />
        </div>
        <div>
          <label class="block text-body text-sm mb-2">邮箱</label>
          <input :value="email" type="email" disabled class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-mute text-sm opacity-60 cursor-not-allowed" />
        </div>
        <button class="btn-pill-filled cursor-target text-sm px-6 py-2.5" :disabled="profileSaving" @click="saveProfile">{{ profileSaving ? '保存中...' : '保存' }}</button>
      </div>

      <div class="card-xai space-y-4">
        <p class="eyebrow-mono-sm text-mute">修改密码</p>
        <div>
          <label class="block text-body text-sm mb-2">当前密码</label>
          <input v-model="currentPassword" type="password" placeholder="输入当前密码" class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" />
        </div>
        <div>
          <label class="block text-body text-sm mb-2">新密码</label>
          <input v-model="newPassword" type="password" placeholder="至少6位" class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" />
          <div v-if="newPassword" class="flex items-center gap-2 mt-2">
            <div class="flex-1 h-1 bg-canvas-soft rounded-full overflow-hidden">
              <div class="h-full rounded-full transition-all duration-300" :style="{ width: passwordStrength.level * 25 + '%', backgroundColor: passwordStrength.color }" />
            </div>
            <span class="text-xs" :style="{ color: passwordStrength.color }">{{ passwordStrength.label }}</span>
          </div>
        </div>
        <div>
          <label class="block text-body text-sm mb-2">确认新密码</label>
          <input v-model="confirmPassword" type="password" placeholder="再次输入" class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" />
        </div>
        <button class="btn-pill-filled cursor-target text-sm px-6 py-2.5" :disabled="passwordSaving" @click="changePassword">{{ passwordSaving ? '修改中...' : '修改密码' }}</button>
      </div>
    </div>

    <!-- Row 3: Quick links -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <button class="card-xai cursor-target text-center py-6 hover:border-ink transition-colors" @click="$router.push('/library')">
        <p class="text-ink text-sm">资源库</p>
        <p class="text-mute text-xs mt-1">学习资料</p>
      </button>
      <button class="card-xai cursor-target text-center py-6 hover:border-ink transition-colors" @click="$router.push('/exam')">
        <p class="text-ink text-sm">做题</p>
        <p class="text-mute text-xs mt-1">专注练习</p>
      </button>
      <button class="card-xai cursor-target text-center py-6 hover:border-ink transition-colors" @click="$router.push('/flashcards')">
        <p class="text-ink text-sm">闪卡</p>
        <p class="text-mute text-xs mt-1">间隔复习</p>
      </button>
      <button class="card-xai cursor-target text-center py-6 hover:border-ink transition-colors" @click="$router.push('/community')">
        <p class="text-ink text-sm">社区</p>
        <p class="text-mute text-xs mt-1">学友动态</p>
      </button>
    </div>
  </div>
</template>
