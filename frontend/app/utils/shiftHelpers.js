// frontend/app/utils/shiftHelpers.js

export function calculateShiftHours(startTime, endTime) {
  const [startH, startM] = startTime.split(':').map(Number)
  const [endH, endM] = endTime.split(':').map(Number)
  
  let hours
  if (endH <= startH && !(endH === startH && endM > startM)) {
    // Next day
    hours = (24 - startH - startM / 60) + (endH + endM / 60)
  } else {
    hours = (endH + endM / 60) - (startH + startM / 60)
  }
  
  return Math.round(hours * 10) / 10
}

export function isNextDay(startTime, endTime) {
  const [startH] = startTime.split(':').map(Number)
  const [endH] = endTime.split(':').map(Number)
  return endH <= startH
}

export function formatShiftTime(startTime, endTime) {
  const start = startTime.substring(0, 5)
  const end = endTime.substring(0, 5)
  const next = isNextDay(startTime, endTime) ? ' (+1)' : ''
  return `${start} - ${end}${next}`
}