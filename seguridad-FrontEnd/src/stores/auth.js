// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // Inicializamos leyendo el localStorage por si el usuario recarga la página
  const token = ref(localStorage.getItem('jwt') || null)
  const role = ref(localStorage.getItem('role') || null)
  const carnet = ref(localStorage.getItem('carnet') || null)

  // Getter para saber si hay un usuario logueado
  const isAuthenticated = computed(() => !!token.value)

  // Acción para iniciar sesión (se llama después de verificar el 2FA exitosamente)
  function login(newToken, userRole, userCarnet) {
    token.value = newToken
    role.value = userRole
    carnet.value = userCarnet
    localStorage.setItem('jwt', newToken)
    localStorage.setItem('role', userRole)
    localStorage.setItem('carnet', userCarnet)
  }

  // Acción para cerrar sesión
  function logout() {
    token.value = null
    role.value = null
    carnet.value = null
    localStorage.removeItem('jwt')
    localStorage.removeItem('role')
    localStorage.removeItem('carnet')
  }

  return { token, role, carnet, isAuthenticated, login, logout }
})