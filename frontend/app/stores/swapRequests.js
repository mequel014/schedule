// frontend/app/stores/swapRequests.js

export const useSwapRequestsStore = defineStore('swapRequests', () => {
  const requests = ref([])
  const myRequests = ref([])
  const loading = ref(false)

  async function fetchRequests(status = null) {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      const params = status ? `?status=${status}` : ''
      requests.value = await $api(`/api/swap-requests${params}`)
      return requests.value
    } finally {
      loading.value = false
    }
  }

  async function fetchMyRequests() {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      myRequests.value = await $api('/api/swap-requests/me')
      return myRequests.value
    } finally {
      loading.value = false
    }
  }

  async function createRequest(data) {
    const { $api } = useNuxtApp()
    const result = await $api('/api/swap-requests', {
      method: 'POST',
      body: data
    })
    await fetchMyRequests()
    return result
  }

  async function resolveRequest(requestId, status, adminComment = null) {
    const { $api } = useNuxtApp()
    const result = await $api(`/api/swap-requests/${requestId}`, {
      method: 'PATCH',
      body: { status, admin_comment: adminComment }
    })
    await fetchRequests()
    return result
  }

  const pendingCount = computed(() => 
    requests.value.filter(r => r.status === 'pending').length
  )

  return {
    requests,
    myRequests,
    loading,
    pendingCount,
    fetchRequests,
    fetchMyRequests,
    createRequest,
    resolveRequest
  }
})