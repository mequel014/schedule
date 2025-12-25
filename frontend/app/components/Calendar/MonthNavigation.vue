<!-- frontend/app/components/Calendar/MonthNavigation.vue -->
<script setup>
import { MONTH_NAMES, getNextMonth, getPrevMonth } from '~/utils/dateHelpers'

const props = defineProps({
  year: Number,
  month: Number
})

const emit = defineEmits(['navigate'])

const prev = computed(() => getPrevMonth(props.year, props.month))
const next = computed(() => getNextMonth(props.year, props.month))

function navigatePrev() {
  emit('navigate', prev.value)
}

function navigateNext() {
  emit('navigate', next.value)
}

function navigateToday() {
  const now = new Date()
  emit('navigate', { year: now.getFullYear(), month: now.getMonth() + 1 })
}
</script>

<template>
  <div class="flex items-center gap-4">
    <button @click="navigatePrev" class="btn btn-circle btn-ghost">
      ←
    </button>
    
    <div class="text-center min-w-[200px]">
      <h2 class="text-xl font-bold">
        {{ MONTH_NAMES[month - 1] }} {{ year }}
      </h2>
    </div>
    
    <button @click="navigateNext" class="btn btn-circle btn-ghost">
      →
    </button>
    
    <button @click="navigateToday" class="btn btn-ghost btn-sm">
      Сегодня
    </button>
  </div>
</template>