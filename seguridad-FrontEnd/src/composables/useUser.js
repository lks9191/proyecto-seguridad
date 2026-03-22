// src/composables/useUser.js
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

export function useUser() {
  const authStore = useAuthStore()
  const router = useRouter()
  
  const profile = ref(null)
  const publicData = ref([])
  const isLoading = ref(false)

  const fetchUserData = () => {
    isLoading.value = true
    
    // Simulamos la respuesta de tu API (Node.js/Express)
    setTimeout(() => {
      // Datos del perfil (Confidencialidad: solo él puede ver esto)
      profile.value = {
        username: 'usuario',
        fullName: 'Lucas Calderón',
        email: 'lucas@example.com',
        location: 'La Paz, Bolivia',
        career: 'Ciencias de la Computación',
        status: 'Activo'
      }
      
      // Datos públicos del sistema
      publicData.value = [
        { id: 1, title: 'Política de Privacidad', content: 'Actualización sobre el manejo de 2FA y sesiones.' },
        { id: 2, title: 'Aviso de Seguridad', content: 'Las contraseñas ahora requieren esquema fuerte (bcrypt).' }
      ]
      
      isLoading.value = false
    }, 500)
  }

  const handleLogout = () => {
    authStore.logout()
    router.push({ name: 'login' })
  }

  onMounted(() => {
    fetchUserData()
  })

  return { profile, publicData, isLoading, handleLogout }
}