// frontend/app/stores/auth.js

export const useAuthStore = defineStore('auth', () => {
  const token = ref(null)
  const user = ref(null)
  const loading = ref(false)

  // Load token from localStorage on init
  if (process.client) {
    token.value = localStorage.getItem('auth_token')
  }

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin' || user.value?.role === 'sysadmin')
  const isSysadmin = computed(() => user.value?.role === 'sysadmin')
  const isDoctor = computed(() => user.value?.role === 'doctor' || user.value?.role === 'sysadmin')

  async function login(email, password) {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      const response = await $api('/api/auth/login', {
        method: 'POST',
        body: { email, password }
      })
      token.value = response.access_token
      if (process.client) {
        localStorage.setItem('auth_token', response.access_token)
      }
      await fetchUser()
      return true
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    if (!token.value) return null
    const { $api } = useNuxtApp()
    try {
      user.value = await $api('/api/users/me')
      return user.value
    } catch (error) {
      logout()
      throw error
    }
  }

  function logout() {
    token.value = null
    user.value = null
    if (process.client) {
      localStorage.removeItem('auth_token')
    }
    navigateTo('/login')
  }

  async function changePassword(oldPassword, newPassword) {
    const { $api } = useNuxtApp()
    await $api('/api/users/me/password/change', {
      method: 'POST',
      body: { old_password: oldPassword, new_password: newPassword }
    })
  }

  return {
    token,
    user,
    loading,
    isAuthenticated,
    isAdmin,
    isSysadmin,
    isDoctor,
    login,
    logout,
    fetchUser,
    changePassword
  }
})