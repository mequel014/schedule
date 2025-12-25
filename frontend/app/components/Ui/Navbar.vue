<!-- frontend/app/components/Ui/Navbar.vue -->
<script setup>
const authStore = useAuthStore()
const swapRequestsStore = useSwapRequestsStore()

const pendingCount = computed(() => swapRequestsStore.pendingCount)

function handleLogout() {
  authStore.logout()
}

const userMenuItems = computed(() => {
  const items = [
    { label: 'Профиль', to: '/profile' },
    { label: 'Сменить пароль', to: '/profile/password' },
  ]
  return items
})
</script>

<template>
  <div class="navbar bg-base-100 shadow-lg">
    <div class="flex-1">
      <NuxtLink to="/" class="btn btn-ghost text-xl">
        🏥 Расписание дежурств
      </NuxtLink>
    </div>
    
    <div class="flex-none gap-2" v-if="authStore.isAuthenticated">
      <!-- Admin notification badge -->
      <div v-if="authStore.isAdmin && pendingCount > 0" class="indicator">
        <span class="indicator-item badge badge-secondary">{{ pendingCount }}</span>
        <NuxtLink to="/admin/swap-requests" class="btn btn-ghost btn-circle">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
        </NuxtLink>
      </div>

      <!-- User dropdown -->
      <div class="dropdown dropdown-end">
        <div tabindex="0" role="button" class="btn btn-ghost">
          <div class="flex items-center gap-2">
            <div class="avatar placeholder">
              <div class="bg-neutral text-neutral-content rounded-full w-8">
                <span class="text-xs">{{ authStore.user?.full_name?.charAt(0) || '?' }}</span>
              </div>
            </div>
            <span class="hidden md:inline">{{ authStore.user?.full_name }}</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
        <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
          <li class="menu-title">
            <span>{{ authStore.user?.email }}</span>
          </li>
          <li v-for="item in userMenuItems" :key="item.to">
            <NuxtLink :to="item.to">{{ item.label }}</NuxtLink>
          </li>
          <li class="border-t mt-2 pt-2">
            <button @click="handleLogout" class="text-error">Выйти</button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>