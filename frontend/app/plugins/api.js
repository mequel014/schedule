// frontend/app/plugins/api.js

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const authStore = useAuthStore()

  const $api = async (url, options = {}) => {
    const headers = { ...options.headers }
    
    if (authStore.token) {
      headers.Authorization = `Bearer ${authStore.token}`
    }
    
    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json'
    }

    const response = await $fetch(`${config.public.apiBase}${url}`, {
      ...options,
      headers,
    })
    
    return response
  }

  return {
    provide: {
      api: $api
    }
  }
})