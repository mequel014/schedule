<!-- frontend/app/components/Admin/UserCreateModal.vue -->
<script setup>
const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'created'])

const loading = ref(false)
const error = ref('')

const form = reactive({
  email: '',
  full_name: '',
  telegram_username: '',
  role: 'doctor',
  priority: 1,
  min_shifts_per_month: 4
})

const usersStore = useUsersStore()

async function submit() {
  error.value = ''
  loading.value = true
  
  try {
    const result = await usersStore.createUser(form)
    emit('created', result)
    emit('update:modelValue', false)
    resetForm()
  } catch (e) {
    error.value = e.data?.detail || 'Ошибка создания пользователя'
  } finally {
    loading.value = false
  }
}

function resetForm() {
  form.email = ''
  form.full_name = ''
  form.telegram_username = ''
  form.role = 'doctor'
  form.priority = 1
  form.min_shifts_per_month = 4
}

function close() {
  emit('update:modelValue', false)
  resetForm()
}
</script>

<template>
  <UiModal :modelValue="modelValue" @update:modelValue="$emit('update:modelValue', $event)" title="Новый пользователь" size="lg">
    <form @submit.prevent="submit" class="space-y-4">
      <UiAlert v-if="error" type="error">{{ error }}</UiAlert>
      
      <div class="form-control">
        <label class="label">
          <span class="label-text">Email *</span>
        </label>
        <input 
          v-model="form.email" 
          type="email" 
          required 
          class="input input-bordered"
          placeholder="doctor@example.com"
        />
      </div>
      
      <div class="form-control">
        <label class="label">
          <span class="label-text">ФИО *</span>
        </label>
        <input 
          v-model="form.full_name" 
          type="text" 
          required 
          class="input input-bordered"
          placeholder="Иванов Иван Иванович"
        />
      </div>
      
      <div class="form-control">
        <label class="label">
          <span class="label-text">Telegram username</span>
        </label>
        <input 
          v-model="form.telegram_username" 
          type="text" 
          class="input input-bordered"
          placeholder="@username"
        />
      </div>
      
      <div class="form-control">
        <label class="label">
          <span class="label-text">Роль</span>
        </label>
        <select v-model="form.role" class="select select-bordered">
          <option value="doctor">Врач</option>
          <option value="admin">Администратор</option>
        </select>
      </div>
      
      <div v-if="form.role === 'doctor'" class="grid grid-cols-2 gap-4">
        <div class="form-control">
          <label class="label">
            <span class="label-text">Приоритет</span>
          </label>
          <input 
            v-model.number="form.priority" 
            type="number" 
            min="1" 
            max="10"
            class="input input-bordered"
          />
        </div>
        
        <div class="form-control">
          <label class="label">
            <span class="label-text">Мин. смен в месяц</span>
          </label>
          <input 
            v-model.number="form.min_shifts_per_month" 
            type="number" 
            min="0" 
            max="15"
            class="input input-bordered"
          />
        </div>
      </div>
      
      <div class="flex justify-end gap-2 pt-4">
        <button type="button" @click="close" class="btn btn-ghost">Отмена</button>
        <button type="submit" :disabled="loading" class="btn btn-primary">
          <span v-if="loading" class="loading loading-spinner loading-sm"></span>
          Создать
        </button>
      </div>
    </form>
  </UiModal>
</template>