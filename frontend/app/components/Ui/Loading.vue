<!-- frontend/app/components/Ui/Loading.vue -->
<script setup>
defineProps({
  size: {
    type: String,
    default: 'md' // xs, sm, md, lg
  },
  text: String
})

const sizeClasses = {
  xs: 'loading-xs',
  sm: 'loading-sm',
  md: 'loading-md',
  lg: 'loading-lg'
}
</script>

<template>
  <div class="flex items-center justify-center gap-2">
    <span :class="['loading loading-spinner', sizeClasses[size]]"></span>
    <span v-if="text">{{ text }}</span>
  </div>
</template>