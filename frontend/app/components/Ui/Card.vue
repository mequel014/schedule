<!-- frontend/app/components/Ui/Card.vue -->
<script setup>
defineProps({
  title: String,
  compact: Boolean,
  bordered: {
    type: Boolean,
    default: true
  }
})
</script>

<template>
  <div :class="['card bg-base-100 shadow-xl', { 'card-compact': compact, 'card-bordered': bordered }]">
    <div class="card-body">
      <h2 v-if="title" class="card-title">{{ title }}</h2>
      <slot />
      <div v-if="$slots.actions" class="card-actions justify-end">
        <slot name="actions" />
      </div>
    </div>
  </div>
</template>