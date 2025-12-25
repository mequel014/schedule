<!-- frontend/app/components/Doctor/Sidebar.vue -->
<script setup>
const route = useRoute()

const menuItems = [
  { icon: '📅', label: 'Мое расписание', to: '/doctor' },
  { icon: '✋', label: 'Мои предпочтения', to: '/doctor/preferences' },
  { icon: '🔄', label: 'Мои заявки', to: '/doctor/swap-requests' },
  { icon: '📊', label: 'Статистика', to: '/doctor/stats' },
]

function isActive(path) {
  if (path === '/doctor') {
    return route.path === '/doctor'
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
          {{ item.label }}
        </NuxtLink>
      </li>
    </ul>
  </aside>
</template>