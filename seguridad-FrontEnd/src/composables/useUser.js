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
  { 
    id: 1, 
    title: 'AGETIC: Nuevos Estándares de Credenciales', 
    content: 'En el marco de la campaña "Protege tu información", AGETIC establece que las contraseñas para servicios estatales deben tener al menos 12 caracteres, combinando mayúsculas, minúsculas, números y símbolos.' 
  },
  { 
    id: 2, 
    title: 'Congreso de Ciberseguridad (CITC)', 
    content: 'Concluye con éxito el Congreso Internacional de Tecnología y Ciberseguridad en La Paz, enfocado en infraestructura tecnológica, hacking ético y respuesta ante incidentes en el Estado.' 
  },
  { 
    id: 3, 
    title: 'Ciudadanía Digital exige Autenticación 2FA', 
    content: 'Para garantizar el no repudio y la integridad en la Sede Electrónica, todos los trámites de alta confidencialidad ahora requieren verificación por código de un solo uso (OTP) al correo o celular.' 
  }
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