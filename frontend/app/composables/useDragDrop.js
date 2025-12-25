// frontend/app/composables/useDragDrop.js

export function useDragDrop() {
  const draggingDoctor = ref(null)
  const dragOverDate = ref(null)

  function handleDragStart(doctor, event) {
    draggingDoctor.value = doctor
    event.dataTransfer.effectAllowed = 'move'
    event.dataTransfer.setData('text/plain', doctor.id)
  }

  function handleDragEnd() {
    draggingDoctor.value = null
    dragOverDate.value = null
  }

  function handleDragOver(date, event) {
    event.preventDefault()
    event.dataTransfer.dropEffect = 'move'
    dragOverDate.value = date
  }

  function handleDragLeave() {
    dragOverDate.value = null
  }

  return {
    draggingDoctor,
    dragOverDate,
    handleDragStart,
    handleDragEnd,
    handleDragOver,
    handleDragLeave
  }
}