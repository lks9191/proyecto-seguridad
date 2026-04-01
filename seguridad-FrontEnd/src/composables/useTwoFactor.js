// src/composables/useTwoFactor.js
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

export function useTwoFactor() {
  const router = useRouter()
  const authStore = useAuthStore()

  const totpCode = ref('')
  const errorMessage = ref('')
  const isLoading = ref(false)

  const verifyCode = async () => {
    isLoading.value = true
    errorMessage.value = ''

    try {
      const response = await api.post('/auth/verify-2fa', {
        token: totpCode.value
      })

      const { access_token, active_role, username: userCarnet } = response.data
      authStore.login(access_token, active_role, userCarnet)

      // Redirect based on the active role
      if (active_role === 'ADMIN') router.push({ name: 'admin-dashboard' })
      else if (active_role === 'AUDITOR') router.push({ name: 'auditor-dashboard' })
      else router.push({ name: 'user-dashboard' })

    } catch (error) {
      if (error.response && error.response.data) {
        errorMessage.value = error.response.data.msg || 'Código de verificación inválido.'
      } else {
        errorMessage.value = 'Error al verificar el código.'
      }
    } finally {
      isLoading.value = false
    }
  }

  return { totpCode, errorMessage, isLoading, verifyCode }
}