// src/composables/useAuditor.js
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

export function useAuditor() {
  const authStore = useAuthStore()
  const router = useRouter()
  
  const logs = ref([])
  const isLoading = ref(false)

  const fetchLogs = () => {
    isLoading.value = true
    
    // Simulando el fetch al backend de la tabla de auditoría
    setTimeout(() => {
      logs.value = [
        { id: 1001, date: '2026-03-22 10:15:22', user: 'admin', event: 'LOGIN_SUCCESS', ip: '190.181.x.x', detail: 'Inicio de sesión con 2FA exitoso' },
        { id: 1002, date: '2026-03-22 10:45:10', user: 'usuario', event: 'LOGIN_FAILED_2FA', ip: '181.115.x.x', detail: 'Código TOTP incorrecto' },
        { id: 1003, date: '2026-03-22 10:46:05', user: 'usuario', event: 'LOGIN_SUCCESS', ip: '181.115.x.x', detail: 'Inicio de sesión con 2FA exitoso' },
        { id: 1004, date: '2026-03-22 11:20:00', user: 'anonimo', event: 'UNAUTHORIZED_ACCESS', ip: '45.23.x.x', detail: 'Intento de acceso a /dashboard/admin' },
        { id: 1005, date: '2026-03-22 11:35:12', user: 'admin', event: 'ROLE_CHANGED', ip: '190.181.x.x', detail: 'Cambió rol de user_id 4 a ADMIN' }
      ]
      isLoading.value = false
    }, 500)
  }

  const handleLogout = () => {
    authStore.logout()
    router.push({ name: 'login' })
  }

  onMounted(() => {
    fetchLogs()
  })

  return { logs, isLoading, handleLogout }
}