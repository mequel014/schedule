// frontend/app/stores/schedule.js

export const useScheduleStore = defineStore('schedule', () => {
  const currentSchedule = ref(null)
  const nextSchedule = ref(null)
  const loading = ref(false)
  const selectedMonth = ref({ year: null, month: null })

  async function fetchCurrentSchedule() {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      currentSchedule.value = await $api('/api/schedules/current')
      return currentSchedule.value
    } finally {
      loading.value = false
    }
  }

  async function fetchNextSchedule() {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      nextSchedule.value = await $api('/api/schedules/next')
      return nextSchedule.value
    } finally {
      loading.value = false
    }
  }

  async function fetchSchedule(year, month) {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      const schedule = await $api(`/api/schedules/${year}/${month}`)
      selectedMonth.value = { year, month }
      return schedule
    } finally {
      loading.value = false
    }
  }

  async function generateSchedule(year, month, seed = null) {
    const { $api } = useNuxtApp()
    const url = seed 
      ? `/api/schedules/${year}/${month}/generate?seed=${seed}`
      : `/api/schedules/${year}/${month}/generate`
    return await $api(url, { method: 'POST' })
  }

  async function updateScheduleVisibility(scheduleId, isVisible, isPublished) {
    const { $api } = useNuxtApp()
    return await $api(`/api/schedules/${scheduleId}`, {
      method: 'PATCH',
      body: { is_visible: isVisible, is_published: isPublished }
    })
  }

  async function addShift(scheduleId, shiftData) {
    const { $api } = useNuxtApp()
    return await $api(`/api/schedules/${scheduleId}/shifts`, {
      method: 'POST',
      body: shiftData
    })
  }

  async function updateShift(shiftId, data) {
    const { $api } = useNuxtApp()
    return await $api(`/api/schedules/shifts/${shiftId}`, {
      method: 'PATCH',
      body: data
    })
  }

  async function deleteShift(shiftId) {
    const { $api } = useNuxtApp()
    return await $api(`/api/schedules/shifts/${shiftId}`, {
      method: 'DELETE'
    })
  }

  async function setDaySettings(scheduleId, dayData) {
    const { $api } = useNuxtApp()
    return await $api(`/api/schedules/${scheduleId}/day-settings`, {
      method: 'POST',
      body: dayData
    })
  }

  return {
    currentSchedule,
    nextSchedule,
    loading,
    selectedMonth,
    fetchCurrentSchedule,
    fetchNextSchedule,
    fetchSchedule,
    generateSchedule,
    updateScheduleVisibility,
    addShift,
    updateShift,
    deleteShift,
    setDaySettings
  }
})