<!-- frontend/app/pages/profile/index.vue -->
<script setup>
definePageMeta({
  layout: 'default',
  middleware: ['auth']
})

const authStore = useAuthStore()
const { $api } = useNuxtApp()

const form = reactive({
  full_name: '',
  email: '',
  telegram_username: ''
})
const loading = ref(false)
const saved = ref(false)

onMounted(() => {
  if (authStore.user) {
    form.full_name = authStore.user.full_name
    form.email = authStore.user.email
    form.telegram_username = authStore.user.telegram_username || ''
  }
})

async function saveProfile() {
  loading.value = true
  saved.value = false
  
  try {
    await $api('/api/users/me', {
      method: 'PATCH',
      body: form
    })
    await authStore.fetchUser()
    saved.value = true
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Мой профиль</h1>
    
    <UiCard>
      <form @submit.prevent="saveProfile" class="space-y-4">
        <UiAlert v-if="saved" type="success" dismissible>
          Профиль обновлен!
        </UiAlert>
        
        <div class="form-control">
          <label class="label">
            <span class="label-text">ФИО</span>
          </label>
          <input 
            v-model="form.full_name"
            type="text"
            class="input input-bordered"
          />
        </div>
        
        <div class="form-control">
          <label class="label">
            <span class="label-text">Email</span>
          </label>
          <input 
            v-model="form.email"
            type="email"
            class="input input-bordered"
          />
        </div>
        
        <div class="form-control">
          <label class="label">
            <span class="label-text">Telegram</span>
          </label>
          <input 
            v-model="form.telegram_username"
            type="text"
            placeholder="@username"
            class="input input-bordered"
          />
        </div>
        
        <button 
          type="submit" 
          :disabled="loading"
          class="btn btn-primary"
        >
          <span v-if="loading" class="loading loading-spinner loading-sm"></span>
          Сохранить
        </button>
      </form>
    </UiCard>
  </div>
</template>