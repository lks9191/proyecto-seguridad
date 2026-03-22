// src/composables/useLogin.js
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export function useLogin() {
  const router = useRouter()
  
  const username = ref('')
  const password = ref('')
  const errorMessage = ref('')
  const isLoading = ref(false)

  // Base de datos simulada de usuarios para tus pruebas
  const mockUsers = {
    'admin': 'ADMIN',
    'usuario': 'USER',
    'auditor': 'AUDITOR'
  }

  const submitLogin = async () => {
    isLoading.value = true
    errorMessage.value = ''

    try {
      // Validamos que el usuario exista en nuestro objeto y la contraseña sea correcta
      const userRole = mockUsers[username.value.toLowerCase()]

      if (userRole && password.value === 'Segura123!') {
        // Guardamos el rol temporalmente en localStorage SOLO para pasarlo al 2FA
        // (En la vida real, el backend manejaría este estado de sesión intermedia)
        localStorage.setItem('pendingRole', userRole)
        
        // Pasamos al paso 2
        router.push({ name: 'two-factor' })
      } else {
        errorMessage.value = 'Credenciales incorrectas. Verifique su usuario o contraseña.'
      }
    } catch (error) {
      errorMessage.value = 'Error de conexión con el servidor.'
    } finally {
      isLoading.value = false
    }
  }

  return { username, password, errorMessage, isLoading, submitLogin }
}