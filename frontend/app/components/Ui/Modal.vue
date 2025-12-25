<!-- frontend/app/components/Ui/Modal.vue -->
<script setup>
const props = defineProps({
  modelValue: Boolean,
  title: String,
  size: {
    type: String,
    default: 'md' // sm, md, lg, xl
  },
  closable: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'close'])

const sizeClasses = {
  sm: 'max-w-sm',
  md: 'max-w-md',
  lg: 'max-w-lg',
  xl: 'max-w-xl',
  '2xl': 'max-w-2xl'
}

function close() {
  if (props.closable) {
    emit('update:modelValue', false)
    emit('close')
  }
}

// Close on escape
onMounted(() => {
  const handleEscape = (e) => {
    if (e.key === 'Escape' && props.modelValue && props.closable) {
      close()
    }
  }
  window.addEventListener('keydown', handleEscape)
  onUnmounted(() => window.removeEventListener('keydown', handleEscape))
})
</script>

<template>
  <Teleport to="body">
    <div v-if="modelValue" class="modal modal-open">
      <div class="modal-backdrop" @click="close"></div>
      <div :class="['modal-box', sizeClasses[size]]">
        <button 
          v-if="closable" 
          @click="close" 
          class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
        >✕</button>
        
        <h3 v-if="title" class="font-bold text-lg mb-4">{{ title }}</h3>
        
        <slot />
        
        <div v-if="$slots.actions" class="modal-action">
          <slot name="actions" />
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.modal-backdrop {
  @apply fixed inset-0 bg-black/50;
}
</style>