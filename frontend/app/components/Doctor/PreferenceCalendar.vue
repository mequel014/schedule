<!-- frontend/app/components/Doctor/PreferenceCalendar.vue -->
<script setup>
import { MONTH_NAMES, WEEKDAY_NAMES, getFirstDayOfMonth, getDaysInMonth } from '~/utils/dateHelpers'

const props = defineProps({
  year: Number,
  month: Number,
  selectedDays: {
    type: Array,
    default: () => []
  },
  disabled: Boolean
})

const emit = defineEmits(['update:selectedDays', 'toggle'])

const daysInMonth = computed(() => getDaysInMonth(props.year, props.month))
const firstDay = computed(() => getFirstDayOfMonth(props.year, props.month))

const calendarDays = computed(() => {
  const days = []
  
  // Empty cells
  for (let i = 0; i < firstDay.value; i++) {
    days.push({ empty: true })
  }
  
  // Actual days
  for (let day = 1; day <= daysInMonth.value; day++) {
    const date = new Date(props.year, props.month - 1, day)
    const dayOfWeek = date.getDay()
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6
    
    days.push({
      day,
      isWeekend,
      isSelected: props.selectedDays.includes(day)
    })
  }
  
  return days
})

function toggleDay(dayInfo) {
  if (props.disabled || dayInfo.empty) return
  
  const day = dayInfo.day
  let newSelected
  
  if (props.selectedDays.includes(day)) {
    newSelected = props.selectedDays.filter(d => d !== day)
  } else {
    newSelected = [...props.selectedDays, day].sort((a, b) => a - b)
  }
  
  emit('update:selectedDays', newSelected)
  emit('toggle', day)
}

function selectAllWeekends() {
  const weekends = []
  for (let day = 1; day <= daysInMonth.value; day++) {
    const date = new Date(props.year, props.month - 1, day)
    const dayOfWeek = date.getDay()
    if (dayOfWeek === 0 || dayOfWeek === 6) {
      weekends.push(day)
    }
  }
  emit('update:selectedDays', weekends)
}

function clearAll() {
  emit('update:selectedDays', [])
}
</script>

<template>
  <div>
    <!-- Actions -->
    <div class="flex gap-2 mb-4">
      <button @click="selectAllWeekends" :disabled="disabled" class="btn btn-sm btn-outline">
        Все выходные
      </button>
      <button @click="clearAll" :disabled="disabled" class="btn btn-sm btn-outline">
        Очистить
      </button>
      <span class="flex-1"></span>
      <span class="text-sm text-gray-500">
        Выбрано: {{ selectedDays.length }} дней
      </span>
    </div>
    
    <!-- Calendar -->
    <div class="bg-base-100 rounded-lg p-4 shadow">
      <h3 class="text-lg font-semibold text-center mb-4">
        {{ MONTH_NAMES[month - 1] }} {{ year }}
      </h3>
      
      <!-- Weekdays -->
      <div class="grid grid-cols-7 gap-1 mb-2">
        <div 
          v-for="(name, idx) in WEEKDAY_NAMES" 
          :key="name"
          :class="['text-center text-sm font-medium py-1', idx >= 5 ? 'text-orange-500' : '']"
        >
          {{ name }}
        </div>
      </div>
      
      <!-- Days -->
      <div class="grid grid-cols-7 gap-1">
        <div
          v-for="(dayInfo, idx) in calendarDays"
          :key="idx"
          :class="[
            'aspect-square flex items-center justify-center rounded-lg text-sm transition-all cursor-pointer select-none',
            {
              'invisible': dayInfo.empty,
              'bg-primary text-primary-content': !dayInfo.empty && dayInfo.isSelected,
              'bg-orange-50': !dayInfo.empty && !dayInfo.isSelected && dayInfo.isWeekend,
              'hover:bg-base-200': !dayInfo.empty && !dayInfo.isSelected && !disabled,
              'opacity-50 cursor-not-allowed': disabled
            }
          ]"
          @click="toggleDay(dayInfo)"
        >
          {{ dayInfo.day }}
        </div>
      </div>
    </div>
  </div>
</template>