import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/services/api'

export function useAuditor() {
  const authStore = useAuthStore()
  const router = useRouter()

  const activeSessions = ref([])
  const sessionHistory = ref([])
  const isLoading = ref(false)
  const message = ref('')

  const fetchLogs = async (silent = false) => {
    if (!silent) isLoading.value = true
    try {
      const [sessionsRes, historyRes] = await Promise.all([
        api.get('/auditor/sessions'),
        api.get('/auditor/sessions/history')
      ])
      activeSessions.value = sessionsRes.data
      sessionHistory.value = historyRes.data
    } catch (error) {
      console.error(error)
      message.value = 'Error al cargar los registros de auditoría.'
    } finally {
      isLoading.value = false
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

  onMounted(fetchLogs)

  return { activeSessions, sessionHistory, isLoading, message, handleLogout, refresh: fetchLogs }
}