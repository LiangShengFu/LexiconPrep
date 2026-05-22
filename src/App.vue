<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import NavBar from '@/components/NavBar.vue'
import AppShell from '@/components/AppShell.vue'
import AdminShell from '@/components/AdminShell.vue'
import ErrorBoundary from '@/components/ErrorBoundary.vue'
import TargetCursor from '@/components/TargetCursor.vue'
import ToastContainer from '@/components/ToastContainer.vue'

const auth = useAuthStore()
auth.initFromStorage()

const route = useRoute()

const isMarketingPage = computed(() => ['/', '/login', '/register'].includes(route.path))
const isAdminPage = computed(() => route.path.startsWith('/admin'))
</script>

<template>
  <template v-if="isMarketingPage">
    <NavBar />
    <ErrorBoundary><router-view /></ErrorBoundary>
  </template>
  <AdminShell v-else-if="isAdminPage">
    <ErrorBoundary><router-view /></ErrorBoundary>
  </AdminShell>
  <AppShell v-else>
    <ErrorBoundary><router-view /></ErrorBoundary>
  </AppShell>
  <TargetCursor :spin-duration="2" :hide-default-cursor="true" />
  <ToastContainer />
</template>
