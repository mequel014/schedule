<!-- frontend/app/components/Ui/Alert.vue -->
<script setup>
defineProps({
  type: {
    type: String,
    default: 'info', // info, success, warning, error
    validator: (v) => ['info', 'success', 'warning', 'error'].includes(v)
  },
  dismissible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['dismiss'])
const visible = ref(true)

function dismiss() {
  visible.value = false
  emit('dismiss')
}

const alertClasses = {
  info: 'alert-info',
  success: 'alert-success',
  warning: 'alert-warning',
  error: 'alert-error'
}

const icons = {
  info: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
  success: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
  warning: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z',
  error: 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z'
}
</script>

<template>
  <div v-if="visible" :class="['alert', alertClasses[type]]">
    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="icons[type]" />
    </svg>
    <span><slot /></span>
    <button v-if="dismissible" @click="dismiss" class="btn btn-sm btn-ghost">✕</button>
  </div>
</template>