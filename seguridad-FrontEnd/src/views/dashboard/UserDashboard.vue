<template>
  <div class="dashboard-wrapper">
    <div class="user-dashboard glow-box">
      <header class="dashboard-header">
        <h2>Panel de Usuario (Perfil Privado)</h2>
        <button @click="handleLogout" class="logout-btn">CERRAR SESIÓN</button>
      </header>

      <div v-if="message" class="alert-info" @click="message = ''">
        {{ message }}
      </div>

      <div v-if="isLoading" class="loading">Cargando tu información...</div>

      <div v-else class="content-grid">
        <section class="card profile-card">
          <div class="card-header">
            <h3>Mis Datos Personales</h3>
            <button @click="showUpdateModal = true" class="edit-btn">EDITAR PERFIL</button>
          </div>
          <p class="subtitle">Solo tú tienes acceso a esta información (Confidencialidad).</p>
          <div v-if="profile" class="profile-details">
            <p><strong>Usuario:</strong> {{ profile.username }}</p>
            <p><strong>Email:</strong> {{ profile.email }}</p>
            <p><strong>Roles:</strong>
              <span v-for="r in profile.roles" :key="r" class="role-badge">{{ r }}</span>
            </p>
            <div class="two-fa-row">
              <p><strong>2FA:</strong>
                <span :class="['badge', profile.is_2fa_enabled ? 'active' : 'inactive']">
                  {{ profile.is_2fa_enabled ? 'Activado (Email)' : 'Desactivado' }}
                </span>
              </p>
              <button v-if="!profile.is_2fa_enabled" @click="openTwoFAModal" class="setup-2fa-btn">
                ACTIVAR 2FA
              </button>
              <button v-else @click="handleDisable2FA" class="disable-2fa-link">
                Desactivar
              </button>
            </div>
            <p><strong>Miembro desde:</strong> {{ formatDate(profile.created_at) }}</p>
          </div>
        </section>

        <section class="card public-card">
          <h3>Información Pública</h3>
          <p class="subtitle">Avisos generales del sistema.</p>
          <ul class="public-list">
            <li v-for="item in publicData" :key="item.id">
              <strong>{{ item.title }}:</strong> {{ item.content }}
            </li>
          </ul>
        </section>
      </div>
    </div>

    <!-- UPDATE PROFILE MODAL -->
    <div v-if="showUpdateModal" class="modal-overlay">
      <div class="modal-content glow-box">
        <h3>Editar Mi Perfil</h3>
        <form @submit.prevent="handleUpdate">
          <div class="input-group">
            <label>Nuevo Usuario</label>
            <input v-model="editForm.username" class="neon-input" :placeholder="profile?.username">
          </div>
          <div class="input-group">
            <label>Nuevo Email</label>
            <input v-model="editForm.email" type="email" class="neon-input" :placeholder="profile?.email">
          </div>
          <div class="input-group">
            <label>Nueva Contraseña (Fuerte)</label>
            <input v-model="editForm.password" type="password" class="neon-input" placeholder="********">
            <small class="hint">Dejar en blanco para no cambiar.</small>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showUpdateModal = false" class="cancel-btn">CANCELAR</button>
            <button type="submit" class="submit-btn" :disabled="isUpdating">
              {{ isUpdating ? 'GUARDANDO...' : 'GUARDAR CAMBIOS' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 2FA SETUP MODAL -->
    <div v-if="showTwoFAModal" class="modal-overlay">
      <div class="modal-content glow-box">
        <h3>Configurar Segundo Factor (Email)</h3>
        <div v-if="twoFAStep === 'request'">
          <p>Para activar el 2FA, enviaremos un código de seguridad a tu correo: <strong>{{ profile?.email }}</strong>
          </p>
          <div class="modal-actions">
            <button @click="showTwoFAModal = false" class="cancel-btn">CANCELAR</button>
            <button @click="handleRequestOTP" class="submit-btn" :disabled="isVerifying">
              {{ isVerifying ? 'ENVIANDO...' : 'ENVIAR CÓDIGO' }}
            </button>
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
              {{ isVerifying ? 'VERIFICANDO...' : 'CONFIRMAR Y ACTIVAR' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUser } from '@/composables/useUser'

const {
  profile, publicData, isLoading, message,
  updateProfile, handleLogout, request2FA, confirm2FA, disable2FA
} = useUser()

const showUpdateModal = ref(false)
const showTwoFAModal = ref(false)
const twoFAStep = ref('request')
const otpToken = ref('')
const isVerifying = ref(false)
const isUpdating = ref(false)
const editForm = ref({ username: '', email: '', password: '' })

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
  if (confirm('¿Estás seguro de desactivar el 2FA? Tu cuenta será menos segura.')) {
    await disable2FA()
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString()
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
  max-width: 900px;
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

h2 {
  color: #0096ff;
}

.logout-btn {
  background: transparent;
  color: #ff4d4d;
  border: 1px solid #ff4d4d;
  border-radius: 30px;
  padding: 0.5rem 1.2rem;
  cursor: pointer;
  font-weight: bold;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.card {
  background-color: #1a1a1a;
  border: 1px solid #333;
  padding: 1.5rem;
  border-radius: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.edit-btn {
  background: #0096ff;
  color: white;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.setup-2fa-btn {
  background: transparent;
  color: #0096ff;
  border: 1px solid #0096ff;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.75rem;
  font-weight: bold;
}

.disable-2fa-link {
  background: transparent;
  border: none;
  color: #ff4d4d;
  text-decoration: underline;
  cursor: pointer;
  font-size: 0.75rem;
  margin-left: 10px;
}

.two-fa-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 1rem 0;
}

.subtitle {
  color: #888;
  font-size: 0.85rem;
  margin-bottom: 1.5rem;
}

.profile-details p {
  margin: 1rem 0;
  color: #ccc;
}

strong {
  color: #0096ff;
}

.role-badge {
  background: rgba(0, 150, 255, 0.1);
  color: #0096ff;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.8rem;
  margin-left: 5px;
}

.badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-weight: bold;
  font-size: 0.85em;
  display: inline-block;
}

.active {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
  border: 1px solid #28a745;
}

.inactive {
  background: rgba(255, 77, 77, 0.1);
  color: #ff4d4d;
  border: 1px solid #ff4d4d;
}

.public-list {
  padding-left: 1.2rem;
  color: #ccc;
}

.public-list li {
  margin-bottom: 1rem;
  font-size: 0.95rem;
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
  cursor: pointer;
  border-left: 4px solid #0096ff;
}

/* MODAL */
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
}

.code-input {
  text-align: center;
  font-size: 1.5rem;
  letter-spacing: 10px;
}

.hint {
  color: #666;
  font-size: 0.75rem;
  margin-top: 0.3rem;
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

@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>