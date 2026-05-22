<script setup lang="ts">
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()
</script>

<template>
  <div class="fixed bottom-6 right-6 z-[9999] flex flex-col gap-2" role="alert" aria-live="polite">
    <div
      v-for="toast in ui.toasts"
      :key="toast.id"
      class="card-xai px-5 py-3 text-sm cursor-pointer animate-[fadeIn_0.2s_ease-out] max-w-[360px]"
      :class="{
        'border-green-500/30': toast.type === 'success',
        'border-red-500/30': toast.type === 'error',
        'border-hairline': toast.type === 'info',
      }"
      @click="ui.removeToast(toast.id)"
    >
      <span :class="{
        'text-green-400': toast.type === 'success',
        'text-red-400': toast.type === 'error',
        'text-body': toast.type === 'info',
      }">{{ toast.message }}</span>
    </div>
  </div>
</template>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
