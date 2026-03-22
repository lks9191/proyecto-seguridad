// src/composables/useRegister.js
import { ref } from 'vue'
import { useRouter } from 'vue-router'

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

    // 1. Validar que las contraseñas coincidan
    if (password.value !== confirmPassword.value) {
      errorMessage.value = 'Las contraseñas no coinciden.'
      isLoading.value = false
      return
    }

    // 2. Validación de Contraseña Fuerte (Req. Funcional 1)
    // Debe tener al menos 8 caracteres, 1 mayúscula, 1 minúscula y 1 número
    const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/
    if (!strongPasswordRegex.test(password.value)) {
      errorMessage.value = 'La contraseña debe tener mín. 8 caracteres, una mayúscula y un número.'
      isLoading.value = false
      return
    }

    try {
      // AQUÍ: Futura llamada a tu API de Node.js (ej. fetch('/api/auth/register'))
      
      // Simulamos la espera del servidor
      setTimeout(() => {
        alert('Registro exitoso. Serás redirigido al Login.')
        // Después de registrar, lo normal es mandar al usuario al Login
        router.push({ name: 'login' })
      }, 1000)
      
    } catch (error) {
      errorMessage.value = 'Error al conectar con el servidor.'
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