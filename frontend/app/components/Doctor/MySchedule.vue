<!-- frontend/app/components/Doctor/MySchedule.vue -->
<script setup>
import { formatTime, formatDate } from '~/utils/dateHelpers'

const props = defineProps({
  schedule: Object
})

const emit = defineEmits(['requestSwap', 'requestCancel'])

const myShifts = computed(() => {
  if (!props.schedule?.days) return []
  
  const authStore = useAuthStore()
  const userId = authStore.user?.id
  
  return props.schedule.days
    .filter(day => day.shifts.some(s => s.doctor_id === userId))
    .map(day => ({
      ...day,
      myShift: day.shifts.find(s => s.doctor_id === userId)
    }))
})
</script>

<template>
  <div>
    <h3 class="text-lg font-semibold mb-4">Мои смены в этом месяце</h3>
    
    <div v-if="myShifts.length" class="space-y-3">
      <div 
        v-for="day in myShifts" 
        :key="day.date"
        class="flex items-center justify-between bg-base-100 rounded-lg p-4 shadow"
      >
        <div>
          <div class="font-medium">{{ formatDate(day.date) }}</div>
          <div class="text-sm text-gray-500">
            {{ formatTime(day.myShift.start_time) }} - {{ formatTime(day.myShift.end_time) }}
          </div>
          <div v-if="day.is_holiday" class="badge badge-error badge-sm mt-1">
            Праздник
          </div>
        </div>
        
        <div class="dropdown dropdown-end">
          <div tabindex="0" role="button" class="btn btn-ghost btn-sm">
            ⋮
          </div>
          <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
            <li>
              <button @click="emit('requestSwap', day.myShift)">
                🔄 Запросить обмен
              </button>
            </li>
            <li>
              <button @click="emit('requestCancel', day.myShift)" class="text-error">
                ❌ Запросить отмену
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>
    
    <UiEmptyState 
      v-else
      icon="📅"
      title="Нет смен"
      description="У вас нет назначенных смен в этом месяце"
    />
  </div>
</template>