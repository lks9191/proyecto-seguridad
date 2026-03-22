// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // Inicializamos leyendo el localStorage por si el usuario recarga la página
  const token = ref(localStorage.getItem('jwt') || null)
  const role = ref(localStorage.getItem('role') || null)

  // Getter para saber si hay un usuario logueado
  const isAuthenticated = computed(() => !!token.value)

  // Acción para iniciar sesión (se llama después de verificar el 2FA exitosamente)
  function login(newToken, userRole) {
    token.value = newToken
    role.value = userRole
    localStorage.setItem('jwt', newToken)
    localStorage.setItem('role', userRole)
  }

  // Acción para cerrar sesión
  function logout() {
    token.value = null
    role.value = null
    localStorage.removeItem('jwt')
    localStorage.removeItem('role')
  }

  return { token, role, isAuthenticated, login, logout }
})