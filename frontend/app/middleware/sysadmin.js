// frontend/app/middleware/sysadmin.js

export default defineNuxtRouteMiddleware(async () => {
  const authStore = useAuthStore()
  
  if (!authStore.isAuthenticated) {
    return navigateTo('/login')
  }
  
  if (!authStore.user) {
    await authStore.fetchUser()
  }
  
  if (!authStore.isSysadmin) {
    return navigateTo('/admin')
  }
})