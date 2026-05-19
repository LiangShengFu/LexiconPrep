<script setup lang="ts">
import { ref } from 'vue'

const nickname = ref('Lin Chen')
const email = ref('linchen@example.com')
const dailyGoal = ref(30)
const pomodoroDuration = ref(25)
const darkMode = ref(true)
const notifications = ref(true)
const soundEffects = ref(false)
</script>

<template>
  <div class="p-8 space-y-6">
    <div>
      <p class="eyebrow-mono-sm mb-2">个人偏好</p>
      <h1 class="text-display-sm text-ink">设置</h1>
    </div>

    <div class="max-w-[600px] space-y-6">
      <!-- Profile -->
      <div class="card-xai space-y-4">
        <p class="eyebrow-mono-sm text-mute mb-2">个人信息</p>
        <div>
          <label class="block text-body text-sm mb-2">显示名称</label>
          <input
            v-model="nickname"
            type="text"
            class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink transition-colors"
          />
        </div>
        <div>
          <label class="block text-body text-sm mb-2">邮箱</label>
          <input
            v-model="email"
            type="email"
            class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink transition-colors"
          />
        </div>
      </div>

      <!-- Study Preferences -->
      <div class="card-xai space-y-4">
        <p class="eyebrow-mono-sm text-mute mb-2">学习目标</p>
        <div>
          <label class="block text-body text-sm mb-2">每日做题目标: {{ dailyGoal }} 题</label>
          <input v-model.number="dailyGoal" type="range" min="10" max="100" step="5" class="w-full accent-white" />
        </div>
        <div>
          <label class="block text-body text-sm mb-2">番茄钟时长: {{ pomodoroDuration }} 分钟</label>
          <input v-model.number="pomodoroDuration" type="range" min="15" max="60" step="5" class="w-full accent-white" />
        </div>
      </div>

      <!-- Toggles -->
      <div class="card-xai space-y-4">
        <p class="eyebrow-mono-sm text-mute mb-2">偏好设置</p>
        <div class="flex items-center justify-between py-2">
          <span class="text-body text-sm">深色模式</span>
          <button
            class="w-10 h-5 rounded-full transition-colors"
            :class="darkMode ? 'bg-ink' : 'bg-canvas-mid'"
            @click="darkMode = !darkMode"
          >
            <div class="w-4 h-4 rounded-full bg-canvas transition-transform" :class="darkMode ? 'translate-x-5' : 'translate-x-0.5'" />
          </button>
        </div>
        <div class="flex items-center justify-between py-2 border-t border-hairline">
          <span class="text-body text-sm">消息通知</span>
          <button
            class="w-10 h-5 rounded-full transition-colors"
            :class="notifications ? 'bg-ink' : 'bg-canvas-mid'"
            @click="notifications = !notifications"
          >
            <div class="w-4 h-4 rounded-full bg-canvas transition-transform" :class="notifications ? 'translate-x-5' : 'translate-x-0.5'" />
          </button>
        </div>
        <div class="flex items-center justify-between py-2 border-t border-hairline">
          <span class="text-body text-sm">音效</span>
          <button
            class="w-10 h-5 rounded-full transition-colors"
            :class="soundEffects ? 'bg-ink' : 'bg-canvas-mid'"
            @click="soundEffects = !soundEffects"
          >
            <div class="w-4 h-4 rounded-full bg-canvas transition-transform" :class="soundEffects ? 'translate-x-5' : 'translate-x-0.5'" />
          </button>
        </div>
      </div>

      <button class="btn-pill-filled text-sm px-8 py-3">保存设置</button>
    </div>
  </div>
</template>
