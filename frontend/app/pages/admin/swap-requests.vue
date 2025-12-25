<!-- frontend/app/pages/admin/swap-requests.vue -->
<script setup>
definePageMeta({
  layout: 'admin'
})

const swapRequestsStore = useSwapRequestsStore()
const loading = ref(true)
const filter = ref('pending')

onMounted(async () => {
  await loadRequests()
})

async function loadRequests() {
  loading.value = true
  try {
    await swapRequestsStore.fetchRequests(filter.value === 'all' ? null : filter.value)
  } finally {
    loading.value = false
  }
}

watch(filter, loadRequests)

async function handleResolve({ requestId, status, adminComment }) {
  await swapRequestsStore.resolveRequest(requestId, status, adminComment)
}
</script>

<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">Заявки на обмен</h1>
    
    <div class="flex gap-2 mb-6">
      <button 
        @click="filter = 'pending'"
        :class="['btn btn-sm', filter === 'pending' ? 'btn-primary' : 'btn-outline']"
      >
        Ожидающие
      </button>
      <button 
        @click="filter = 'approved'"
        :class="['btn btn-sm', filter === 'approved' ? 'btn-success' : 'btn-outline']"
      >
        Одобренные
      </button>
      <button 
        @click="filter = 'rejected'"
        :class="['btn btn-sm', filter === 'rejected' ? 'btn-error' : 'btn-outline']"
      >
        Отклоненные
      </button>
      <button 
        @click="filter = 'all'"
        :class="['btn btn-sm', filter === 'all' ? 'btn-neutral' : 'btn-outline']"
      >
        Все
      </button>
    </div>
    
    <UiLoading v-if="loading" size="lg" />
    
    <UiCard v-else>
      <AdminSwapRequestsList 
        :requests="swapRequestsStore.requests"
        @resolve="handleResolve"
      />
    </UiCard>
  </div>
</template>