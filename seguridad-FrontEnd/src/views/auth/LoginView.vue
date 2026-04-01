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
        <h2>Identificación de Usuario</h2>
        <p class="auth-subtitle">Ingrese sus credenciales para acceder a la Sede Electrónica</p>
        
        <form @submit.prevent="submitLogin">
          <div class="input-group">
            <label for="username">Carnet de Identidad (CI)</label>
            <input id="username" v-model="username" type="text" required autocomplete="username" class="gov-input" placeholder="Ingrese su número de carnet" />
          </div>

          <div class="input-group">
            <label for="password">Contraseña</label>
            <input id="password" v-model="password" type="password" required autocomplete="current-password" class="gov-input" />
          </div>

          <div class="input-group">
            <label for="role">Acceder como</label>
            <select id="role" v-model="role" class="gov-select">
              <option value="USER">CIUDADANO (USUARIO)</option>
              <option value="ADMIN">FUNCIONARIO (ADMINISTRADOR)</option>
              <option value="AUDITOR">CONTROL INTERNO (AUDITOR)</option>
            </select>
          </div>

          <div class="error-container">
            <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
          </div>

          <button type="submit" :disabled="isLoading" class="gov-btn-primary">
            {{ isLoading ? 'Verificando datos...' : 'Acceder al sistema' }}
          </button>

          <div class="register-section">
            <p>¿Aún no está registrado en el sistema?</p>
            <router-link to="/register" class="gov-link">Crear una nueva cuenta ciudadana</router-link>
          </div>
        </form>
      </div>
    </main>

    <footer class="gov-footer">
      <p>© 2026 Plataforma de Identidad y Trámites Digitales - SUT-BO.</p>
    </footer>
  </div>
</template>

<script setup>
import { useLogin } from '@/composables/useLogin'

const { username, password, role, errorMessage, isLoading, submitLogin } = useLogin()
</script>

<style scoped>
/* Reset de fuentes a un estilo más limpio y corporativo */
.gov-layout {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa; /* Fondo gris muy claro, estilo papel/web corporativa */
  margin: 0; /* Asegurar que no haya márgenes si Vue los inyecta */
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
}

/* --- HEADER GUBERNAMENTAL (Inspirado en la imagen) --- */
.gov-header {
  background-color: #2c3136; /* Gris carbón oscuro */
  color: #ffffff;
  padding: 1.5rem 0;
  border-bottom: 4px solid #0056b3; /* Línea institucional azul */
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
  flex-grow: 1; /* Ocupa el espacio entre header y footer */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem 1rem;
}

/* --- TARJETA DE IDENTIFICACIÓN --- */
.auth-card {
  background-color: #ffffff;
  padding: 2.5rem 3rem;
  width: 100%;
  max-width: 450px;
  /* Sombras sutiles, nada de neón */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
  border-top: 4px solid #0056b3; /* Detalle corporativo */
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
}

label {
  color: #4a5568;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 0.4rem;
}

.gov-input, .gov-select {
  background-color: #ffffff;
  border: 1px solid #cbd5e0;
  color: #2d3748;
  font-size: 1rem;
  padding: 0.75rem;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  font-family: inherit;
}

.gov-input:focus, .gov-select:focus {
  border-color: #0056b3;
  box-shadow: 0 0 0 3px rgba(0, 86, 179, 0.1); /* Efecto de foco accesible */
}

/* --- MENSAJES DE ERROR --- */
.error-container {
  min-height: 2.5rem;
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
}

.gov-btn-primary:hover:not(:disabled) {
  background-color: #004494;
}

.gov-btn-primary:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.register-section {
  margin-top: 2rem;
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