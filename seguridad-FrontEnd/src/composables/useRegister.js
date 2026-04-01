// src/composables/useRegister.js
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import api from '@/services/api'

export function useRegister() {
  const router = useRouter()

  const carnet = ref('')
  const names = ref('')
  const paternal_surname = ref('')
  const maternal_surname = ref('')
  const email = ref('')
  const password = ref('')
  const confirmPassword = ref('')
  const registrationSuccess = ref(false)

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
        carnet: carnet.value,
        names: names.value,
        paternal_surname: paternal_surname.value,
        maternal_surname: maternal_surname.value,
        email: email.value,
        password: password.value
      })

      registrationSuccess.value = true
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
    carnet,
    names,
    paternal_surname,
    maternal_surname,
    email,
    password,
    confirmPassword,
    registrationSuccess,
    errorMessage,
    isLoading,
    submitRegister
  }
}