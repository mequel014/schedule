<!-- frontend/app/components/Admin/Sidebar.vue -->
<script setup>
const route = useRoute()
const authStore = useAuthStore()
const swapRequestsStore = useSwapRequestsStore()

const menuItems = computed(() => {
  const items = [
    { icon: '📊', label: 'Дашборд', to: '/admin' },
    { icon: '📅', label: 'Расписание', to: '/admin/schedule' },
    { icon: '👨‍⚕️', label: 'Врачи', to: '/admin/doctors' },
    { 
      icon: '🔄', 
      label: 'Заявки на обмен', 
      to: '/admin/swap-requests',
      badge: swapRequestsStore.pendingCount
    },
  ]
  
  if (authStore.isSysadmin) {
    items.push(
      { icon: '👥', label: 'Пользователи', to: '/admin/users' }
    )
  }
  
  return items
})

function isActive(path) {
  if (path === '/admin') {
    return route.path === '/admin'
  }
  return route.path.startsWith(path)
}
</script>

<template>
  <aside class="w-64 min-h-screen bg-base-100 border-r">
    <ul class="menu p-4 gap-1">
      <li v-for="item in menuItems" :key="item.to">
        <NuxtLink 
          :to="item.to" 
          :class="{ 'active': isActive(item.to) }"
        >
          <span>{{ item.icon }}</span>
          <span class="flex-1">{{ item.label }}</span>
          <span v-if="item.badge" class="badge badge-sm badge-secondary">
            {{ item.badge }}
          </span>
        </NuxtLink>
      </li>
    </ul>
    
    <!-- Quick actions -->
    <div class="p-4 border-t mt-auto">
      <NuxtLink to="/doctor" class="btn btn-outline btn-sm w-full">
        👁️ Режим врача
      </NuxtLink>
    </div>
  </aside>
</template>