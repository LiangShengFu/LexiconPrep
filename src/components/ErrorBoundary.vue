<script setup lang="ts">
import { ref, onErrorCaptured } from 'vue'

const hasError = ref(false)
const errorMsg = ref('')
const retryKey = ref(0)

onErrorCaptured((err: Error) => {
  hasError.value = true
  errorMsg.value = err.message || '发生了未知错误'
  return false
})

const retry = () => {
  hasError.value = false
  errorMsg.value = ''
  retryKey.value++
}
</script>

<template>
  <div v-if="hasError" class="card-xai text-center py-16 max-w-[400px] mx-auto my-20" role="alert">
    <p class="text-mute text-sm mb-2">页面出错了</p>
    <p class="text-sm text-red-400 mb-6">{{ errorMsg }}</p>
    <button class="btn-pill-outline cursor-target text-sm" @click="retry">重新加载</button>
  </div>
  <slot v-else :key="retryKey" />
</template>
