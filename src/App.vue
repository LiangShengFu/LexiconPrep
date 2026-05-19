<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import NavBar from '@/components/NavBar.vue'
import AppShell from '@/components/AppShell.vue'
import ToastContainer from '@/components/ToastContainer.vue'

const auth = useAuthStore()
auth.initFromStorage()

const route = useRoute()

const isMarketingPage = computed(() => {
  const marketingRoutes = ['/', '/login', '/register']
  return marketingRoutes.includes(route.path)
})
</script>

<template>
  <NavBar v-if="isMarketingPage" />
  <AppShell v-else>
    <router-view />
  </AppShell>
  <div v-if="isMarketingPage">
    <router-view />
  </div>
  <ToastContainer />
</template>
