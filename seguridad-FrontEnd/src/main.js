// src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Si tienes un archivo de estilos globales, lo importas aquí
// import './assets/main.css'

const app = createApp(App)
const pinia = createPinia()

// 1. Primero instalamos Pinia para que el estado global esté disponible
app.use(pinia)

// 2. Luego instalamos el Router. 
// Es crucial que sea en este orden para que el router.beforeEach 
// pueda acceder a la tienda de autenticación (authStore).
app.use(router)

// 3. Finalmente, montamos la aplicación en el div con id="app" del index.html
app.mount('#app')