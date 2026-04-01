// src/composables/useLogin.js
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

export function useLogin() {
  const router = useRouter()
  const authStore = useAuthStore()

  const username = ref('')
  const password = ref('')
  const role = ref('USER') // Default role selected
  const errorMessage = ref('')
  const isLoading = ref(false)

  const submitLogin = async () => {
    isLoading.value = true
    errorMessage.value = ''

    try {
      const response = await api.post('/auth/login', {
        username: username.value,
        password: password.value,
        role: role.value
      })

      if (response.data.msg === '2FA REQUIRED') {
        localStorage.setItem('jwt', response.data.temp_token)
        router.push({ name: 'two-factor' })
      } else {
        const { access_token, roles, active_role, username: userCarnet } = response.data
        authStore.login(access_token, active_role, userCarnet)

        // Redirect based on the active role
        if (active_role === 'ADMIN') router.push({ name: 'admin-dashboard' })
        else if (active_role === 'AUDITOR') router.push({ name: 'auditor-dashboard' })
        else router.push({ name: 'user-dashboard' })
      }
    } catch (error) {
      if (error.response && error.response.data) {
        errorMessage.value = error.response.data.msg || 'Credenciales o rol incorrectos.'
      } else {
        errorMessage.value = 'Error de conexión con el servidor.'
      }
    } finally {
      isLoading.value = false
    }
  }

  return { username, password, role, errorMessage, isLoading, submitLogin }
}
