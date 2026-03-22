// src/composables/useRegister.js
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import api from '@/services/api'

export function useRegister() {
  const router = useRouter()

  const username = ref('')
  const email = ref('')
  const password = ref('')
  const confirmPassword = ref('')

  const errorMessage = ref('')
  const isLoading = ref(false)

  const submitRegister = async () => {
    isLoading.value = true
    errorMessage.value = ''

    if (password.value !== confirmPassword.value) {
      errorMessage.value = 'Las contraseñas no coinciden.'
      isLoading.value = false
      return
    }

    try {
      await api.post('/auth/register', {
        username: username.value,
        email: email.value,
        password: password.value
      })

      alert('Registro exitoso. Ahora puedes iniciar sesión.')
      router.push({ name: 'login' })

    } catch (error) {
      if (error.response && error.response.data) {
        errorMessage.value = error.response.data.msg || 'Error al registrar usuario.'
      } else {
        errorMessage.value = 'Error al conectar con el servidor.'
      }
    } finally {
      isLoading.value = false
    }
  }

  return {
    username,
    email,
    password,
    confirmPassword,
    errorMessage,
    isLoading,
    submitRegister
  }
}