<!-- frontend/app/pages/doctor/stats.vue -->
<script setup>
import { MONTH_NAMES } from '~/utils/dateHelpers'

definePageMeta({
  layout: 'doctor'
})

const doctorsStore = useDoctorsStore()
const loading = ref(true)
const stats = ref(null)
const history = ref([])

onMounted(async () => {
  try {
    stats.value = await doctorsStore.fetchMyStats()
    history.value = await doctorsStore.fetchMyStatsHistory()
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">Моя статистика</h1>
    
    <UiLoading v-if="loading" size="lg" />
    
    <template v-else>
      <!-- Current month stats -->
      <UiStats 
        :stats="[
          { title: 'Смен в этом месяце', value: stats?.shifts_count || 0, icon: '📅' },
          { title: 'Часов в этом месяце', value: stats?.total_hours || 0, icon: '⏰' },
          { title: 'Выходных смен', value: stats?.weekend_shifts || 0, icon: '🌙' },
        ]"
        class="mb-8"
      />
      
      <!-- History -->
      <UiCard title="История по месяцам">
        <div class="overflow-x-auto">
          <table class="table">
            <thead>
              <tr>
                <th>Месяц</th>
                <th>Смен</th>
                <th>Часов</th>
                <th>Выходных</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in history" :key="`${item.year}-${item.month}`">
                <td>{{ MONTH_NAMES[item.month - 1] }} {{ item.year }}</td>
                <td>{{ item.shifts_count }}</td>
                <td>{{ item.total_hours }}</td>
                <td>{{ item.weekend_shifts }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <UiEmptyState 
          v-if="!history.length"
          icon="📊"
          title="Нет данных"
          description="История смен пока пуста"
        />
      </UiCard>
    </template>
  </div>
</template>