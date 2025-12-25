<!-- frontend/app/layouts/default.vue -->
<script setup>
const authStore = useAuthStore()

onMounted(async () => {
  if (authStore.isAuthenticated && !authStore.user) {
    await authStore.fetchUser()
  }
})
</script>

<template>
  <div class="min-h-screen bg-base-200">
    <UiNavbar />
    <main class="container mx-auto px-4 py-6">
      <slot />
    </main>
  </div>
</template>