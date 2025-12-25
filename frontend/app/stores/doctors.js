// frontend/app/stores/doctors.js

export const useDoctorsStore = defineStore('doctors', () => {
  const doctors = ref([])
  const loading = ref(false)

  async function fetchDoctors() {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      doctors.value = await $api('/api/doctors')
      return doctors.value
    } finally {
      loading.value = false
    }
  }

  async function updateDoctorProfile(userId, data) {
    const { $api } = useNuxtApp()
    const updated = await $api(`/api/doctors/${userId}/profile`, {
      method: 'PATCH',
      body: data
    })
    // Update local state
    const idx = doctors.value.findIndex(d => d.id === userId)
    if (idx !== -1) {
      doctors.value[idx] = { ...doctors.value[idx], ...data }
    }
    return updated
  }

  async function fetchMyStats(year, month) {
    const { $api } = useNuxtApp()
    const params = new URLSearchParams()
    if (year) params.set('year', year)
    if (month) params.set('month', month)
    return await $api(`/api/doctors/me/stats?${params.toString()}`)
  }

  async function fetchMyStatsHistory() {
    const { $api } = useNuxtApp()
    return await $api('/api/doctors/me/stats/history')
  }

  return {
    doctors,
    loading,
    fetchDoctors,
    updateDoctorProfile,
    fetchMyStats,
    fetchMyStatsHistory
  }
})