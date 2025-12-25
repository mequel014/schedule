<!-- frontend/app/pages/index.vue -->
<script setup>
const authStore = useAuthStore()

definePageMeta({
  middleware: ['auth']
})

// Redirect based on role
onMounted(() => {
  if (authStore.isAdmin) {
    navigateTo('/admin')
  } else {
    navigateTo('/doctor')
  }
})
</script>

<template>
  <div class="flex items-center justify-center min-h-[50vh]">
    <UiLoading size="lg" text="Загрузка..." />
  </div>
</template>