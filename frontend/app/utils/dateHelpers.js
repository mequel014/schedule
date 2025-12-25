// frontend/app/utils/dateHelpers.js

export const MONTH_NAMES = [
  'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
  'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
]

export const WEEKDAY_NAMES = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

export const WEEKDAY_FULL = [
  'Понедельник', 'Вторник', 'Среда', 'Четверг', 
  'Пятница', 'Суббота', 'Воскресенье'
]

export function formatDate(date) {
  if (typeof date === 'string') {
    date = new Date(date)
  }
  return date.toLocaleDateString('ru-RU')
}

export function formatTime(time) {
  if (!time) return ''
  if (typeof time === 'string') {
    return time.substring(0, 5)
  }
  return time
}

export function getNextMonth(year, month) {
  if (month === 12) {
    return { year: year + 1, month: 1 }
  }
  return { year, month: month + 1 }
}

export function getPrevMonth(year, month) {
  if (month === 1) {
    return { year: year - 1, month: 12 }
  }
  return { year, month: month - 1 }
}

export function getDaysInMonth(year, month) {
  return new Date(year, month, 0).getDate()
}

export function getFirstDayOfMonth(year, month) {
  // Returns 0-6 (Mon=0, Sun=6) to match our calendar
  const day = new Date(year, month - 1, 1).getDay()
  return day === 0 ? 6 : day - 1
}