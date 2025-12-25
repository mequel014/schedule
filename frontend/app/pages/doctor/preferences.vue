<!-- frontend/app/pages/doctor/preferences.vue -->
<script setup>
import { getNextMonth, MONTH_NAMES } from '~/utils/dateHelpers'

definePageMeta({
  layout: 'doctor'
})

const preferencesStore = usePreferencesStore()
const loading = ref(true)
const saving = ref(false)

// Default to next month
const now = new Date()
const nextMonth = getNextMonth(now.getFullYear(), now.getMonth() + 1)
const selectedYear = ref(nextMonth.year)
const selectedMonth = ref(nextMonth.month)
const selectedDays = ref([])

onMounted(async () => {
  await loadPreferences()
})

async function loadPreferences() {
  loading.value = true
  try {
    const prefs = await preferencesStore.fetchMonthPreferences(
      selectedYear.value, 
      selectedMonth.value
    )
    selectedDays.value = prefs?.days || []
  } finally {
    loading.value = false
  }
}

watch([selectedYear, selectedMonth], loadPreferences)

async function savePreferences() {
  saving.value = true
  try {
    await preferencesStore.setPreferences(
      selectedYear.value,
      selectedMonth.value,
      selectedDays.value
    )
    alert('Предпочтения сохранены!')
  } finally {
    saving.value = false
  }
}

async function copyFromPrevious() {
  saving.value = true
  try {
    await preferencesStore.copyFromPrevious(selectedYear.value, selectedMonth.value)
    await loadPreferences()
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">Мои предпочтения</h1>
    
    <UiCard class="mb-6">
      <p class="text-gray-600 mb-4">
        Выберите дни, в которые вы <strong>готовы дежурить</strong>. 
        Эти предпочтения будут учтены при автоматическом составлении расписания.
      </p>
      
      <div class="flex gap-4 items-center">
        <select v-model="selectedMonth" class="select select-bordered">
          <option v-for="(name, idx) in MONTH_NAMES" :key="idx" :value="idx + 1">
            {{ name }}
          </option>
        </select>
        
        <select v-model="selectedYear" class="select select-bordered">
          <option :value="now.getFullYear()">{{ now.getFullYear() }}</option>
          <option :value="now.getFullYear() + 1">{{ now.getFullYear() + 1 }}</option>
        </select>
        
        <button @click="copyFromPrevious" :disabled="saving" class="btn btn-outline btn-sm">
          📋 Скопировать из прошлого месяца
        </button>
      </div>
    </UiCard>
    
    <UiLoading v-if="loading" size="lg" />
    
    <template v-else>
      <DoctorPreferenceCalendar 
        :year="selectedYear"
        :month="selectedMonth"
        v-model:selected-days="selectedDays"
      />
      
      <div class="mt-6 flex justify-end">
        <button 
          @click="savePreferences" 
          :disabled="saving"
          class="btn btn-primary"
        >
          <span v-if="saving" class="loading loading-spinner loading-sm"></span>
          Сохранить предпочтения
        </button>
      </div>
    </template>
  </div>
</template>