<!-- frontend/app/pages/admin/index.vue -->
<script setup>
definePageMeta({
  layout: 'admin'
})

const { $api } = useNuxtApp()
const stats = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    stats.value = await $api('/api/stats/dashboard')
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">Панель управления</h1>
    
    <UiLoading v-if="loading" size="lg" />
    
    <template v-else>
      <AdminDashboardStats :stats="stats" class="mb-8" />
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <UiCard title="Быстрые действия">
          <div class="space-y-2">
            <NuxtLink to="/admin/schedule" class="btn btn-outline w-full justify-start">
              📅 Управление расписанием
            </NuxtLink>
            <NuxtLink to="/admin/doctors" class="btn btn-outline w-full justify-start">
              👨‍⚕️ Управление врачами
            </NuxtLink>
            <NuxtLink to="/admin/swap-requests" class="btn btn-outline w-full justify-start">
              🔄 Заявки на обмен
            </NuxtLink>
          </div>
        </UiCard>
        
        <UiCard title="Текущий месяц">
          <div v-if="stats">
            <p>Смен запланировано: <strong>{{ stats.shifts_this_month }}</strong></p>
            <p>Всего часов: <strong>{{ stats.total_hours }}</strong></p>
            <p>Активных врачей: <strong>{{ stats.total_doctors }}</strong></p>
          </div>
        </UiCard>
      </div>
    </template>
  </div>
</template>