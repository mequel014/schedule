// frontend/app/stores/users.js

export const useUsersStore = defineStore('users', () => {
  const users = ref([])
  const loading = ref(false)

  async function fetchUsers(role = null) {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      const params = role ? `?role=${role}` : ''
      users.value = await $api(`/api/users${params}`)
      return users.value
    } finally {
      loading.value = false
    }
  }

  async function createUser(userData) {
    const { $api } = useNuxtApp()
    const result = await $api('/api/users', {
      method: 'POST',
      body: userData
    })
    await fetchUsers()
    return result
  }

  async function updateUser(userId, data) {
    const { $api } = useNuxtApp()
    const updated = await $api(`/api/users/${userId}`, {
      method: 'PATCH',
      body: data
    })
    const idx = users.value.findIndex(u => u.id === userId)
    if (idx !== -1) {
      users.value[idx] = updated
    }
    return updated
  }

  async function updateUserRole(userId, role) {
    const { $api } = useNuxtApp()
    return await $api(`/api/users/${userId}/role`, {
      method: 'PATCH',
      body: { role }
    })
  }

  async function resetUserPassword(userId) {
    const { $api } = useNuxtApp()
    return await $api(`/api/users/${userId}/reset-password`, {
      method: 'POST'
    })
  }

  return {
    users,
    loading,
    fetchUsers,
    createUser,
    updateUser,
    updateUserRole,
    resetUserPassword
  }
})