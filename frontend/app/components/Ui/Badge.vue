<!-- frontend/app/components/Ui/Badge.vue -->
<script setup>
defineProps({
  variant: {
    type: String,
    default: 'neutral', // primary, secondary, accent, neutral, info, success, warning, error
  },
  size: {
    type: String,
    default: 'md' // xs, sm, md, lg
  },
  outline: Boolean
})

const variantClasses = {
  primary: 'badge-primary',
  secondary: 'badge-secondary',
  accent: 'badge-accent',
  neutral: 'badge-neutral',
  info: 'badge-info',
  success: 'badge-success',
  warning: 'badge-warning',
  error: 'badge-error',
  ghost: 'badge-ghost'
}

const sizeClasses = {
  xs: 'badge-xs',
  sm: 'badge-sm',
  md: '',
  lg: 'badge-lg'
}
</script>

<template>
  <span :class="[
    'badge',
    variantClasses[variant],
    sizeClasses[size],
    { 'badge-outline': outline }
  ]">
    <slot />
  </span>
</template>