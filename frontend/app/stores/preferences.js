// frontend/app/stores/preferences.js

export const usePreferencesStore = defineStore('preferences', () => {
  const myPreferences = ref([])
  const loading = ref(false)

  async function fetchMyPreferences() {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      myPreferences.value = await $api('/api/preferences/me')
      return myPreferences.value
    } finally {
      loading.value = false
    }
  }

  async function fetchMonthPreferences(year, month) {
    const { $api } = useNuxtApp()
    return await $api(`/api/preferences/me/${year}/${month}`)
  }

  async function setPreferences(year, month, days) {
    const { $api } = useNuxtApp()
    const result = await $api('/api/preferences/me', {
      method: 'POST',
      body: { year, month, days }
    })
    await fetchMyPreferences()
    return result
  }

  async function copyFromPrevious(year, month) {
    const { $api } = useNuxtApp()
    const result = await $api(`/api/preferences/me/copy-from-previous?year=${year}&month=${month}`, {
      method: 'POST'
    })
    await fetchMyPreferences()
    return result
  }

  return {
    myPreferences,
    loading,
    fetchMyPreferences,
    fetchMonthPreferences,
    setPreferences,
    copyFromPrevious
  }
})