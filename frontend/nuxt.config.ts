// https://nuxt.com/docs/api/configuration/nuxt-config
// frontend/nuxt.config.ts

export default defineNuxtConfig({
  future: {
    compatibilityVersion: 4,
  },
  compatibilityDate: '2024-04-03',
  devtools: { enabled: false },
  
  modules: [
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss',
  ],
  
  css: ['~/assets/css/main.css'],
  
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000'
    }
  },
  
  app: {
    head: {
      title: 'Расписание дежурств',
      meta: [
        { name: 'description', content: 'Система управления расписанием дежурных врачей' }
      ]
    }
  }
})