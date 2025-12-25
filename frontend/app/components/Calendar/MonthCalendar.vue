<!-- frontend/app/components/Calendar/MonthCalendar.vue -->
<script setup>
import { MONTH_NAMES, WEEKDAY_NAMES, getFirstDayOfMonth, getDaysInMonth } from '~/utils/dateHelpers'

const props = defineProps({
  schedule: {
    type: Object,
    required: true
  },
  editable: {
    type: Boolean,
    default: false
  },
  showPreferences: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['dayClick', 'shiftClick', 'dropDoctor'])

const calendarDays = computed(() => {
  if (!props.schedule?.days) return []
  
  const firstDay = getFirstDayOfMonth(props.schedule.year, props.schedule.month)
  const daysInMonth = getDaysInMonth(props.schedule.year, props.schedule.month)
  
  // Create calendar grid with empty cells for alignment
  const days = []
  
  // Add empty cells for days before month starts
  for (let i = 0; i < firstDay; i++) {
    days.push({ empty: true })
  }
  
  // Add actual days
  props.schedule.days.forEach(day => {
    days.push(day)
  })
  
  return days
})

function handleDayClick(day) {
  if (!day.empty) {
    emit('dayClick', day)
  }
}

function handleDrop(day, event) {
  if (!props.editable || day.empty) return
  
  const doctorId = event.dataTransfer.getData('text/plain')
  if (doctorId) {
    emit('dropDoctor', { day, doctorId })
  }
}
</script>

<template>
  <div class="bg-base-100 rounded-lg shadow p-4">
    <!-- Header -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold">
        {{ MONTH_NAMES[schedule.month - 1] }} {{ schedule.year }}
      </h2>
      <div class="flex gap-2">
        <UiBadge v-if="schedule.is_published" variant="success">Опубликовано</UiBadge>
        <UiBadge v-else-if="schedule.is_visible" variant="info">Видимо</UiBadge>
        <UiBadge v-else variant="warning">Черновик</UiBadge>
      </div>
    </div>
    
    <!-- Weekday headers -->
    <div class="calendar-grid mb-2">
      <div 
        v-for="(day, idx) in WEEKDAY_NAMES" 
        :key="day"
        :class="[
          'text-center font-semibold py-2',
          idx >= 5 ? 'text-orange-500' : ''
        ]"
      >
        {{ day }}
      </div>
    </div>
    
    <!-- Calendar grid -->
    <div class="calendar-grid">
      <div 
        v-for="(day, idx) in calendarDays" 
        :key="idx"
        :class="[
          'day-cell',
          { 
            'bg-transparent border-transparent': day.empty,
            'weekend': !day.empty && day.is_weekend,
            'holiday': !day.empty && day.is_holiday,
            'cursor-pointer': !day.empty && editable,
            'bg-blue-50': showPreferences && day.preferred_doctors?.length
          }
        ]"
        @click="handleDayClick(day)"
        @drop="handleDrop(day, $event)"
        @dragover.prevent
      >
        <template v-if="!day.empty">
          <!-- Day number -->
          <div class="flex justify-between items-start mb-2">
            <span :class="['text-lg font-semibold', day.is_holiday ? 'text-red-500' : '']">
              {{ new Date(day.date).getDate() }}
            </span>
            <span v-if="day.is_holiday" class="text-xs text-red-500">праздник</span>
          </div>
          
          <!-- Shifts -->
          <div class="space-y-1">
            <CalendarShiftCard 
              v-for="shift in day.shifts"
              :key="shift.id"
              :shift="shift"
              :editable="editable"
              @click="emit('shiftClick', shift)"
            />
          </div>
          
          <!-- Preferred doctors indicator -->
          <div v-if="showPreferences && day.preferred_doctors?.length" class="mt-2 text-xs text-blue-500">
            {{ day.preferred_doctors.length }} желающих
          </div>
        </template>
      </div>
    </div>
  </div>
</template>