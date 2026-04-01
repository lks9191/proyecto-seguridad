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
      </div>
    </header>

    <main class="login-wrapper">
      <div class="auth-card">
        <h2>Registro Ciudadano</h2>
        <p class="auth-subtitle">Cree una cuenta para acceder a los servicios de la Sede Electrónica</p>
        
        <form @submit.prevent="submitRegister">
          
          <div class="input-group">
            <label for="carnet">Carnet de Identidad (CI)</label>
            <input id="carnet" v-model="carnet" type="text" required placeholder="Ej: 1234567" class="gov-input" />
          </div>

          <div class="row-inputs">
            <div class="input-group">
              <label for="names">Nombres</label>
              <input id="names" v-model="names" type="text" required placeholder="Ej: Juan Carlos" class="gov-input" />
            </div>
          </div>

          <div class="row-inputs">
            <div class="input-group">
              <label for="paternal_surname">Apellido Paterno</label>
              <input id="paternal_surname" v-model="paternal_surname" type="text" required placeholder="Ej: Perez" class="gov-input" />
            </div>
            <div class="input-group">
              <label for="maternal_surname">Apellido Materno</label>
              <input id="maternal_surname" v-model="maternal_surname" type="text" placeholder="Ej: Rodriguez" class="gov-input" />
            </div>
          </div>

          <div class="input-group">
            <label for="email">Correo Electrónico</label>
            <input id="email" v-model="email" type="email" required autocomplete="email" class="gov-input" />
          </div>
          
          <div class="input-group">
            <label for="password">Contraseña</label>
            <input id="password" v-model="password" type="password" required autocomplete="new-password" class="gov-input" />
          </div>

          <div class="input-group">
            <label for="confirmPassword">Confirmar Contraseña</label>
            <input id="confirmPassword" v-model="confirmPassword" type="password" required autocomplete="new-password" class="gov-input" />
          </div>

          <div class="error-container">
            <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
          </div>
          
          <button type="submit" :disabled="isLoading" class="gov-btn-primary">
            {{ isLoading ? 'Procesando registro...' : 'CREAR CUENTA' }}
          </button>

          <div class="register-section">
            <p>¿Ya está registrado en el sistema?</p>
            <router-link to="/login" class="gov-link">Volver al inicio de sesión</router-link>
          </div>
        </form>
      </div>
    </main>

    <ModalAviso 
      :show="registrationSuccess" 
      title="Registro Exitoso" 
      message="Su cuenta ha sido creada correctamente. Ahora puede iniciar sesión con su número de carnet."
      type="success"
      @close="$router.push({ name: 'login' })"
    />

    <footer class="gov-footer">
      <p>© 2026 Plataforma de Identidad y Trámites Digitales - SUT-BO.</p>
    </footer>
  </div>
</template>

<script setup>
import { useRegister } from '@/composables/useRegister'
import ModalAviso from '@/components/common/ModalAviso.vue'

const { 
  carnet,
  names,
  paternal_surname,
  maternal_surname,
  email, 
  password, 
  confirmPassword, 
  registrationSuccess,
  errorMessage, 
  isLoading, 
  submitRegister 
} = useRegister()
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
  overflow-y: auto; /* Para permitir scroll si la pantalla es muy pequeña */
}

/* --- HEADER --- */
.gov-header {
  background-color: #2c3136;
  color: #ffffff;
  padding: 1.5rem 0;
  border-bottom: 4px solid #0056b3;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.shield-icon {
  font-size: 2.5rem;
}

.titles h1 {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.titles p {
  margin: 0;
  font-size: 0.85rem;
  color: #a0aab2;
}

/* --- CONTENEDOR CENTRAL --- */
.login-wrapper {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem 1rem;
}

/* --- TARJETA DE REGISTRO --- */
.auth-card {
  background-color: #ffffff;
  padding: 2.5rem 3rem;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
  border-top: 4px solid #0056b3;
}

.auth-card h2 {
  color: #2c3136;
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.auth-subtitle {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 2rem;
  line-height: 1.4;
}

/* --- FORMULARIOS --- */
.input-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.2rem;
  flex: 1;
}

.row-inputs {
  display: flex;
  gap: 1rem;
  width: 100%;
}

label {
  color: #4a5568;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 0.4rem;
}

.gov-input {
  background-color: #ffffff;
  border: 1px solid #cbd5e0;
  color: #2d3748;
  font-size: 1rem;
  padding: 0.75rem;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  font-family: inherit;
}

.gov-input:focus {
  border-color: #0056b3;
  box-shadow: 0 0 0 3px rgba(0, 86, 179, 0.1);
}

/* --- MENSAJES DE ERROR --- */
.error-container {
  min-height: 1.5rem; /* Ajustado ligeramente para hacer espacio al botón */
  margin-top: 0.5rem;
  margin-bottom: 1rem;
}

.error-msg {
  color: #c53030;
  font-size: 0.85rem;
  background: #fff5f5;
  padding: 0.75rem;
  border-left: 4px solid #c53030;
  margin: 0;
}

/* --- BOTONES Y ENLACES --- */
.gov-btn-primary {
  background-color: #0056b3;
  color: #ffffff;
  border: none;
  padding: 0.85rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.2s;
  margin-top: 0.5rem;
}

.gov-btn-primary:hover:not(:disabled) {
  background-color: #004494;
}

.gov-btn-primary:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.register-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
  text-align: center;
}

.register-section p {
  color: #4a5568;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.gov-link {
  color: #0056b3;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
}

.gov-link:hover {
  text-decoration: underline;
}

/* --- FOOTER --- */
.gov-footer {
  background-color: #2c3136;
  color: #a0aab2;
  text-align: center;
  padding: 1.5rem;
  font-size: 0.85rem;
}

/* --- RESPONSIVE --- */
@media (max-width: 480px) {
  .auth-card {
    padding: 2rem 1.5rem;
  }
  .titles h1 {
    font-size: 1.2rem;
  }
}
</style>