<!-- frontend/app/layouts/admin.vue -->
<script setup>
definePageMeta({
  middleware: ['auth', 'admin']
})

const authStore = useAuthStore()
const swapRequestsStore = useSwapRequestsStore()

onMounted(async () => {
  if (authStore.isAuthenticated) {
    await swapRequestsStore.fetchRequests('pending')
  }
})
</script>

<template>
  <div class="min-h-screen bg-base-200">
    <UiNavbar />
    <div class="flex">
      <AdminSidebar />
      <main class="flex-1 p-6">
        <slot />
      </main>
    </div>
  </div>
</template>