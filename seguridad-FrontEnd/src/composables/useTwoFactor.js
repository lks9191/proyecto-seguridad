// src/composables/useTwoFactor.js
import { ref } from 'vue'
import { useRouter } from 'vue-router'
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
      // Simulación de validación exitosa del código
      if (totpCode.value === '123456') {
        
        // 1. Recuperamos el rol del usuario que intentó loguearse
        const assignedRole = localStorage.getItem('pendingRole') || 'USER'
        
        // 2. Simulamos el JWT que entregaría el backend
        const mockJwt = `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.simulacion.${assignedRole}`
        
        // 3. Guardamos en el estado global (Pinia)
        authStore.login(mockJwt, assignedRole)
        
        // 4. Limpiamos el rol temporal por seguridad
        localStorage.removeItem('pendingRole')

        // 5. Control de Acceso: Redirección según el RBAC
        switch (assignedRole) {
          case 'ADMIN':
            router.push({ name: 'admin-dashboard' })
            break
          case 'AUDITOR':
            router.push({ name: 'auditor-dashboard' })
            break
          case 'USER':
          default:
            router.push({ name: 'user-dashboard' })
            break
        }
        
      } else {
        errorMessage.value = 'Código TOTP inválido. Intente nuevamente.'
      }
    } catch (error) {
      errorMessage.value = 'Error al verificar el código.'
    } finally {
      isLoading.value = false
    }
  }

  return { totpCode, errorMessage, isLoading, verifyCode }
}