<!-- frontend/app/components/Admin/DashboardStats.vue -->
<script setup>
const props = defineProps({
  stats: Object
})
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    <div class="stat bg-base-100 rounded-lg shadow">
      <div class="stat-figure text-primary text-3xl">👨‍⚕️</div>
      <div class="stat-title">Всего врачей</div>
      <div class="stat-value text-primary">{{ stats?.total_doctors || 0 }}</div>
    </div>
    
    <div class="stat bg-base-100 rounded-lg shadow">
      <div class="stat-figure text-secondary text-3xl">📅</div>
      <div class="stat-title">Смен в этом месяце</div>
      <div class="stat-value text-secondary">{{ stats?.shifts_this_month || 0 }}</div>
    </div>
    
    <div class="stat bg-base-100 rounded-lg shadow">
      <div class="stat-figure text-accent text-3xl">⏰</div>
      <div class="stat-title">Всего часов</div>
      <div class="stat-value text-accent">{{ stats?.total_hours || 0 }}</div>
    </div>
    
    <div class="stat bg-base-100 rounded-lg shadow">
      <div class="stat-figure text-warning text-3xl">🔄</div>
      <div class="stat-title">Ожидающие заявки</div>
      <div class="stat-value text-warning">{{ stats?.pending_swaps || 0 }}</div>
    </div>
  </div>
</template>