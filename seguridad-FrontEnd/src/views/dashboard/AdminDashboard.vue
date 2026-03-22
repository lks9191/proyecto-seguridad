<template>
  <div class="dashboard-wrapper">
    <div class="admin-dashboard glow-box">
      <header class="dashboard-header">
        <div class="header-left">
          <h2>Panel de Administración (RBAC)</h2>
          <div v-if="profile" class="user-info-mini">
            <span class="username">{{ profile.username }}</span>
            <span :class="['status-dot', profile.is_2fa_enabled ? 'active' : 'inactive']"
              :title="profile.is_2fa_enabled ? '2FA Activo' : '2FA Inactivo'"></span>
            <button @click="openTwoFAModal" class="mini-2fa-btn">{{ profile.is_2fa_enabled ? '2FA OK' : 'ACTIVAR 2FA'
              }}</button>
          </div>
        </div>
        <div class="header-actions">
          <button @click="refresh" class="refresh-btn">REFRESCAR</button>
          <button @click="handleLogout" class="logout-btn">CERRAR SESIÓN</button>
        </div>
      </header>

      <div v-if="message" class="alert-info" @click="message = ''">
        {{ message }}
      </div>

      <!-- TABS -->
      <div class="tabs">
        <button :class="{ active: activeTab === 'users' }" @click="activeTab = 'users'">USUARIOS</button>
        <button :class="{ active: activeTab === 'roles' }" @click="activeTab = 'roles'">ROLES</button>
        <button :class="{ active: activeTab === 'sessions' }" @click="activeTab = 'sessions'">SESIONES</button>
      </div>

      <div v-if="isLoading" class="loading">Cargando datos...</div>

      <div v-else class="tab-content">
        <!-- USER CRUD -->
        <div v-if="activeTab === 'users'" class="section">
          <div class="section-header">
            <h3>Gestión de Usuarios</h3>
            <button @click="openCreateModal" class="add-btn">+ NUEVO USUARIO</button>
          </div>
          <div class="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Usuario</th>
                  <th>Email</th>
                  <th>Roles</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in users" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>{{ user.username }}</td>
                  <td>{{ user.email }}</td>
                  <td>
                    <span v-for="r in user.roles" :key="r" :class="['role-badge', r.toLowerCase()]">
                      {{ r }}
                    </span>
                  </td>
                  <td>
                    <button @click="openEditModal(user)" class="edit-btn-small">EDITAR</button>
                    <button @click="deleteUser(user.id)" class="delete-icon">🗑️</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ROLE CRUD -->
        <div v-if="activeTab === 'roles'" class="section">
          <div class="section-header">
            <h3>Gestión de Roles</h3>
            <div class="add-role-form">
              <input v-model="newRoleName" placeholder="Nombre del rol" class="neon-input">
              <button @click="handleCreateRole" class="add-btn">AGREGAR</button>
            </div>
          </div>
          <div class="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nombre del Rol</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="role in roles" :key="role.id">
                  <td>{{ role.id }}</td>
                  <td><span class="role-badge">{{ role.name }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- SESSIONS -->
        <div v-if="activeTab === 'sessions'" class="section">
          <h3>Sesiones Activas</h3>
          <div class="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>IP</th>
                  <th>Iniciada</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="s in activeSessions" :key="s.id">
                  <td>{{ s.username }}</td>
                  <td>{{ s.ip_address }}</td>
                  <td>{{ formatDate(s.created_at) }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <h3 class="mt-2">Historial de Sesiones</h3>
          <div class="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>Acción</th>
                  <th>IP</th>
                  <th>Fecha</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="h in sessionHistory" :key="h.id">
                  <td>{{ h.username }}</td>
                  <td>
                    <span :class="['event-badge', getEventClass(h.action)]">{{ h.action }}</span>
                  </td>
                  <td>{{ h.ip_address }}</td>
                  <td>{{ formatDate(h.timestamp) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL PARA USUARIO (CREAR/EDITAR) -->
    <div v-if="showUserModal" class="modal-overlay">
      <div class="modal-content glow-box">
        <h3>{{ isEditing ? 'Editar Usuario' : 'Crear Nuevo Usuario' }}</h3>
        <div v-if="modalError" class="modal-alert-error" @click="modalError = ''">
          {{ modalError }}
        </div>
        <form @submit.prevent="handleSubmitUser">
          <div class="input-group">
            <label>Username</label>
            <input v-model="userForm.username" required class="neon-input">
          </div>
          <div class="input-group">
            <label>Email</label>
            <input v-model="userForm.email" type="email" required class="neon-input">
          </div>
          <div class="input-group">
            <label>{{ isEditing ? 'Nueva Contraseña (Opcional)' : 'Password (Fuerte)' }}</label>
            <input v-model="userForm.password" type="password" :required="!isEditing" class="neon-input">
          </div>
          <div class="input-group" v-if="!isEditing || userForm.password">
            <label>Confirmar Password</label>
            <input v-model="userForm.confirmPassword" type="password" required class="neon-input">
          </div>
          <div class="input-group">
            <label>Roles</label>
            <div class="roles-checklist">
              <label v-for="r in roles" :key="r.id" class="checkbox-label">
                <input type="checkbox" :value="r.name" v-model="userForm.roles">
                {{ r.name }}
              </label>
            </div>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showUserModal = false" class="cancel-btn">CANCELAR</button>
            <button type="submit" class="submit-btn" :disabled="isSubmitting">
              {{ isSubmitting ? 'GUARDANDO...' : (isEditing ? 'ACTUALIZAR' : 'CREAR') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 2FA SETUP MODAL (ADMIN PERSO) -->
    <div v-if="showTwoFAModal" class="modal-overlay">
      <div class="modal-content glow-box">
        <h3>Seguridad: 2FA vía Email</h3>
        <div v-if="twoFAStep === 'request'">
          <p v-if="!profile?.is_2fa_enabled">Activa el segundo factor para mayor seguridad. Enviaremos un código a
            <strong>{{ profile?.email }}</strong>.</p>
          <p v-else>El segundo factor está actualmente activo. ¿Deseas desactivarlo?</p>
          <div class="modal-actions">
            <button @click="showTwoFAModal = false" class="cancel-btn">CANCELAR</button>
            <button v-if="!profile?.is_2fa_enabled" @click="handleRequestOTP" class="submit-btn"
              :disabled="isVerifying">
              {{ isVerifying ? 'ENVIANDO...' : 'ENVIAR CÓDIGO' }}
            </button>
            <button v-else @click="handleDisable2FA" class="logout-btn">DESACTIVAR 2FA</button>
          </div>
        </div>
        <div v-else>
          <p>Ingresa el código de 6 dígitos enviado a tu correo.</p>
          <div class="input-group">
            <input v-model="otpToken" class="neon-input code-input" placeholder="000000" maxlength="6">
          </div>
          <div class="modal-actions">
            <button @click="twoFAStep = 'request'" class="cancel-btn">VOLVER</button>
            <button @click="handleConfirm2FA" class="submit-btn" :disabled="isVerifying || otpToken.length < 6">
              {{ isVerifying ? 'VERIFICANDO...' : 'CONFIRMAR' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useAdmin } from '@/composables/useAdmin'
import { useUser } from '@/composables/useUser'

const {
  users, roles, activeSessions, sessionHistory,
  isLoading, message, createUser, deleteUser,
  updateUser, createRole, handleLogout, refresh
} = useAdmin()

const { profile, request2FA, confirm2FA, disable2FA } = useUser()

const activeTab = ref('users')
const showUserModal = ref(false)
const isEditing = ref(false)
const isSubmitting = ref(false)
const editingUserId = ref(null)
const newRoleName = ref('')
const modalError = ref('')

// 2FA Admin/Perso
const showTwoFAModal = ref(false)
const twoFAStep = ref('request')
const otpToken = ref('')
const isVerifying = ref(false)

const openTwoFAModal = () => {
  twoFAStep.value = 'request'
  otpToken.value = ''
  showTwoFAModal.value = true
}

const handleRequestOTP = async () => {
  isVerifying.value = true
  if (await request2FA()) twoFAStep.value = 'verify'
  isVerifying.value = false
}

const handleConfirm2FA = async () => {
  isVerifying.value = true
  if (await confirm2FA(otpToken.value)) showTwoFAModal.value = false
  isVerifying.value = false
}

const handleDisable2FA = async () => {
  if (confirm('¿Desactivar 2FA?')) {
    await disable2FA()
    showTwoFAModal.value = false
  }
}

watch(message, (newVal) => {
  if (showUserModal.value && (newVal.toLowerCase().includes('error') || newVal.toLowerCase().includes('debe'))) {
    modalError.value = newVal
  }
})

const userForm = ref({ username: '', email: '', password: '', confirmPassword: '', roles: ['USER'] })

const openCreateModal = () => {
  isEditing.value = false
  userForm.value = { username: '', email: '', password: '', confirmPassword: '', roles: ['USER'] }
  modalError.value = ''
  showUserModal.value = true
}

const openEditModal = (user) => {
  isEditing.value = true
  editingUserId.value = user.id
  userForm.value = { username: user.username, email: user.email, password: '', confirmPassword: '', roles: [...user.roles] }
  modalError.value = ''
  showUserModal.value = true
}

const handleSubmitUser = async () => {
  modalError.value = ''
  if (userForm.value.password || !isEditing.value) {
    if (userForm.value.password !== userForm.value.confirmPassword) {
      modalError.value = 'Las contraseñas no coinciden.'
      return
    }
  }
  isSubmitting.value = true
  let success = false
  const data = { ...userForm.value }; delete data.confirmPassword;
  if (isEditing.value) {
    if (!data.password) delete data.password
    success = await updateUser(editingUserId.value, data)
  } else {
    success = await createUser(data)
  }
  isSubmitting.value = false
  if (success) showUserModal.value = false
  else modalError.value = message.value
}

const handleCreateRole = async () => {
  if (newRoleName.value) { await createRole(newRoleName.value); newRoleName.value = '' }
}

const formatDate = (dateStr) => dateStr ? new Date(dateStr).toLocaleString() : '-'
const getEventClass = (event) => {
  if (event.includes('SUCCESS')) return 'success'
  if (event.includes('FAILED')) return 'danger'
  if (event.includes('LOGOUT')) return 'warning'
  return 'default'
}
</script>

<style scoped>
.dashboard-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  min-height: 100vh;
  background-color: #0d0d0d;
  padding: 2rem 1rem;
  box-sizing: border-box;
  font-family: sans-serif;
  color: #ffffff;
  overflow-y: auto;
}

.glow-box {
  background-color: #111111;
  padding: 2.5rem;
  border-radius: 20px;
  max-width: 1000px;
  margin: 0 auto;
  box-shadow: 0 0 15px rgba(0, 150, 255, 0.2);
  border: 1px solid rgba(0, 150, 255, 0.2);
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #333;
  padding-bottom: 1rem;
  margin-bottom: 2rem;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.user-info-mini {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  background: #1a1a1a;
  padding: 5px 15px;
  border-radius: 20px;
  border: 1px solid #333;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ff4d4d;
}

.status-dot.active {
  background: #28a745;
  box-shadow: 0 0 5px #28a745;
}

.mini-2fa-btn {
  background: transparent;
  border: none;
  color: #0096ff;
  font-size: 0.7rem;
  font-weight: bold;
  cursor: pointer;
  text-decoration: underline;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

h2 {
  color: #0096ff;
  margin: 0;
}

.refresh-btn,
.logout-btn {
  background: transparent;
  border-radius: 30px;
  padding: 0.5rem 1.2rem;
  font-size: 0.85rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.refresh-btn {
  color: #0096ff;
  border: 1px solid #0096ff;
}

.logout-btn {
  color: #ff4d4d;
  border: 1px solid #ff4d4d;
}

.refresh-btn:hover {
  background: #0096ff;
  color: white;
}

.logout-btn:hover {
  background: #ff4d4d;
  color: white;
}

.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #333;
}

.tabs button {
  background: transparent;
  border: none;
  color: #888;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-weight: bold;
}

.tabs button.active {
  color: #0096ff;
  border-bottom: 2px solid #0096ff;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.add-btn {
  background: #0096ff;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.table-responsive {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
}

th,
td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #333;
}

th {
  background: #222;
  color: #0096ff;
  font-weight: bold;
}

.role-badge {
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.75rem;
  margin-right: 5px;
  border: 1px solid #444;
}

.admin {
  color: #0096ff;
  border-color: #0096ff;
}

.auditor {
  color: #ffa500;
  border-color: #ffa500;
}

.edit-btn-small {
  background: transparent;
  color: #0096ff;
  border: 1px solid #0096ff;
  padding: 4px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  margin-right: 10px;
}

.edit-btn-small:hover {
  background: #0096ff;
  color: white;
}

.delete-icon {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  width: 90%;
  max-width: 450px;
}

.input-group {
  margin-bottom: 1.2rem;
  display: flex;
  flex-direction: column;
}

.input-group label {
  margin-bottom: 0.5rem;
  color: #aaa;
  font-size: 0.9rem;
}

.neon-input {
  background: #0d0d0d;
  color: white;
  border: 1px solid #444;
  padding: 0.6rem;
  border-radius: 4px;
  outline: none;
}

.neon-input:focus {
  border-color: #0096ff;
}

.code-input {
  text-align: center;
  font-size: 1.5rem;
  letter-spacing: 10px;
}

.roles-checklist {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  background: #0d0d0d;
  padding: 0.8rem;
  border-radius: 4px;
  border: 1px solid #444;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #ccc;
  cursor: pointer;
  font-size: 0.9rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.cancel-btn {
  background: #333;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 4px;
  cursor: pointer;
}

.submit-btn {
  background: #0096ff;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.alert-info {
  background: rgba(0, 150, 255, 0.1);
  color: #0096ff;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
  border-left: 4px solid #0096ff;
  cursor: pointer;
}

.modal-alert-error {
  background: rgba(255, 77, 77, 0.1);
  color: #ff4d4d;
  padding: 0.8rem 1.2rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
  border-left: 4px solid #ff4d4d;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: bold;
}

.event-badge {
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.8rem;
  font-weight: bold;
}

.success {
  color: #28a745;
  border: 1px solid #28a745;
}

.danger {
  color: #ff4d4d;
  border: 1px solid #ff4d4d;
}

.warning {
  color: #ffa500;
  border: 1px solid #ffa500;
}

.loading {
  text-align: center;
  color: #0096ff;
  padding: 2rem;
}
</style>