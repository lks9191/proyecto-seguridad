// src/composables/useAdmin.js
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

export function useAdmin() {
  const authStore = useAuthStore()
  const router = useRouter()
  
  // Simulamos una lista de usuarios que vendría de tu backend
  const users = ref([])
  const isLoading = ref(false)
  const message = ref('')

  // Función para cargar usuarios (Simulando una petición GET)
  const fetchUsers = async () => {
    isLoading.value = true
    try {
      // AQUÍ: Futura llamada a tu API con Axios/Fetch enviando el JWT
      // const response = await api.get('/admin/users')
      
      // Datos mockeados para tu demostración
      setTimeout(() => {
        users.value = [
          { id: 1, username: 'lucas.calderon', email: 'lucas@example.com', role: 'ADMIN' },
          { id: 2, username: 'maria.perez', email: 'maria@example.com', role: 'USER' },
          { id: 3, username: 'carlos.auditor', email: 'carlos@example.com', role: 'AUDITOR' },
          { id: 4, username: 'juan.prueba', email: 'juan@example.com', role: 'USER' }
        ]
        isLoading.value = false
      }, 500) // Simulamos medio segundo de latencia de red
    } catch (error) {
      message.value = 'Error al cargar los usuarios.'
      isLoading.value = false
    }
  }

  // Función para cambiar el rol de un usuario (Simulando una petición PUT/PATCH)
  const changeUserRole = async (userId, newRole) => {
    // AQUÍ: Futura llamada a tu API
    // await api.put(`/admin/users/${userId}/role`, { role: newRole })
    
    // Actualizamos el estado local para reflejar el cambio en la UI
    const userIndex = users.value.findIndex(u => u.id === userId)
    if (userIndex !== -1) {
      users.value[userIndex].role = newRole
      message.value = `Rol actualizado a ${newRole} con éxito.`
      
      // Limpiamos el mensaje después de 3 segundos
      setTimeout(() => message.value = '', 3000)
    }
  }

  // Función para cerrar sesión y probar el flujo de nuevo
  const handleLogout = () => {
    authStore.logout()
    router.push({ name: 'login' })
  }

  // Cargar los usuarios automáticamente cuando la vista se monte
  onMounted(() => {
    fetchUsers()
  })

  return {
    users,
    isLoading,
    message,
    changeUserRole,
    handleLogout
  }
}