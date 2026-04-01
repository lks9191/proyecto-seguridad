import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/services/api'

export function useAdmin() {
  const authStore = useAuthStore()
  const router = useRouter()

  const users = ref([])
  const roles = ref([])
  const activeSessions = ref([])
  const sessionHistory = ref([])
  const isLoading = ref(false)
  const message = ref('')

  const fetchData = async (silent = false) => {
    if (!silent) isLoading.value = true
    try {
      const [usersRes, rolesRes, sessionsRes, historyRes] = await Promise.all([
        api.get('/admin/users'),
        api.get('/admin/roles'),
        api.get('/admin/sessions'),
        api.get('/admin/sessions/history')
      ])
      users.value = usersRes.data
      roles.value = rolesRes.data
      activeSessions.value = sessionsRes.data
      sessionHistory.value = historyRes.data
    } catch (error) {
      console.error(error)
      message.value = 'Error al cargar datos del panel.'
    } finally {
      isLoading.value = false
    }
  }

  const createUser = async (userData) => {
    try {
      await api.post('/admin/users', userData)
      message.value = 'Usuario creado con éxito.'
      fetchData()
      return true
    } catch (error) {
      message.value = error.response?.data?.msg || 'Error al crear usuario.'
      return false
    }
  }

  const deleteUser = async (userId) => {
    if (!confirm('¿Estás seguro de eliminar este usuario?')) return
    try {
      await api.delete(`/admin/users/${userId}`)
      message.value = 'Usuario eliminado.'
      fetchData()
    } catch (error) {
      message.value = 'Error al eliminar usuario.'
    }
  }

  const changeUserRole = async (userId, roleName) => {
    try {
      await api.post('/admin/assign-role', { user_id: userId, role: roleName })
      message.value = `Rol ${roleName} asignado correctamente.`
      fetchData()
    } catch (error) {
      message.value = 'Error al asignar rol.'
    }
  }

  const updateUser = async (userId, userData) => {
    try {
      await api.put(`/admin/users/${userId}`, userData)
      message.value = 'Usuario actualizado con éxito.'
      fetchData()
      return true
    } catch (error) {
      message.value = error.response?.data?.msg || 'Error al actualizar usuario.'
      return false
    }
  }

  const createRole = async (roleName) => {
    try {
      await api.post('/admin/roles', { name: roleName })
      message.value = 'Rol creado.'
      fetchData()
    } catch (error) {
      message.value = 'Error al crear rol.'
    }
  }

  const updateRole = async (roleId, roleName) => {
    try {
      await api.put(`/admin/roles/${roleId}`, { name: roleName })
      message.value = 'Rol actualizado con éxito.'
      fetchData()
      return true
    } catch (error) {
      message.value = error.response?.data?.msg || 'Error al actualizar rol.'
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

  onMounted(fetchData)

  return {
    users,
    roles,
    activeSessions,
    sessionHistory,
    isLoading,
    message,
    createUser,
    deleteUser,
    changeUserRole,
    updateUser,
    createRole,
    updateRole,
    handleLogout,
    refresh: fetchData
  }
}