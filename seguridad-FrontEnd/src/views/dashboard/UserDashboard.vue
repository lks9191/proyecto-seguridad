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
          <button @click="handleConfirmLogout" class="gov-btn-logout">Cerrar Sesión</button>
        </div>
      </div>
    </header>

    <main class="dashboard-main">
      <div class="dashboard-header-bar">
        <h2>Panel de Ciudadano</h2>
        <p class="subtitle">Bienvenido a la Sede Electrónica</p>
      </div>

      <ModalConfirmacion :show="confirmModal.show" :title="confirmModal.title" :message="confirmModal.message"
        @cancel="confirmModal.show = false" @confirm="handleConfirmedAction" />

      <ModalAviso :show="noticeModal.show" :title="noticeModal.title" :message="noticeModal.message"
        :type="noticeModal.type" @close="noticeModal.show = false" />

      <div v-if="message" class="alert-info" @click="message = ''">
        {{ message }}
      </div>

      <div v-if="isLoading" class="loading">Cargando su información...</div>

      <div v-else>
        <div class="content-grid">
          <UserProfileCard :profile="profile" @open-edit="showUpdateModal = true" @setup-2fa="openTwoFAModal"
            @disable-2fa="handleDisable2FA" />

          <PublicNoticesCard :publicData="publicData" />
        </div>

        <TramitesListCard :tramites="misTramites" @open-new-tramite="showNewTramiteModal = true" />
      </div>
    </main>

    <footer class="gov-footer">
      <p>© 2026 Plataforma de Identidad y Trámites Digitales - SUT-BO.</p>
    </footer>

    <div v-if="showUpdateModal" class="gov-modal-overlay">
      <div class="gov-modal-content">
        <h3>Editar Mi Perfil</h3>
        <p class="modal-subtitle">Actualice su información de contacto ciudadana.</p>

        <form @submit.prevent="handleUpdate">
          <div class="input-group">
            <label>Nombres y Apellidos</label>
            <div class="row-inputs">
              <input v-model="editForm.names" class="gov-input" placeholder="Nombres">
              <input v-model="editForm.paternal_surname" class="gov-input" placeholder="Ap. Paterno">
            </div>
          </div>
          <div class="input-group">
            <label>Carnet de Identidad (CI)</label>
            <input v-model="editForm.username" class="gov-input" :placeholder="profile?.carnet">
          </div>
          <div class="input-group">
            <label>Nuevo Correo Electrónico</label>
            <input v-model="editForm.email" type="email" class="gov-input" :placeholder="profile?.email">
          </div>
          <div class="input-group">
            <label>Nueva Contraseña (Fuerte)</label>
            <input v-model="editForm.password" type="password" class="gov-input" placeholder="********">
            <small class="hint">Dejar en blanco para no cambiar la contraseña actual.</small>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showUpdateModal = false" class="gov-btn-secondary">Cancelar</button>
            <button type="submit" class="gov-btn-primary" :disabled="isUpdating">
              {{ isUpdating ? 'Guardando...' : 'Guardar Cambios' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showTwoFAModal" class="gov-modal-overlay">
      <div class="gov-modal-content">
        <h3>Configurar Segundo Factor (2FA)</h3>

        <div v-if="twoFAStep === 'request'">
          <p class="modal-subtitle">Para activar la autenticación de dos factores, enviaremos un código de seguridad a
            su correo institucional: <strong>{{ profile?.email }}</strong></p>
          <div class="modal-actions">
            <button @click="showTwoFAModal = false" class="gov-btn-secondary">Cancelar</button>
            <button @click="handleRequestOTP" class="gov-btn-primary" :disabled="isVerifying">
              {{ isVerifying ? 'Enviando...' : 'Enviar Código' }}
            </button>
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

    <div v-if="showNewTramiteModal" class="gov-modal-overlay">
      <div class="gov-modal-content">
        <h3>Iniciar Nuevo Trámite</h3>
        <p class="modal-subtitle">Seleccione el tipo de certificado que desea solicitar a la administración pública.</p>

        <form @submit.prevent="simularNuevoTramite">
          <div class="input-group">
            <label>Tipo de Trámite</label>
            <select class="gov-select" required>
              <option value="" disabled selected>-- Seleccione una opción --</option>
              <option value="nacimiento">Certificado de Nacimiento Original</option>
              <option value="antecedentes">Certificado de Antecedentes (FELCC)</option>
              <option value="licencia">Renovación de Licencia de Conducir</option>
              <option value="cedula">Cédula de Identidad Electrónica</option>
              <option value="matrimonio">Certificado de Matrimonio</option>
            </select>
          </div>

          <div class="modal-actions">
            <button type="button" @click="showNewTramiteModal = false" class="gov-btn-secondary">Cancelar</button>
            <button type="submit" class="gov-btn-primary">Solicitar Aprobación</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUser } from '@/composables/useUser'
import ModalConfirmacion from '@/components/common/ModalConfirmacion.vue'
import ModalAviso from '@/components/common/ModalAviso.vue'

import UserProfileCard from '@/components/dashboard/UserProfileCard.vue'
import PublicNoticesCard from '@/components/dashboard/PublicNoticesCard.vue'
import TramitesListCard from '@/components/dashboard/TramitesListCard.vue'

const {
  profile, publicData, isLoading, message,
  updateProfile, handleLogout, request2FA, confirm2FA, disable2FA
} = useUser()

const showUpdateModal = ref(false)
const showTwoFAModal = ref(false)
const showNewTramiteModal = ref(false)

const twoFAStep = ref('request')
const otpToken = ref('')
const isVerifying = ref(false)
const isUpdating = ref(false)
const editForm = ref({ username: '', email: '', password: '', names: '', paternal_surname: '', maternal_surname: '' })

// Estados para modales genéricos
const confirmModal = ref({ show: false, title: '', message: '', action: null })
const noticeModal = ref({ show: false, title: '', message: '', type: 'info' })

const showAlert = (title, message, type = 'info') => {
  noticeModal.value = { show: true, title, message, type }
}

const showConfirm = (title, message, action) => {
  confirmModal.value = { show: true, title, message, action }
}

const handleConfirmedAction = async () => {
  if (confirmModal.value.action) await confirmModal.value.action()
  confirmModal.value.show = false
}

const handleConfirmLogout = () => {
  showConfirm('Cerrar Sesión', '¿Está seguro de que desea salir?', handleLogout)
}

const misTramites = ref([
  { id: 'SUT-0089', tipo: 'Certificado de Nacimiento Original', fecha: '2026-03-20', estado: 'Aprobado', estadoClass: 'success' },
  { id: 'SUT-0145', tipo: 'Renovación Cédula de Identidad', fecha: '2026-03-22', estado: 'En Revisión', estadoClass: 'warning' },
  { id: 'SUT-0201', tipo: 'Certificado de Antecedentes (FELCC)', fecha: '2026-03-24', estado: 'Pendiente de Pago', estadoClass: 'danger' },
])

const simularNuevoTramite = () => {
  showAlert('Trámite Iniciado', 'Solicitud enviada correctamente. Un administrador revisará su petición.', 'success')
  showNewTramiteModal.value = false
}

const handleUpdate = async () => {
  isUpdating.value = true
  const success = await updateProfile(editForm.value)
  isUpdating.value = false
  if (success) {
    showUpdateModal.value = false
    editForm.value = { username: '', email: '', password: '' }
  }
}

const openTwoFAModal = () => {
  twoFAStep.value = 'request'
  otpToken.value = ''
  showTwoFAModal.value = true
}

const handleRequestOTP = async () => {
  isVerifying.value = true
  const success = await request2FA()
  isVerifying.value = false
  if (success) {
    twoFAStep.value = 'verify'
  }
}

const handleConfirm2FA = async () => {
  isVerifying.value = true
  const success = await confirm2FA(otpToken.value)
  isVerifying.value = false
  if (success) {
    showTwoFAModal.value = false
  }
}

const handleDisable2FA = async () => {
  showConfirm(
    'Desactivar 2FA',
    '¿Está seguro de desactivar el 2FA? Su cuenta será menos segura.',
    async () => {
      await disable2FA()
      showAlert('Seguridad', 'El Segundo Factor ha sido desactivado.', 'info')
    }
  )
}
</script>

<style scoped>
/* Reset y fondo general */
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
  max-width: 1200px;
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
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  padding: 2rem;
  box-sizing: border-box;
}

