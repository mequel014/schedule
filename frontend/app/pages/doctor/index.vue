<!-- frontend/app/pages/doctor/index.vue -->
<script setup>
definePageMeta({
  layout: 'doctor'
})

const scheduleStore = useScheduleStore()
const swapRequestsStore = useSwapRequestsStore()

const loading = ref(true)
const showSwapModal = ref(false)
const selectedShift = ref(null)
const requestType = ref('cancel')

onMounted(async () => {
  try {
    await scheduleStore.fetchCurrentSchedule()
    await swapRequestsStore.fetchMyRequests()
  } finally {
    loading.value = false
  }
})

function handleRequestSwap(shift) {
  selectedShift.value = shift
  requestType.value = 'swap'
  showSwapModal.value = true
}

function handleRequestCancel(shift) {
  selectedShift.value = shift
  requestType.value = 'cancel'
  showSwapModal.value = true
}

async function handleSubmitRequest({ shiftId, type, comment }) {
  await swapRequestsStore.createRequest({
    shift_id: shiftId,
    request_type: type,
    comment
  })
}
</script>

<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">Мое расписание</h1>
    
    <UiLoading v-if="loading" size="lg" />
    
    <template v-else>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2">
          <CalendarMonthCalendar 
            v-if="scheduleStore.currentSchedule"
            :schedule="scheduleStore.currentSchedule"
          />
          <UiEmptyState 
            v-else
            icon="📅"
            title="Расписание недоступно"
            description="Расписание на этот месяц еще не опубликовано"
          />
        </div>
        
        <div>
          <DoctorMySchedule 
            :schedule="scheduleStore.currentSchedule"
            @request-swap="handleRequestSwap"
            @request-cancel="handleRequestCancel"
          />
        </div>
      </div>
    </template>
    
    <DoctorSwapRequestModal 
      v-model="showSwapModal"
      :shift="selectedShift"
      :type="requestType"
      @submit="handleSubmitRequest"
    />
  </div>
</template>