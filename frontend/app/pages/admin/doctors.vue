<!-- frontend/app/pages/admin/doctors.vue -->
<script setup>
definePageMeta({
  layout: 'admin'
})

const doctorsStore = useDoctorsStore()
const loading = ref(true)

onMounted(async () => {
  try {
    await doctorsStore.fetchDoctors()
  } finally {
    loading.value = false
  }
})

async function handleUpdatePriority({ userId, priority, minShifts }) {
  await doctorsStore.updateDoctorProfile(userId, {
    priority,
    min_shifts_per_month: minShifts
  })
}
</script>

<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">Врачи</h1>
    
    <UiLoading v-if="loading" size="lg" />
    
    <UiCard v-else>
      <AdminDoctorsList 
        :doctors="doctorsStore.doctors"
        @update-priority="handleUpdatePriority"
      />
    </UiCard>
  </div>
</template>