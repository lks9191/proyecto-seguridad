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
            <span class="username">{{ profile.carnet }}</span>
            <span :class="['status-dot', profile.is_2fa_enabled ? 'active' : 'inactive']"
              :title="profile.is_2fa_enabled ? '2FA Activo' : '2FA Inactivo'"></span>
            <button @click="openTwoFAModal" class="mini-2fa-btn">
              {{ profile.is_2fa_enabled ? '2FA OK' : 'Activar 2FA' }}
            </button>
          </div>

          <button @click="refresh" class="gov-btn-outline-light">Refrescar</button>
          <button @click="handleConfirmLogout" class="gov-btn-logout">Cerrar Sesión</button>
        </div>
      </div>
    </header>

    <main class="dashboard-main">
      <div class="dashboard-header-bar">
        <h2>Panel de Auditoría y Transparencia</h2>
        <p class="subtitle">Monitoreo de Solo Lectura para garantizar la Integridad del sistema.</p>
      </div>

      <ModalConfirmacion :show="showConfirm" :title="confirmData.title" :message="confirmData.message"
        @cancel="showConfirm = false" @confirm="handleConfirmAction" />

      <div v-if="message" class="alert-info" @click="message = ''">
        {{ message }}
      </div>

      <div v-if="isLoading" class="loading">Cargando registros de auditoría...</div>

      <div v-else class="tab-content">
        <div class="gov-card mb-2">
          <div class="section-header">
            <h3>Sesiones Activas Actualmente</h3>
            <p class="section-subtitle">Monitoreo en tiempo real de accesos a la plataforma.</p>
          </div>

          <div class="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>Dirección IP</th>
                  <th>Inicio de Sesión</th>
                  <th>Expiración Estimada</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="session in activeSessions" :key="session.id">
                  <td class="fw-bold">{{ session.username }}</td>
                  <td class="mono-text">{{ session.ip_address }}</td>
                  <td>{{ formatDate(session.login_at) }}</td>
                  <td><span class="event-badge warning">{{ formatDate(session.expires_at) }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="gov-card">
          <div class="section-header">
            <h3>Historial de Accesos y Eventos</h3>
            <p class="section-subtitle">Registro histórico inmutable para fines de auditoría legal.</p>
          </div>

          <div class="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>Login (Fecha/Hora)</th>
                  <th>Observación Login</th>
                  <th>Logout (Fecha/Hora)</th>
                  <th>Observación Logout</th>
                  <th>Dirección IP</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="log in sessionHistory" :key="log.id">
                  <td class="fw-bold">{{ log.username }}</td>
                  <td>{{ formatDate(log.login_at) }}</td>
                  <td><small>{{ log.login_obs }}</small></td>
                  <td>{{ log.is_active ? 'SESIÓN ACTIVA' : formatDate(log.logout_at) }}</td>
                  <td><small>{{ log.is_active ? '-' : log.logout_obs }}</small></td>
                  <td class="mono-text">{{ log.ip_address }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>

    <footer class="gov-footer">
      <p>© 2026 Plataforma de Identidad y Trámites Digitales - SUT-BO.</p>
    </footer>

    <div v-if="showTwoFAModal" class="gov-modal-overlay">
      <div class="gov-modal-content">
        <h3>Seguridad de la Cuenta (2FA)</h3>

        <div v-if="twoFAStep === 'request'">
          <p class="modal-subtitle" v-if="!profile?.is_2fa_enabled">
            Para garantizar la transparencia de sus auditorías, asegure su cuenta. Enviaremos un código a: <strong>{{
              profile?.email }}</strong>
          </p>
          <p class="modal-subtitle" v-else>
            El segundo factor está activo protegiendo la integridad de su cuenta de Auditor.
          </p>
          <div class="modal-actions">
            <button @click="showTwoFAModal = false" class="gov-btn-secondary">Cancelar</button>
            <button v-if="!profile?.is_2fa_enabled" @click="handleRequestOTP" class="gov-btn-primary"
              :disabled="isVerifying">
              {{ isVerifying ? 'Enviando...' : 'Enviar Código' }}
            </button>
            <button v-else @click="handleDisable2FA" class="gov-btn-danger">Desactivar 2FA</button>
          </div>
        </div>

        <div v-else>
          <p class="modal-subtitle">Ingrese el código de 6 dígitos enviado a su correo institucional.</p>
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
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuditor } from '@/composables/useAuditor'
import { useUser } from '@/composables/useUser'
import ModalConfirmacion from '@/components/common/ModalConfirmacion.vue'

const {
  activeSessions,
  sessionHistory,
  isLoading,
  message,
  handleLogout,
  refresh
} = useAuditor()

const { profile, request2FA, confirm2FA, disable2FA } = useUser()

// 2FA Auditor
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

const showConfirm = ref(false)
const confirmData = ref({ title: '', message: '', action: null })

const requestConfirm = (title, message, action) => {
  confirmData.value = { title, message, action }
  showConfirm.value = true
}

const handleConfirmAction = async () => {
  if (confirmData.value.action) await confirmData.value.action()
  showConfirm.value = false
}

const handleConfirmLogout = () => {
  requestConfirm('Cerrar Sesión', '¿Está seguro de que desea salir del sistema?', handleLogout)
}

const handleDisable2FA = async () => {
  requestConfirm(
    'Desactivar 2FA',
    'Atención: Desactivar el 2FA disminuye la seguridad de sus accesos. ¿Desea continuar?',
    disable2FA
  )
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString()
}

let refreshInterval = null
onMounted(() => {
  refreshInterval = setInterval(() => {
    refresh(true)
  }, 10000) // Refresca cada 10 segundos
})

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval)
})

