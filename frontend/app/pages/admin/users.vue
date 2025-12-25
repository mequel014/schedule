<!-- frontend/app/pages/admin/users.vue -->
<script setup>
definePageMeta({
  layout: 'admin',
  middleware: ['sysadmin']
})

const usersStore = useUsersStore()
const loading = ref(true)
const showCreateModal = ref(false)

onMounted(async () => {
  try {
    await usersStore.fetchUsers()
  } finally {
    loading.value = false
  }
})

async function handleResetPassword(userId) {
  if (!confirm('Сбросить пароль пользователя?')) return
  
  const result = await usersStore.resetUserPassword(userId)
  alert(`Новый пароль: ${result.password}`)
}

async function handleToggleActive(user) {
  await usersStore.updateUser(user.id, { is_active: !user.is_active })
}
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Пользователи</h1>
      <button @click="showCreateModal = true" class="btn btn-primary">
        + Добавить пользователя
      </button>
    </div>
    
    <UiLoading v-if="loading" size="lg" />
    
    <UiCard v-else>
      <div class="overflow-x-auto">
        <table class="table">
          <thead>
            <tr>
              <th>ФИО</th>
              <th>Email</th>
              <th>Роль</th>
              <th>Статус</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in usersStore.users" :key="user.id">
              <td>{{ user.full_name }}</td>
              <td>{{ user.email }}</td>
              <td>
                <UiBadge :variant="user.role === 'admin' ? 'primary' : 'neutral'">
                  {{ user.role }}
                </UiBadge>
              </td>
              <td>
                <UiBadge :variant="user.is_active ? 'success' : 'error'">
                  {{ user.is_active ? 'Активен' : 'Неактивен' }}
                </UiBadge>
              </td>
              <td>
                <div class="flex gap-1">
                  <button 
                    @click="handleToggleActive(user)"
                    class="btn btn-ghost btn-xs"
                  >
                    {{ user.is_active ? '🔒' : '🔓' }}
                  </button>
                  <button 
                    @click="handleResetPassword(user.id)"
                    class="btn btn-ghost btn-xs"
                  >
                    🔑
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </UiCard>
    
    <AdminUserCreateModal 
      v-model="showCreateModal"
      @created="usersStore.fetchUsers()"
    />
  </div>
</template>