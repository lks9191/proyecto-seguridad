import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/services/api'

export function useUser() {
  const authStore = useAuthStore()
  const router = useRouter()

  const profile = ref(null)
  const publicData = ref([])
  const isLoading = ref(false)
  const message = ref('')

  const fetchUserData = async () => {
    isLoading.value = true
    try {
      const response = await api.get('/user/profile')
      profile.value = response.data

      // Some mock public data for the UI
      publicData.value = [
        { id: 1, title: 'Política de Privacidad', content: 'Actualización sobre el manejo de 2FA y sesiones.' },
        { id: 2, title: 'Aviso de Seguridad', content: 'Las contraseñas ahora requieren esquema fuerte (bcrypt).' }
      ]
    } catch (error) {
      console.error(error)
      message.value = 'Error al cargar tu perfil.'
    } finally {
      isLoading.value = false
    }
  }

  const updateProfile = async (updateData) => {
    try {
      await api.put('/user/profile', updateData)
      message.value = 'Perfil actualizado con éxito.'
      fetchUserData()
      return true
    } catch (error) {
      message.value = error.response?.data?.msg || 'Error al actualizar perfil.'
      return false
    }
  }

  const request2FA = async () => {
    try {
      const res = await api.post('/user/request-2fa')
      message.value = res.data.msg
      return true
    } catch (error) {
      message.value = error.response?.data?.msg || 'Error al solicitar 2FA.'
      return false
    }
  }

  const confirm2FA = async (token) => {
    try {
      const res = await api.post('/user/confirm-2fa', { token })
      message.value = res.data.msg
      fetchUserData()
      return true
    } catch (error) {
      message.value = error.response?.data?.msg || 'Código inválido.'
      return false
    }
  }

  const disable2FA = async () => {
    try {
      const res = await api.post('/user/disable-2fa')
      message.value = res.data.msg
      fetchUserData()
      return true
    } catch (error) {
      message.value = error.response?.data?.msg || 'Error al desactivar 2FA.'
      return false
    }
  }

  const handleLogout = async () => {
    try {
      await api.post('/user/logout')
    } catch (e) {
      console.error(e)
    }
    authStore.logout()
    router.push({ name: 'login' })
  }

  onMounted(fetchUserData)

  return {
    profile, publicData, isLoading, message,
    updateProfile, handleLogout, fetchUserData,
    request2FA, confirm2FA, disable2FA
  }
}