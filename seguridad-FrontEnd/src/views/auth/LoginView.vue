<template>
  <div class="login-wrapper">
    <div class="glow-box">
      <h2>IDENTIFICACIÓN</h2>
      <form @submit.prevent="submitLogin">

        <div class="input-group">
          <label for="username">Usuario</label>
          <input id="username" v-model="username" type="text" required autocomplete="username" class="neon-input" />
        </div>

        <div class="input-group">
          <label for="password">Contraseña</label>
          <input id="password" v-model="password" type="password" required autocomplete="current-password"
            class="neon-input" />
        </div>

        <div class="input-group">
          <label for="role">Ingresar como</label>
          <select id="role" v-model="role" class="neon-select">
            <option value="USER">USUARIO</option>
            <option value="ADMIN">ADMINISTRADOR</option>
            <option value="AUDITOR">AUDITOR</option>
          </select>
        </div>

        <div class="error-container">
          <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
        </div>

        <p class="register-link">
          ¿No tienes cuenta? <router-link to="/register">Regístrate aquí</router-link>
        </p>

        <button type="submit" :disabled="isLoading">
          {{ isLoading ? 'VERIFICANDO...' : 'INGRESAR' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { useLogin } from '@/composables/useLogin'

const { username, password, role, errorMessage, isLoading, submitLogin } = useLogin()
</script>

<style scoped>
.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: #0d0d0d;
  padding: 1rem;
  box-sizing: border-box;
  z-index: 9999;
}

.glow-box {
  background-color: #111111;
  padding: 3rem 2.5rem;
  border-radius: 20px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 0 20px rgba(0, 150, 255, 0.3),
    inset 0 0 10px rgba(0, 150, 255, 0.05);
  border: 1px solid rgba(0, 150, 255, 0.2);
  box-sizing: border-box;
}

h2 {
  text-align: center;
  color: #0096ff;
  margin-bottom: 2.5rem;
  font-size: 1.6rem;
  letter-spacing: 2px;
  font-weight: bold;
}

.input-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5rem;
}

label {
  color: #888;
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.neon-input {
  background: transparent;
  border: none;
  border-bottom: 2px solid #333;
  color: #ffffff;
  font-size: 1rem;
  padding: 0.5rem 0;
  outline: none;
  transition: border-bottom-color 0.3s;
}

.neon-input:focus {
  border-bottom-color: #0096ff;
}

.neon-select {
  background: #0d0d0d;
  color: white;
  border: 1px solid #333;
  padding: 0.6rem;
  border-radius: 4px;
  outline: none;
  cursor: pointer;
  font-size: 0.9rem;
}

.neon-select:focus {
  border-color: #0096ff;
  box-shadow: 0 0 10px rgba(0, 150, 255, 0.2);
}

.error-container {
  min-height: 2.5rem;
  /* Espacio reservado para el mensaje de error */
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 0.5rem;
}

.error-msg {
  color: #ff4d4d;
  font-size: 0.85rem;
  text-align: center;
  background: rgba(255, 77, 77, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 4px;
  border-left: 3px solid #ff4d4d;
  width: 100%;
}

.register-link {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.85rem;
  color: #666;
}

.register-link a {
  color: #0096ff;
  text-decoration: none;
  font-weight: bold;
}

button {
  background-color: #0096ff;
  color: #ffffff;
  border: none;
  border-radius: 30px;
  padding: 1rem;
  font-size: 1rem;
  font-weight: bold;
  letter-spacing: 2px;
  cursor: pointer;
  width: 100%;
  margin-top: 1.5rem;
  box-shadow: 0 0 15px rgba(0, 150, 255, 0.4);
  transition: all 0.3s;
}

button:hover:not(:disabled) {
  background-color: #1aa3ff;
  box-shadow: 0 0 25px rgba(0, 150, 255, 0.6);
  transform: translateY(-2px);
}

button:disabled {
  background-color: #222;
  color: #555;
  box-shadow: none;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .glow-box {
    padding: 2rem 1.5rem;
  }

  h2 {
    font-size: 1.4rem;
  }
}
</style>