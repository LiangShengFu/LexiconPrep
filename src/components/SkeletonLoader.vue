<script setup lang="ts">
defineProps<{ rows?: number; type?: 'card' | 'line' }>()
</script>

<template>
  <div class="space-y-4 animate-pulse">
    <div v-if="type === 'card'" class="card-xai space-y-3">
      <div class="h-4 bg-canvas-soft rounded w-1/3" />
      <div class="h-6 bg-canvas-soft rounded w-2/3" />
      <div class="h-3 bg-canvas-soft rounded w-full" />
    </div>
    <div v-else v-for="i in (rows || 3)" :key="i" class="flex items-center gap-3">
      <div class="h-3 bg-canvas-soft rounded flex-1" :style="{ width: `${60 + Math.random() * 30}%` }" />
    </div>
  </div>
</template>
