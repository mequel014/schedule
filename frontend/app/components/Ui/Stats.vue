<!-- frontend/app/components/Ui/Stats.vue -->
<script setup>
defineProps({
  stats: {
    type: Array,
    required: true
    // [{ title, value, desc?, icon?, color? }]
  }
})
</script>

<template>
  <div class="stats shadow w-full">
    <div v-for="stat in stats" :key="stat.title" class="stat">
      <div v-if="stat.icon" class="stat-figure text-3xl">{{ stat.icon }}</div>
      <div class="stat-title">{{ stat.title }}</div>
      <div :class="['stat-value', stat.color ? `text-${stat.color}` : '']">{{ stat.value }}</div>
      <div v-if="stat.desc" class="stat-desc">{{ stat.desc }}</div>
    </div>
  </div>
</template>