const getEventClass = (event) => {
  if (event.includes('SUCCESS')) return 'success'
  if (event.includes('FAILED') || event.includes('UNAUTHORIZED')) return 'danger'
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

.logo-area {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.shield-icon {
  font-size: 2rem;
}

.titles h1 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.titles p {
  margin: 0;
  font-size: 0.8rem;
  color: #a0aab2;
}

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

.username {
  font-weight: 600;
  font-size: 0.9rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #fca5a5;
}

.status-dot.active {
  background: #86efac;
}

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

.mini-2fa-btn:hover {
  color: #ffffff;
}

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

.gov-btn-outline-light:hover {
  background: rgba(255, 255, 255, 0.1);
}

.gov-btn-logout {
  background-color: #c53030;
  color: #ffffff;
  border: 1px solid #9b1c1c;
  padding: 0.5rem 1.2rem;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.gov-btn-logout:hover {
  background-color: #9b1c1c;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* --- CONTENIDO PRINCIPAL --- */
.dashboard-main {
  flex-grow: 1;
  max-width: 1300px;
  margin: 0 auto;
  width: 100%;
  padding: 2rem;
  box-sizing: border-box;
}

.dashboard-header-bar {
  margin-bottom: 2rem;
}

.dashboard-header-bar h2 {
  margin: 0 0 0.3rem 0;
  color: #2c3136;
  font-size: 1.8rem;
}

.subtitle {
  color: #4a5568;
  margin: 0;
  font-size: 1rem;
}

/* Tarjetas (Secciones) */
.gov-card {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border-top: 4px solid #0056b3;
  padding: 2rem;
}

.mb-2 {
  margin-bottom: 2rem;
}

.section-header {
  margin-bottom: 1.5rem;
}

h3 {
  margin: 0 0 0.3rem 0;
  color: #2c3136;
  font-size: 1.3rem;
  font-weight: 600;
}

.section-subtitle {
  margin: 0;
  color: #718096;
  font-size: 0.9rem;
}

/* --- TABLAS --- */
.table-responsive {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
}

th,
td {
  border-bottom: 1px solid #e2e8f0;
  padding: 12px 15px;
  text-align: left;
  font-size: 0.9rem;
  color: #4a5568;
}

th {
  background-color: #edf2f7;
  color: #2c3136;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.5px;
}

tr:hover {
  background-color: #f8fafc;
}

.fw-bold {
  font-weight: 600;
  color: #2c3136;
}

.mono-text {
  font-family: 'Courier New', Courier, monospace;
  color: #718096;
  font-size: 0.95em;
  background: #f8fafc;
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
}

/* Badges de Eventos */
.event-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  display: inline-block;
}

.success {
  background-color: #def7ec;
  color: #03543f;
  border: 1px solid #84e1bc;
}

.danger {
  background-color: #fde8e8;
  color: #9b1c1c;
  border: 1px solid #f8b4b4;
}

.warning {
  background-color: #fef3c7;
  color: #92400e;
  border: 1px solid #fde68a;
}

.default {
  background-color: #f1f5f9;
  color: #475569;
  border: 1px solid #cbd5e0;
}

/* --- MODALES --- */
.gov-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(44, 49, 54, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.gov-modal-content {
  background: #ffffff;
  width: 90%;
  max-width: 500px;
  padding: 2.5rem;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  border-top: 4px solid #0056b3;
}

.gov-modal-content h3 {
  margin-top: 0;
  color: #2c3136;
  font-size: 1.4rem;
  margin-bottom: 0.5rem;
}

.modal-subtitle {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
  line-height: 1.4;
}

.input-group {
  margin-bottom: 1.2rem;
  display: flex;
  flex-direction: column;
}

.gov-input {
  background: #ffffff;
  color: #2d3748;
  border: 1px solid #cbd5e0;
  padding: 0.75rem;
  border-radius: 4px;
  outline: none;
  font-family: inherit;
  font-size: 0.95rem;
}

.gov-input:focus {
  border-color: #0056b3;
  box-shadow: 0 0 0 3px rgba(0, 86, 179, 0.1);
}

.code-input {
  text-align: center;
  font-size: 1.5rem;
  letter-spacing: 8px;
  font-weight: bold;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  border-top: 1px solid #e2e8f0;
  padding-top: 1.5rem;
}

.gov-btn-secondary {
  background: #edf2f7;
  color: #4a5568;
  border: 1px solid #cbd5e0;
  padding: 0.6rem 1.2rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.gov-btn-secondary:hover {
  background: #e2e8f0;
}

.gov-btn-primary {
  background: #0056b3;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.gov-btn-primary:hover:not(:disabled) {
  background: #004494;
}

.gov-btn-primary:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}

.gov-btn-danger {
  background: #c53030;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.alert-info {
  background: #e6f7ff;
  color: #0056b3;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
  cursor: pointer;
  border-left: 4px solid #0056b3;
  font-weight: 500;
}

.loading {
  text-align: center;
  color: #0056b3;
  padding: 2rem;
  font-weight: 600;
}

/* --- FOOTER --- */
.gov-footer {
  background-color: #2c3136;
  color: #a0aab2;
  text-align: center;
  padding: 1.5rem;
  font-size: 0.85rem;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .header-actions {
    flex-direction: column;
    width: 100%;
  }

  .dashboard-main {
    padding: 1rem;
  }
}
</style>