// src/composables/useLogin.js
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import api from '@/services/api'

export function useLogin() {
  const router = useRouter()

  const username = ref('')
  const password = ref('')
  const errorMessage = ref('')
  const isLoading = ref(false)

  const submitLogin = async () => {
    isLoading.value = true
    errorMessage.value = ''

    try {
      const response = await api.post('/auth/login', {
        username: username.value,
        password: password.value
      })

      if (response.data.msg === '2FA REQUIRED') {
        // Save the temporary token for 2FA verification
        localStorage.setItem('jwt', response.data.temp_token)
        router.push({ name: 'two-factor' })
      } else {
        // Direct login (if 2FA was disabled, though our backend currently requires it if set)
        const { access_token, roles } = response.data
        localStorage.setItem('jwt', access_token)
        localStorage.setItem('role', roles[0]) // Taking the first role for simplicity in the demo

        // Redirect based on role
        if (roles.includes('ADMIN')) router.push({ name: 'admin-dashboard' })
        else if (roles.includes('AUDITOR')) router.push({ name: 'auditor-dashboard' })
        else router.push({ name: 'user-dashboard' })
      }
    } catch (error) {
      if (error.response && error.response.data) {
        errorMessage.value = error.response.data.msg || 'Credenciales incorrectas.'
      } else {
        errorMessage.value = 'Error de conexión con el servidor.'
      }
    } finally {
      isLoading.value = false
    }
  }

  return { username, password, errorMessage, isLoading, submitLogin }
}