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
        <h2>Verificación de Seguridad (2FA)</h2>
        <p class="auth-subtitle">
          Hemos enviado un código temporal a su correo electrónico institucional. Por favor, ingréselo a continuación para continuar.
        </p>

        <form @submit.prevent="verifyCode">
          <div class="input-group">
            <label for="totp">Código de 6 dígitos</label>
            <input 
              id="totp" 
              v-model="totpCode" 
              type="text" 
              maxlength="6" 
              required 
              placeholder="123456" 
              class="gov-input code-input"
              autocomplete="off" 
            />
          </div>

          <div class="error-container">
            <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
          </div>

          <button type="submit" :disabled="isLoading" class="gov-btn-primary">
            {{ isLoading ? 'Verificando código...' : 'AUTENTICAR Y ACCEDER' }}
          </button>
        </form>
      </div>
    </main>

    <footer class="gov-footer">
      <p>© 2026 Plataforma de Identidad y Trámites Digitales - SUT-BO.</p>
    </footer>
  </div>
</template>

<script setup>
import { useTwoFactor } from '@/composables/useTwoFactor'

const { totpCode, errorMessage, isLoading, verifyCode } = useTwoFactor()
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

/* --- TARJETA DE 2FA --- */
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
  font-size: 1.4rem;
  font-weight: 600;
  text-align: center;
}

.auth-subtitle {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 2rem;
  line-height: 1.5;
  text-align: center;
}

/* --- FORMULARIOS --- */
.input-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.2rem;
}

label {
  color: #4a5568;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  text-align: center;
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

/* Input específico para códigos 2FA */
.code-input {
  text-align: center;
  font-size: 1.8rem;
  letter-spacing: 8px;
  font-weight: 600;
  padding: 1rem 0;
  color: #2c3136;
}

.code-input::placeholder {
  color: #cbd5e0;
  letter-spacing: 8px;
}

.code-input:focus::placeholder {
  color: transparent;
}

/* --- MENSAJES DE ERROR --- */
.error-container {
  min-height: 1.5rem;
  margin-top: 0.5rem;
  margin-bottom: 1.5rem;
}

.error-msg {
  color: #c53030;
  font-size: 0.85rem;
  background: #fff5f5;
  padding: 0.75rem;
  border-left: 4px solid #c53030;
  margin: 0;
  text-align: center;
}

/* --- BOTONES --- */
.gov-btn-primary {
  background-color: #0056b3;
  color: #ffffff;
  border: none;
  padding: 1rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.2s;
  border-radius: 4px;
}

.gov-btn-primary:hover:not(:disabled) {
  background-color: #004494;
}

.gov-btn-primary:disabled {
  background-color: #a0aec0;
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

/* --- RESPONSIVE --- */
@media (max-width: 480px) {
  .auth-card {
    padding: 2rem 1.5rem;
  }
  .titles h1 {
    font-size: 1.2rem;
  }
  .code-input {
    font-size: 1.5rem;
    letter-spacing: 6px;
  }
}
</style>