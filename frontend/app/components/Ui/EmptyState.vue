<!-- frontend/app/components/Ui/EmptyState.vue -->
<script setup>
defineProps({
  icon: String,
  title: String,
  description: String
})
</script>

<template>
  <div class="text-center py-12">
    <div v-if="icon" class="text-6xl mb-4">{{ icon }}</div>
    <h3 v-if="title" class="text-xl font-semibold text-gray-700">{{ title }}</h3>
    <p v-if="description" class="text-gray-500 mt-2">{{ description }}</p>
    <div v-if="$slots.default" class="mt-4">
      <slot />
    </div>
  </div>
</template>