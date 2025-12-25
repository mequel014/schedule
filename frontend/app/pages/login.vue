<!-- frontend/app/pages/login.vue -->
<script setup>
definePageMeta({
  layout: false
})

const authStore = useAuthStore()
const router = useRouter()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  
  try {
    await authStore.login(email.value, password.value)
    
    // Redirect based on role
    if (authStore.isAdmin) {
      router.push('/admin')
    } else {
      router.push('/doctor')
    }
  } catch (e) {
    error.value = 'Неверный email или пароль'
  } finally {
    loading.value = false
  }
}

// Redirect if already logged in
onMounted(() => {
  if (authStore.isAuthenticated) {
    router.push(authStore.isAdmin ? '/admin' : '/doctor')
  }
})
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-base-200">
    <div class="card w-96 bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title justify-center text-2xl mb-6">
          🏥 Расписание дежурств
        </h2>
        
        <form @submit.prevent="handleLogin" class="space-y-4">
          <UiAlert v-if="error" type="error">{{ error }}</UiAlert>
          
          <div class="form-control">
            <label class="label">
              <span class="label-text">Email</span>
            </label>
            <input 
              v-model="email"
              type="email"
              required
              class="input input-bordered"
              placeholder="doctor@example.com"
            />
          </div>
          
          <div class="form-control">
            <label class="label">
              <span class="label-text">Пароль</span>
            </label>
            <input 
              v-model="password"
              type="password"
              required
              class="input input-bordered"
              placeholder="••••••••"
            />
          </div>
          
          <button 
            type="submit" 
            :disabled="loading"
            class="btn btn-primary w-full"
          >
            <span v-if="loading" class="loading loading-spinner"></span>
            <span v-else>Войти</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>