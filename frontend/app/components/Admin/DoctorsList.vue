<!-- frontend/app/components/Admin/DoctorsList.vue -->
<script setup>
const props = defineProps({
  doctors: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['edit', 'updatePriority'])

const editingDoctor = ref(null)
const priorityInput = ref(1)
const minShiftsInput = ref(4)

function startEdit(doctor) {
  editingDoctor.value = doctor
  priorityInput.value = doctor.priority
  minShiftsInput.value = doctor.min_shifts_per_month
}

function saveEdit() {
  emit('updatePriority', {
    userId: editingDoctor.value.id,
    priority: priorityInput.value,
    minShifts: minShiftsInput.value
  })
  editingDoctor.value = null
}

function cancelEdit() {
  editingDoctor.value = null
}
</script>

<template>
  <div class="overflow-x-auto">
    <table class="table table-zebra">
      <thead>
        <tr>
          <th>Врач</th>
          <th>Email</th>
          <th>Приоритет</th>
          <th>Мин. смен</th>
          <th>Смен (месяц)</th>
          <th>Часов (месяц)</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="doctor in doctors" :key="doctor.id">
          <td>
            <div class="font-medium">{{ doctor.full_name }}</div>
          </td>
          <td>{{ doctor.email }}</td>
          <td>
            <template v-if="editingDoctor?.id === doctor.id">
              <input 
                v-model.number="priorityInput" 
                type="number" 
                min="1" 
                max="10"
                class="input input-bordered input-sm w-16"
              />
            </template>
            <template v-else>
              <UiBadge :variant="doctor.priority >= 5 ? 'primary' : 'neutral'">
                {{ doctor.priority }}
              </UiBadge>
            </template>
          </td>
          <td>
            <template v-if="editingDoctor?.id === doctor.id">
              <input 
                v-model.number="minShiftsInput" 
                type="number" 
                min="0" 
                max="15"
                class="input input-bordered input-sm w-16"
              />
            </template>
            <template v-else>
              {{ doctor.min_shifts_per_month }}
            </template>
          </td>
          <td>
            <span :class="doctor.current_month_shifts < doctor.min_shifts_per_month ? 'text-warning' : 'text-success'">
              {{ doctor.current_month_shifts }}
            </span>
          </td>
          <td>{{ doctor.current_month_hours }}ч</td>
          <td>
            <template v-if="editingDoctor?.id === doctor.id">
              <div class="flex gap-1">
                <button @click="saveEdit" class="btn btn-success btn-xs">✓</button>
                <button @click="cancelEdit" class="btn btn-ghost btn-xs">✕</button>
              </div>
            </template>
            <template v-else>
              <button @click="startEdit(doctor)" class="btn btn-ghost btn-xs">
                ✏️
              </button>
            </template>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>