.dashboard-header-bar {
  margin-bottom: 2rem;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 1rem;
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

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
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

/* --- MODALES GUBERNAMENTALES --- */
.gov-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(44, 49, 54, 0.7);
  /* Gris oscuro semi-transparente */
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

.input-group label {
  margin-bottom: 0.4rem;
  color: #4a5568;
  font-size: 0.85rem;
  font-weight: 600;
}

.gov-input,
.gov-select {
  background: #ffffff;
  color: #2d3748;
  border: 1px solid #cbd5e0;
  padding: 0.75rem;
  border-radius: 4px;
  outline: none;
  font-family: inherit;
  font-size: 0.95rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.gov-input:focus,
.gov-select:focus {
  border-color: #0056b3;
  box-shadow: 0 0 0 3px rgba(0, 86, 179, 0.1);
}

.code-input {
  text-align: center;
  font-size: 1.5rem;
  letter-spacing: 8px;
  font-weight: bold;
}

.hint {
  color: #718096;
  font-size: 0.75rem;
  margin-top: 0.4rem;
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
  transition: all 0.2s;
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
  transition: all 0.2s;
}

.gov-btn-primary:hover:not(:disabled) {
  background: #004494;
}

.gov-btn-primary:disabled {
  background: #a0aec0;
  cursor: not-allowed;
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
  .content-grid {
    grid-template-columns: 1fr;
  }

  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .dashboard-main {
    padding: 1rem;
  }
}
</style>