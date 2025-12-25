<!-- frontend/app/components/Calendar/ShiftCard.vue -->
<script setup>
import { formatTime } from '~/utils/dateHelpers'

const props = defineProps({
  shift: {
    type: Object,
    required: true
  },
  editable: {
    type: Boolean,
    default: false
  }
})

const doctorColor = computed(() => {
  // Simple hash-based color
  const colors = [
    'bg-blue-100 text-blue-800',
    'bg-green-100 text-green-800',
    'bg-purple-100 text-purple-800',
    'bg-pink-100 text-pink-800',
    'bg-yellow-100 text-yellow-800',
    'bg-indigo-100 text-indigo-800'
  ]
  const hash = props.shift.doctor_id?.split('').reduce((a, c) => a + c.charCodeAt(0), 0) || 0
  return colors[hash % colors.length]
})
</script>

<template>
  <div 
    :class="['doctor-card', doctorColor, { 'hover:shadow': editable }]"
  >
    <div class="font-medium truncate">{{ shift.doctor_name || 'Врач' }}</div>
    <div class="text-xs opacity-75">
      {{ formatTime(shift.start_time) }} - {{ formatTime(shift.end_time) }}
    </div>
  </div>
</template>