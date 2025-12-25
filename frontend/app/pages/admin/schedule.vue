<!-- frontend/app/pages/admin/schedule.vue -->
<script setup>
definePageMeta({
  layout: 'admin'
})

const scheduleStore = useScheduleStore()
const doctorsStore = useDoctorsStore()
const { $api } = useNuxtApp()

const schedule = ref(null)
const loading = ref(true)
const generating = ref(false)
const selectedDay = ref(null)
const showDayModal = ref(false)

const currentYear = ref(new Date().getFullYear())
const currentMonth = ref(new Date().getMonth() + 1)

async function loadSchedule() {
  loading.value = true
  try {
    schedule.value = await scheduleStore.fetchSchedule(currentYear.value, currentMonth.value)
  } finally {
    loading.value = false
  }
}

async function loadDoctors() {
  await doctorsStore.fetchDoctors()
}

onMounted(() => {
  loadSchedule()
  loadDoctors()
})

function handleNavigate({ year, month }) {
  currentYear.value = year
  currentMonth.value = month
  loadSchedule()
}

function handleDayClick(day) {
  selectedDay.value = day
  showDayModal.value = true
}

async function handleGenerate() {
  if (!confirm('Это заменит текущее расписание. Продолжить?')) return
  
  generating.value = true
  try {
    await scheduleStore.generateSchedule(currentYear.value, currentMonth.value)
    await loadSchedule()
  } finally {
    generating.value = false
  }
}

async function handleAddShift({ doctorId, date, startTime, endTime }) {
  // First ensure schedule exists
  let scheduleId = schedule.value?.id
  if (!scheduleId) {
    const created = await $api('/api/schedules', {
      method: 'POST',
      body: { year: currentYear.value, month: currentMonth.value }
    })
    scheduleId = created.id
  }
  
  await scheduleStore.addShift(scheduleId, {
    doctor_id: doctorId,
    date,
    start_time: startTime,
    end_time: endTime
  })
  await loadSchedule()
}

async function handleDeleteShift(shiftId) {
  await scheduleStore.deleteShift(shiftId)
  await loadSchedule()
}

async function handleUpdateSettings({ day, startTime, endTime, isHoliday }) {
  let scheduleId = schedule.value?.id
  if (!scheduleId) {
    const created = await $api('/api/schedules', {
      method: 'POST',
      body: { year: currentYear.value, month: currentMonth.value }
    })
    scheduleId = created.id
  }
  
  await scheduleStore.setDaySettings(scheduleId, {
    day,
    start_time: startTime,
    end_time: endTime,
    is_holiday: isHoliday
  })
  await loadSchedule()
}

async function toggleVisibility() {
  if (!schedule.value?.id) return
  await scheduleStore.updateScheduleVisibility(
    schedule.value.id,
    !schedule.value.is_visible,
    schedule.value.is_published
  )
  await loadSchedule()
}

async function togglePublished() {
  if (!schedule.value?.id) return
  await scheduleStore.updateScheduleVisibility(
    schedule.value.id,
    schedule.value.is_visible,
    !schedule.value.is_published
  )
  await loadSchedule()
}
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Расписание</h1>
      
      <div class="flex gap-2">
        <button 
          @click="handleGenerate"
          :disabled="generating"
          class="btn btn-primary"
        >
          <span v-if="generating" class="loading loading-spinner loading-sm"></span>
          🎲 Сгенерировать
        </button>
        
        <button 
          v-if="schedule?.id"
          @click="toggleVisibility"
          :class="['btn', schedule.is_visible ? 'btn-warning' : 'btn-outline']"
        >
          {{ schedule.is_visible ? '👁️ Скрыть' : '👁️ Показать' }}
        </button>
        
        <button 
          v-if="schedule?.id && schedule.is_visible"
          @click="togglePublished"
          :class="['btn', schedule.is_published ? 'btn-success' : 'btn-outline']"
        >
          {{ schedule.is_published ? '✓ Опубликовано' : '📢 Опубликовать' }}
        </button>
      </div>
    </div>
    
    <CalendarMonthNavigation 
      :year="currentYear"
      :month="currentMonth"
      @navigate="handleNavigate"
      class="mb-6"
    />
    
    <UiLoading v-if="loading" size="lg" />
    
    <template v-else-if="schedule">
      <CalendarMonthCalendar 
        :schedule="schedule"
        :editable="true"
        :show-preferences="true"
        @day-click="handleDayClick"
      />
    </template>
    
    <UiEmptyState 
      v-else
      icon="📅"
      title="Расписание не создано"
      description="Создайте расписание или сгенерируйте автоматически"
    >
      <button @click="handleGenerate" class="btn btn-primary">
        Сгенерировать расписание
      </button>
    </UiEmptyState>
    
    <!-- Day edit modal -->
    <CalendarDayEditModal 
      v-model="showDayModal"
      :day="selectedDay"
      :schedule-id="schedule?.id"
      :doctors="doctorsStore.doctors"
      @add-shift="handleAddShift"
      @delete-shift="handleDeleteShift"
      @update-settings="handleUpdateSettings"
    />
  </div>
</template>