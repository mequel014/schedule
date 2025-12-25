// frontend/app/middleware/auth.js

export default defineNuxtRouteMiddleware(async (to) => {
  const authStore = useAuthStore()
  
  // Skip for login page
  if (to.path === '/login') {
    return
  }
  
  // Check if authenticated
  if (!authStore.isAuthenticated) {
    return navigateTo('/login')
  }
  
  // Fetch user if not loaded
  if (!authStore.user) {
    try {
      await authStore.fetchUser()
    } catch (error) {
      return navigateTo('/login')
    }
  }
})