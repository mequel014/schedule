<!-- frontend/app/pages/profile/password.vue -->
<script setup>
definePageMeta({
  layout: 'default',
  middleware: ['auth']
})

const authStore = useAuthStore()

const form = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const error = ref('')
const loading = ref(false)
const success = ref(false)

async function changePassword() {
  error.value = ''
  success.value = false
  
  if (form.newPassword !== form.confirmPassword) {
    error.value = 'Пароли не совпадают'
    return
  }
  
  if (form.newPassword.length < 6) {
    error.value = 'Пароль должен быть не менее 6 символов'
    return
  }
  
  loading.value = true
  
  try {
    await authStore.changePassword(form.oldPassword, form.newPassword)
    success.value = true
    form.oldPassword = ''
    form.newPassword = ''
    form.confirmPassword = ''
  } catch (e) {
    error.value = 'Неверный текущий пароль'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Смена пароля</h1>
    
    <UiCard>
      <form @submit.prevent="changePassword" class="space-y-4">
        <UiAlert v-if="error" type="error">{{ error }}</UiAlert>
        <UiAlert v-if="success" type="success">Пароль успешно изменен!</UiAlert>
        
        <div class="form-control">
          <label class="label">
            <span class="label-text">Текущий пароль</span>
          </label>
          <input 
            v-model="form.oldPassword"
            type="password"
            required
            class="input input-bordered"
          />
        </div>
        
        <div class="form-control">
          <label class="label">
            <span class="label-text">Новый пароль</span>
          </label>
          <input 
            v-model="form.newPassword"
            type="password"
            required
            class="input input-bordered"
          />
        </div>
        
        <div class="form-control">
          <label class="label">
            <span class="label-text">Подтвердите пароль</span>
          </label>
          <input 
            v-model="form.confirmPassword"
            type="password"
            required
            class="input input-bordered"
          />
        </div>
        
        <button 
          type="submit"
          :disabled="loading"
          class="btn btn-primary"
        >
          <span v-if="loading" class="loading loading-spinner loading-sm"></span>
          Сменить пароль
        </button>
      </form>
    </UiCard>
  </div>
</template>