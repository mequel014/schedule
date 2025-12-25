<!-- frontend/app/components/Admin/SwapRequestsList.vue -->
<script setup>
import { formatDate } from '~/utils/dateHelpers'

const props = defineProps({
  requests: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['resolve'])

const resolvingId = ref(null)
const adminComment = ref('')

const statusLabels = {
  pending: { text: 'Ожидает', class: 'badge-warning' },
  approved: { text: 'Одобрено', class: 'badge-success' },
  rejected: { text: 'Отклонено', class: 'badge-error' }
}

const typeLabels = {
  swap: 'Обмен',
  cancel: 'Отмена'
}

function startResolve(request) {
  resolvingId.value = request.id
  adminComment.value = ''
}

function resolve(status) {
  emit('resolve', {
    requestId: resolvingId.value,
    status,
    adminComment: adminComment.value
  })
  resolvingId.value = null
}
</script>

<template>
  <div class="overflow-x-auto">
    <table class="table">
      <thead>
        <tr>
          <th>Дата</th>
          <th>Врач</th>
          <th>Тип</th>
          <th>Смена</th>
          <th>Комментарий</th>
          <th>Статус</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in requests" :key="request.id" class="hover">
          <td>{{ formatDate(request.created_at) }}</td>
          <td>{{ request.requester_name }}</td>
          <td>
            <UiBadge :variant="request.request_type === 'swap' ? 'info' : 'warning'">
              {{ typeLabels[request.request_type] }}
            </UiBadge>
          </td>
          <td>{{ request.shift_date }}</td>
          <td class="max-w-xs truncate">{{ request.comment || '—' }}</td>
          <td>
            <span :class="['badge', statusLabels[request.status].class]">
              {{ statusLabels[request.status].text }}
            </span>
          </td>
          <td>
            <div v-if="request.status === 'pending'">
              <div v-if="resolvingId === request.id" class="space-y-2">
                <input 
                  v-model="adminComment" 
                  type="text" 
                  placeholder="Комментарий..."
                  class="input input-bordered input-sm w-full"
                />
                <div class="flex gap-1">
                  <button @click="resolve('approved')" class="btn btn-success btn-xs">
                    Одобрить
                  </button>
                  <button @click="resolve('rejected')" class="btn btn-error btn-xs">
                    Отклонить
                  </button>
                  <button @click="resolvingId = null" class="btn btn-ghost btn-xs">
                    ✕
                  </button>
                </div>
              </div>
              <button v-else @click="startResolve(request)" class="btn btn-primary btn-sm">
                Рассмотреть
              </button>
            </div>
            <span v-else class="text-gray-500 text-sm">
              {{ request.admin_comment || '—' }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
    
    <UiEmptyState 
      v-if="requests.length === 0"
      icon="📋"
      title="Нет заявок"
      description="Заявки на обмен или отмену смен пока отсутствуют"
    />
  </div>
</template>