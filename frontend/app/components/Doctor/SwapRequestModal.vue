<!-- frontend/app/components/Doctor/SwapRequestModal.vue -->
<script setup>
const props = defineProps({
  modelValue: Boolean,
  shift: Object,
  type: {
    type: String,
    default: 'cancel' // 'swap' or 'cancel'
  }
})

const emit = defineEmits(['update:modelValue', 'submit'])

const comment = ref('')
const loading = ref(false)

async function submit() {
  loading.value = true
  try {
    emit('submit', {
      shiftId: props.shift?.id,
      type: props.type,
      comment: comment.value
    })
    emit('update:modelValue', false)
    comment.value = ''
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <UiModal 
    :modelValue="modelValue" 
    @update:modelValue="$emit('update:modelValue', $event)"
    :title="type === 'swap' ? 'Запрос на обмен' : 'Запрос на отмену'"
  >
    <div class="space-y-4">
      <div class="bg-base-200 rounded-lg p-4">
        <p class="text-sm text-gray-500">Смена:</p>
        <p class="font-medium">{{ shift?.date }}</p>
      </div>
      
      <div class="form-control">
        <label class="label">
          <span class="label-text">Причина / Комментарий</span>
        </label>
        <textarea 
          v-model="comment"
          class="textarea textarea-bordered h-24"
          placeholder="Укажите причину..."
        ></textarea>
      </div>
      
      <div class="flex justify-end gap-2">
        <button 
          @click="$emit('update:modelValue', false)"
          class="btn btn-ghost"
        >
          Отмена
        </button>
        <button 
          @click="submit"
          :disabled="loading"
          :class="['btn', type === 'cancel' ? 'btn-error' : 'btn-primary']"
        >
          <span v-if="loading" class="loading loading-spinner loading-sm"></span>
          Отправить заявку
        </button>
      </div>
    </div>
  </UiModal>
</template>