<template>
  <div class="gov-layout">
    <header class="gov-header">
      <div class="header-content">
        <div class="logo-area">
          <span class="shield-icon">🛡️</span>
          <div class="titles">
            <h1>SUT-BO</h1>
            <p>Sistema Único de Trámites Bolivia</p>
          </div>
        </div>
        
        <div class="header-actions">
          <div v-if="profile" class="admin-profile-badge">
            <span class="username">{{ profile.username }}</span>
            <span :class="['status-dot', profile.is_2fa_enabled ? 'active' : 'inactive']"
              :title="profile.is_2fa_enabled ? '2FA Activo' : '2FA Inactivo'"></span>
            <button @click="openTwoFAModal" class="mini-2fa-btn">
              {{ profile.is_2fa_enabled ? '2FA OK' : 'Activar 2FA' }}
            </button>
          </div>
          
          <button @click="refresh" class="gov-btn-outline-light">Refrescar</button>
          <button @click="handleLogout" class="gov-logout-btn">Cerrar Sesión</button>
        </div>
      </div>
    </header>

    <main class="dashboard-main">
      <div class="dashboard-header-bar">
        <h2>Panel de Administración (RBAC)</h2>
        <p class="subtitle">Gestión centralizada de identidades, roles y auditoría de sesiones.</p>
      </div>

      <div v-if="message" class="alert-info" @click="message = ''">
        {{ message }}
      </div>

      <div class="gov-card">
        <div class="gov-tabs">
          <button :class="{ active: activeTab === 'users' }" @click="activeTab = 'users'">USUARIOS</button>
          <button :class="{ active: activeTab === 'roles' }" @click="activeTab = 'roles'">ROLES</button>
          <button :class="{ active: activeTab === 'sessions' }" @click="activeTab = 'sessions'">SESIONES ACTIVAS</button>
        </div>

        <div v-if="isLoading" class="loading">Cargando información del sistema...</div>

        <div v-else class="tab-content">
          <div v-if="activeTab === 'users'" class="section">
            <div class="section-header">
              <h3>Directorio de Usuarios</h3>
              <button @click="openCreateModal" class="gov-btn-primary">+ Nuevo Funcionario / Ciudadano</button>
            </div>
            
            <div class="table-responsive">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Usuario / Documento</th>
                    <th>Correo Electrónico</th>
                    <th>Roles Asignados</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in users" :key="user.id">
                    <td class="fw-bold">{{ user.id }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.email }}</td>
                    <td>
                      <span v-for="r in user.roles" :key="r" :class="['role-badge', r.toLowerCase()]">
                        {{ r }}
                      </span>
                    </td>
                    <td>
                      <button @click="openEditModal(user)" class="gov-btn-outline-small">Editar</button>
                      <button @click="deleteUser(user.id)" class="gov-btn-danger-icon" title="Eliminar Usuario">🗑️</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div v-if="activeTab === 'roles'" class="section">
            <div class="section-header">
              <h3>Gestión de Privilegios (Roles)</h3>
              <div class="add-role-form">
                <input v-model="newRoleName" placeholder="Ej: SUPERVISOR" class="gov-input input-inline">
                <button @click="handleCreateRole" class="gov-btn-primary">Añadir Rol</button>
              </div>
            </div>
            
            <div class="table-responsive">
              <table>
                <thead>
                  <tr>
                    <th style="width: 80px;">ID</th>
                    <th>Identificador del Rol</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="role in roles" :key="role.id">
                    <td class="fw-bold">{{ role.id }}</td>
                    <td><span class="role-badge default-role">{{ role.name }}</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div v-if="activeTab === 'sessions'" class="section">
            <h3>Sesiones Activas en Tiempo Real</h3>
            <div class="table-responsive mb-2">
              <table>
                <thead>
                  <tr>
                    <th>Usuario conectado</th>
                    <th>Dirección IP</th>
                    <th>Hora de Inicio</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="s in activeSessions" :key="s.id">
                    <td class="fw-bold">{{ s.username }}</td>
                    <td class="mono-text">{{ s.ip_address }}</td>
                    <td>{{ formatDate(s.created_at) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h3 class="mt-2">Registro Histórico (Auditoría Básica)</h3>
            <div class="table-responsive">
              <table>
                <thead>
                  <tr>
                    <th>Usuario</th>
                    <th>Evento Registrado</th>
                    <th>Dirección IP</th>
                    <th>Fecha y Hora</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="h in sessionHistory" :key="h.id">
                    <td class="fw-bold">{{ h.username }}</td>
                    <td>
                      <span :class="['event-badge', getEventClass(h.action)]">{{ h.action }}</span>
                    </td>
                    <td class="mono-text">{{ h.ip_address }}</td>
                    <td>{{ formatDate(h.timestamp) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </main>

    <footer class="gov-footer">
      <p>© 2026 Plataforma de Identidad y Trámites Digitales - SUT-BO.</p>
    </footer>

    <div v-if="showUserModal" class="gov-modal-overlay">
      <div class="gov-modal-content">
        <h3>{{ isEditing ? 'Actualizar Credenciales' : 'Registrar Nuevo Usuario' }}</h3>
        <p class="modal-subtitle">Complete el formulario para asignar accesos en el sistema.</p>
        
        <div v-if="modalError" class="modal-alert-error" @click="modalError = ''">
          {{ modalError }}
        </div>
        
        <form @submit.prevent="handleSubmitUser">
          <div class="input-group">
            <label>Identificación (Usuario / Documento)</label>
            <input v-model="userForm.username" required class="gov-input">
          </div>
          <div class="input-group">
            <label>Correo Electrónico Institucional/Personal</label>
            <input v-model="userForm.email" type="email" required class="gov-input">
          </div>
          <div class="input-group">
            <label>{{ isEditing ? 'Nueva Contraseña (Opcional)' : 'Contraseña Segura' }}</label>
            <input v-model="userForm.password" type="password" :required="!isEditing" class="gov-input">
          </div>
          <div class="input-group" v-if="!isEditing || userForm.password">
            <label>Confirmar Contraseña</label>
            <input v-model="userForm.confirmPassword" type="password" required class="gov-input">
          </div>
          <div class="input-group">
            <label>Privilegios (Roles RBAC)</label>
            <div class="roles-checklist">
              <label v-for="r in roles" :key="r.id" class="checkbox-label">
                <input type="checkbox" :value="r.name" v-model="userForm.roles" class="gov-checkbox">
                <span>{{ r.name }}</span>
              </label>
            </div>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showUserModal = false" class="gov-btn-secondary">Cancelar</button>
            <button type="submit" class="gov-btn-primary" :disabled="isSubmitting">
              {{ isSubmitting ? 'Procesando...' : (isEditing ? 'Actualizar Registro' : 'Crear Usuario') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showTwoFAModal" class="gov-modal-overlay">
      <div class="gov-modal-content">
        <h3>Seguridad de la Cuenta (2FA)</h3>
        <div v-if="twoFAStep === 'request'">
          <p class="modal-subtitle" v-if="!profile?.is_2fa_enabled">
            Como administrador, es obligatorio asegurar su cuenta. Enviaremos un código a: <strong>{{ profile?.email }}</strong>
          </p>
          <p class="modal-subtitle" v-else>
            El segundo factor está actualmente activo protegiendo su cuenta. ¿Desea desactivarlo bajo su propio riesgo?
          </p>
          <div class="modal-actions">
            <button @click="showTwoFAModal = false" class="gov-btn-secondary">Cancelar</button>
            <button v-if="!profile?.is_2fa_enabled" @click="handleRequestOTP" class="gov-btn-primary" :disabled="isVerifying">
              {{ isVerifying ? 'Enviando...' : 'Enviar Código' }}
            </button>
            <button v-else @click="handleDisable2FA" class="gov-btn-danger">Desactivar 2FA</button>
          </div>
        </div>
        <div v-else>
          <p class="modal-subtitle">Ingrese el código de 6 dígitos enviado a su correo.</p>
          <div class="input-group">
            <input v-model="otpToken" class="gov-input code-input" placeholder="000000" maxlength="6">
          </div>
          <div class="modal-actions">
            <button @click="twoFAStep = 'request'" class="gov-btn-secondary">Volver</button>
            <button @click="handleConfirm2FA" class="gov-btn-primary" :disabled="isVerifying || otpToken.length < 6">
              {{ isVerifying ? 'Verificando...' : 'Confirmar y Activar' }}
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
  if (confirm('Atención: Desactivar el 2FA en una cuenta de Administrador es un riesgo crítico. ¿Continuar?')) {
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
/* Reset y layout principal */
.gov-layout {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
  margin: 0;
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  overflow-y: auto;
}

/* --- HEADER --- */
.gov-header {
  background-color: #2c3136;
  color: #ffffff;
  padding: 1rem 0;
  border-bottom: 4px solid #0056b3;
}

.header-content {
  max-width: 1300px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-area { display: flex; align-items: center; gap: 1rem; }
.shield-icon { font-size: 2rem; }
.titles h1 { margin: 0; font-size: 1.2rem; font-weight: 600; letter-spacing: 0.5px; }
.titles p { margin: 0; font-size: 0.8rem; color: #a0aab2; }

/* Header Actions y Mini Perfil */
.header-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.admin-profile-badge {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.4rem 1rem;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.username { font-weight: 600; font-size: 0.9rem; }

.status-dot { width: 8px; height: 8px; border-radius: 50%; background: #fca5a5; }
.status-dot.active { background: #86efac; }

.mini-2fa-btn {
  background: transparent;
  border: none;
  color: #93c5fd;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
}
.mini-2fa-btn:hover { color: #ffffff; }

.gov-btn-outline-light {
  background: transparent;
  color: #ffffff;
  border: 1px solid #cbd5e0;
  padding: 0.4rem 1rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
}
.gov-btn-outline-light:hover { background: rgba(255,255,255,0.1); }

.gov-logout-btn {
  background-color: transparent;
  color: #ffcccb;
  border: 1px solid #c53030;
  padding: 0.4rem 1rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.gov-logout-btn:hover { background-color: #c53030; color: white; }

/* --- CONTENIDO PRINCIPAL --- */
.dashboard-main {
  flex-grow: 1;
  max-width: 1300px;
  margin: 0 auto;
  width: 100%;
  padding: 2rem;
  box-sizing: border-box;
}

.dashboard-header-bar { margin-bottom: 1.5rem; }
.dashboard-header-bar h2 { margin: 0 0 0.3rem 0; color: #2c3136; font-size: 1.8rem; }
.subtitle { color: #4a5568; margin: 0; font-size: 0.95rem; }

/* Tarjeta Principal */
.gov-card {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border-top: 4px solid #0056b3;
  padding: 0; /* Padding movido a las secciones */
  overflow: hidden;
}

/* Tabs */
.gov-tabs {
  display: flex;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.gov-tabs button {
  background: transparent;
  border: none;
  color: #718096;
  padding: 1rem 1.5rem;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  border-bottom: 3px solid transparent;
  transition: all 0.2s;
}

.gov-tabs button:hover { color: #2c3136; background: #edf2f7; }
.gov-tabs button.active { color: #0056b3; border-bottom: 3px solid #0056b3; background: #ffffff;}

/* Secciones Internas */
.section { padding: 2rem; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
h3 { margin: 0; color: #2c3136; font-size: 1.25rem; font-weight: 600; }

.add-role-form { display: flex; gap: 0.5rem; }
.input-inline { min-width: 250px; margin-bottom: 0 !important; }

/* --- TABLAS --- */
.table-responsive { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 4px; }
th, td { border-bottom: 1px solid #e2e8f0; padding: 12px 15px; text-align: left; font-size: 0.9rem; color: #4a5568; }
th { background-color: #edf2f7; color: #2c3136; font-weight: 600; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.5px; }
tr:hover { background-color: #f8fafc; }
.fw-bold { font-weight: 600; color: #2c3136; }
.mono-text { font-family: monospace; color: #718096; font-size: 0.95em; }

/* --- BADGES Y BOTONES --- */
.gov-btn-primary { background: #0056b3; color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 4px; cursor: pointer; font-weight: 600; font-size: 0.85rem; }
.gov-btn-primary:hover { background: #004494; }
.gov-btn-outline-small { background: transparent; color: #0056b3; border: 1px solid #0056b3; padding: 0.3rem 0.8rem; border-radius: 4px; cursor: pointer; font-size: 0.8rem; font-weight: 600; margin-right: 0.5rem; }
.gov-btn-outline-small:hover { background: #0056b3; color: white; }
.gov-btn-danger-icon { background: #fff5f5; border: 1px solid #feb2b2; padding: 0.3rem 0.6rem; border-radius: 4px; cursor: pointer; font-size: 1rem; color: #c53030; }
.gov-btn-danger-icon:hover { background: #fed7d7; }

/* Badges de Roles */
.role-badge { padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; margin-right: 5px; display: inline-block; }
.admin { background: #e0e7ff; color: #3730a3; border: 1px solid #c7d2fe; }
.auditor { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
.user { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }
.default-role { background: #e2e8f0; color: #1e293b; }

/* Badges de Eventos */
.event-badge { padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
.success { background-color: #def7ec; color: #03543f; border: 1px solid #84e1bc; }
.danger { background-color: #fde8e8; color: #9b1c1c; border: 1px solid #f8b4b4; }
.warning { background-color: #fef3c7; color: #92400e; border: 1px solid #fde68a; }

/* --- MODALES --- */
.gov-modal-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(44, 49, 54, 0.7); display: flex; justify-content: center; align-items: center; z-index: 1000; backdrop-filter: blur(2px); }
.gov-modal-content { background: #ffffff; width: 90%; max-width: 500px; padding: 2.5rem; border-radius: 8px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15); border-top: 4px solid #0056b3; }
.gov-modal-content h3 { margin-top: 0; color: #2c3136; font-size: 1.4rem; margin-bottom: 0.5rem; }
.modal-subtitle { color: #666; font-size: 0.9rem; margin-bottom: 1.5rem; line-height: 1.4; }
.input-group { margin-bottom: 1.2rem; display: flex; flex-direction: column; }
.input-group label { margin-bottom: 0.4rem; color: #4a5568; font-size: 0.85rem; font-weight: 600; }
.gov-input { background: #ffffff; color: #2d3748; border: 1px solid #cbd5e0; padding: 0.75rem; border-radius: 4px; outline: none; font-family: inherit; font-size: 0.95rem; }
.gov-input:focus { border-color: #0056b3; box-shadow: 0 0 0 3px rgba(0, 86, 179, 0.1); }

.roles-checklist { display: flex; flex-wrap: wrap; gap: 1rem; background: #f8fafc; padding: 1rem; border-radius: 4px; border: 1px solid #e2e8f0; }
.checkbox-label { display: flex; align-items: center; gap: 0.5rem; color: #4a5568; cursor: pointer; font-size: 0.9rem; font-weight: 600; }
.gov-checkbox { width: 16px; height: 16px; accent-color: #0056b3; cursor: pointer; }

.modal-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 2rem; border-top: 1px solid #e2e8f0; padding-top: 1.5rem; }
.gov-btn-secondary { background: #edf2f7; color: #4a5568; border: 1px solid #cbd5e0; padding: 0.6rem 1.2rem; border-radius: 4px; cursor: pointer; font-weight: 600; }
.gov-btn-secondary:hover { background: #e2e8f0; }
.gov-btn-danger { background: #c53030; color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 4px; cursor: pointer; font-weight: 600; }

.alert-info { background: #e6f7ff; color: #0056b3; padding: 1rem; border-radius: 4px; margin-bottom: 1.5rem; cursor: pointer; border-left: 4px solid #0056b3; font-weight: 500; }
.modal-alert-error { background: #fff5f5; color: #c53030; padding: 0.8rem 1.2rem; border-radius: 4px; margin-bottom: 1.5rem; border-left: 4px solid #c53030; font-weight: 600; font-size: 0.9rem; cursor: pointer; }
.loading { text-align: center; color: #0056b3; padding: 2rem; font-weight: 600; }
.mt-2 { margin-top: 2rem; }
.mb-2 { margin-bottom: 2rem; }
.code-input { text-align: center; font-size: 1.5rem; letter-spacing: 8px; font-weight: bold; }

/* --- FOOTER --- */
.gov-footer { background-color: #2c3136; color: #a0aab2; text-align: center; padding: 1.5rem; font-size: 0.85rem; }

@media (max-width: 768px) {
  .header-content { flex-direction: column; gap: 1rem; text-align: center; }
  .header-actions { flex-direction: column; }
  .gov-tabs { flex-wrap: wrap; }
  .gov-tabs button { width: 100%; text-align: left; border-bottom: 1px solid #e2e8f0; }
  .gov-tabs button.active { border-left: 4px solid #0056b3; border-bottom: none; }
  .section-header { flex-direction: column; align-items: flex-start; gap: 1rem; }
}
</style>