<!-- frontend/app/components/Calendar/DayEditModal.vue -->
<script setup>
import { formatTime } from '~/utils/dateHelpers'

const props = defineProps({
  modelValue: Boolean,
  day: Object,
  scheduleId: String,
  doctors: Array
})

const emit = defineEmits(['update:modelValue', 'addShift', 'deleteShift', 'updateSettings'])

const selectedDoctor = ref('')
const startTime = ref('17:00')
const endTime = ref('08:00')
const isHoliday = ref(false)

watch(() => props.day, (day) => {
  if (day) {
    startTime.value = formatTime(day.default_start_time)
    endTime.value = formatTime(day.default_end_time)
    isHoliday.value = day.is_holiday
  }
}, { immediate: true })

function addShift() {
  if (!selectedDoctor.value) return
  
  emit('addShift', {
    doctorId: selectedDoctor.value,
    date: props.day.date,
    startTime: startTime.value,
    endTime: endTime.value
  })
  
  selectedDoctor.value = ''
}

function deleteShift(shiftId) {
  emit('deleteShift', shiftId)
}

function updateSettings() {
  emit('updateSettings', {
    day: new Date(props.day.date).getDate(),
    startTime: startTime.value,
    endTime: endTime.value,
    isHoliday: isHoliday.value
  })
}

const availableDoctors = computed(() => {
  const assignedIds = props.day?.shifts?.map(s => s.doctor_id) || []
  return props.doctors?.filter(d => !assignedIds.includes(d.id)) || []
})
</script>

<template>
  <UiModal 
    :modelValue="modelValue" 
    @update:modelValue="$emit('update:modelValue', $event)"
    :title="`${day?.date} - Редактирование`"
    size="lg"
  >
    <div v-if="day" class="space-y-6">
      <!-- Day settings -->
      <div class="border rounded-lg p-4">
        <h4 class="font-semibold mb-3">Настройки дня</h4>
        
        <div class="grid grid-cols-2 gap-4">
          <div class="form-control">
            <label class="label">
              <span class="label-text">Начало смены</span>
            </label>
            <input 
              v-model="startTime" 
              type="time" 
              class="input input-bordered"
            />
          </div>
          
          <div class="form-control">
            <label class="label">
              <span class="label-text">Конец смены</span>
            </label>
            <input 
              v-model="endTime" 
              type="time" 
              class="input input-bordered"
            />
          </div>
        </div>
        
        <div class="form-control mt-3">
          <label class="label cursor-pointer justify-start gap-2">
            <input v-model="isHoliday" type="checkbox" class="checkbox checkbox-sm" />
            <span class="label-text">Праздничный день</span>
          </label>
        </div>
        
        <button @click="updateSettings" class="btn btn-sm btn-outline mt-3">
          Сохранить настройки
        </button>
      </div>
      
      <!-- Current shifts -->
      <div>
        <h4 class="font-semibold mb-3">Назначенные смены</h4>
        
        <div v-if="day.shifts?.length" class="space-y-2">
          <div 
            v-for="shift in day.shifts" 
            :key="shift.id"
            class="flex items-center justify-between bg-base-200 rounded-lg p-3"
          >
            <div>
              <div class="font-medium">{{ shift.doctor_name }}</div>
              <div class="text-sm text-gray-500">
                {{ formatTime(shift.start_time) }} - {{ formatTime(shift.end_time) }}
              </div>
            </div>
            <button 
              @click="deleteShift(shift.id)"
              class="btn btn-ghost btn-sm text-error"
            >
              🗑️
            </button>
          </div>
        </div>
        <p v-else class="text-gray-500">Нет назначенных смен</p>
      </div>
      
      <!-- Add new shift -->
      <div class="border rounded-lg p-4">
        <h4 class="font-semibold mb-3">Добавить смену</h4>
        
        <div class="flex gap-2">
          <select 
            v-model="selectedDoctor" 
            class="select select-bordered flex-1"
          >
            <option value="">Выберите врача</option>
            <option 
              v-for="doctor in availableDoctors" 
              :key="doctor.id" 
              :value="doctor.id"
            >
              {{ doctor.full_name }}
            </option>
          </select>
          
          <button 
            @click="addShift" 
            :disabled="!selectedDoctor"
            class="btn btn-primary"
          >
            Добавить
          </button>
        </div>
        
        <!-- Preferred doctors -->
        <div v-if="day.preferred_doctors?.length" class="mt-3">
          <p class="text-sm text-blue-500">
            💡 Желающие: 
            {{ doctors?.filter(d => day.preferred_doctors.includes(d.id)).map(d => d.full_name).join(', ') }}
          </p>
        </div>
      </div>
    </div>
  </UiModal>
</template>