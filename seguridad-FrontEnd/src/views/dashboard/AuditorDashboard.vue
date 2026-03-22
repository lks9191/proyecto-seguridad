<template>
  <div class="dashboard-wrapper">
    <div class="auditor-dashboard glow-box">
      <header class="dashboard-header">
        <div class="header-left">
          <h2>Panel de Auditoría</h2>
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

      <div v-if="isLoading" class="loading">Cargando logs de auditoría...</div>

      <div v-else class="tab-content">
        <div class="section">
          <h3>Sesiones Activas Actualmente</h3>
          <p class="subtitle">Monitoreo en tiempo real de accesos al sistema.</p>
          <div class="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>Dirección IP</th>
                  <th>Fecha de Inicio</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="session in activeSessions" :key="session.id">
                  <td>{{ session.username }}</td>
                  <td><code class="ip-text">{{ session.ip_address }}</code></td>
                  <td>{{ formatDate(session.created_at) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="section mt-4">
          <h3>Historial de Accesos y Eventos</h3>
          <p class="subtitle">Registro histórico para fines de auditoría legal.</p>
          <div class="table-responsive">
            <table>
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>Acción Realizada</th>
                  <th>Dirección IP</th>
                  <th>Fecha y Hora</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="log in sessionHistory" :key="log.id">
                  <td>{{ log.username }}</td>
                  <td>
                    <span :class="['event-badge', getEventClass(log.action)]">
                      {{ log.action }}
                    </span>
                  </td>
                  <td><code class="ip-text">{{ log.ip_address }}</code></td>
                  <td>{{ formatDate(log.timestamp) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- 2FA SETUP MODAL (AUDITOR PERSO) -->
    <div v-if="showTwoFAModal" class="modal-overlay">
      <div class="modal-content glow-box">
        <h3>Seguridad: 2FA vía Email</h3>
        <div v-if="twoFAStep === 'request'">
          <p v-if="!profile?.is_2fa_enabled">Protege tu acceso de auditor. Enviaremos un código a <strong>{{
            profile?.email }}</strong>.</p>
          <p v-else>El segundo factor está activo manejando la integridad de tu cuenta.</p>
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
import { ref } from 'vue'
import { useAuditor } from '@/composables/useAuditor'
import { useUser } from '@/composables/useUser'

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

const handleDisable2FA = async () => {
  if (confirm('¿Desactivar 2FA?')) {
    await disable2FA()
    showTwoFAModal.value = false
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString()
}

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

h2 {
  color: #0096ff;
  margin: 0;
}

.logout-btn {
  background: transparent;
  color: #ff4d4d;
  border: 1px solid #ff4d4d;
  border-radius: 30px;
  padding: 0.5rem 1.2rem;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s;
}

.logout-btn:hover {
  background: #ff4d4d;
  color: white;
}

.refresh-btn {
  background: transparent;
  color: #0096ff;
  border: 1px solid #0096ff;
  border-radius: 30px;
  padding: 0.5rem 1.2rem;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s;
  margin-right: 1rem;
}

.refresh-btn:hover {
  background: #0096ff;
  color: white;
}

.section {
  background: #1a1a1a;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #333;
  margin-bottom: 2rem;
}

h3 {
  margin-bottom: 0.2rem;
}

.subtitle {
  color: #888;
  font-size: 0.85rem;
  margin-bottom: 1.5rem;
}

.table-responsive {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #333;
}

th {
  color: #0096ff;
  font-weight: bold;
  font-size: 0.9rem;
  text-transform: uppercase;
}

.ip-text {
  background: #000;
  color: #00ff00;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
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

.alert-info {
  background: rgba(0, 150, 255, 0.1);
  color: #0096ff;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  border-left: 4px solid #0096ff;
  cursor: pointer;
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

.neon-input {
  background: #0d0d0d;
  color: white;
  border: 1px solid #444;
  padding: 0.6rem;
  border-radius: 4px;
  outline: none;
}

.code-input {
  text-align: center;
  font-size: 1.5rem;
  letter-spacing: 10px;
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
</style>