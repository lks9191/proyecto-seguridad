<template>
  <div class="login-wrapper">
    <div class="glow-box">
      <h2>Login</h2>
      <form @submit.prevent="submitLogin">
        
        <div class="input-group">
          <label for="username">Username</label>
          <input id="username" v-model="username" type="text" required autocomplete="username" />
        </div>
        
        <div class="input-group">
          <label for="password">Password</label>
          <input id="password" v-model="password" type="password" required autocomplete="current-password" />
        </div>

        <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
        <p class="register-link">
          ¿No tienes cuenta? <router-link to="/register">Regístrate aquí</router-link>
        </p>
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? 'VERIFICANDO...' : 'SUBMIT' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { useLogin } from '@/composables/useLogin'

const { username, password, errorMessage, isLoading, submitLogin } = useLogin()
</script>

<style scoped>
/* Fondo oscuro para que cubra toda la pantalla sin barras de scroll */

.register-link {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.85rem;
  color: #aaaaaa;
}
.register-link a {
  color: #0096ff;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s;
}
.register-link a:hover {
  color: #1aa3ff;
  text-decoration: underline;
}
.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed; /* Se ancla a la ventana del navegador */
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: #0d0d0d;
  padding: 1rem; /* Evita que la caja toque los bordes del celular */
  box-sizing: border-box;
  z-index: 9999; /* Asegura que esté por encima de todo */
}

/* El contenedor con el resplandor azul */
.glow-box {
  background-color: #111111;
  padding: 3rem 2.5rem;
  border-radius: 20px;
  width: 100%;
  max-width: 380px;
  box-shadow: 0 0 15px rgba(0, 150, 255, 0.4),
              0 0 30px rgba(0, 150, 255, 0.2),
              inset 0 0 10px rgba(0, 150, 255, 0.1);
  border: 1px solid rgba(0, 150, 255, 0.3);
  box-sizing: border-box; /* Mantiene el padding dentro del ancho total */
}

h2 {
  text-align: center;
  color: #ffffff;
  margin-bottom: 2.5rem;
  font-family: sans-serif;
  font-size: 1.8rem;
  font-weight: 600;
  letter-spacing: 1px;
}

.input-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.8rem;
}

label {
  color: #cccccc;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  font-family: sans-serif;
}

/* Estilo minimalista para los inputs */
input {
  background: transparent;
  border: none;
  border-bottom: 2px solid #444;
  color: #ffffff;
  font-size: 1rem;
  padding: 0.5rem 0;
  outline: none;
  transition: border-bottom-color 0.3s;
}

input:focus {
  border-bottom-color: #0096ff;
}

.error-msg {
  color: #ff4d4d;
  font-size: 0.85rem;
  text-align: center;
  margin-bottom: 1rem;
}

/* Botón estilo píldora con resplandor */
button {
  background-color: #0096ff;
  color: #ffffff;
  border: none;
  border-radius: 30px;
  padding: 0.9rem;
  font-size: 1rem;
  font-weight: bold;
  letter-spacing: 2px;
  cursor: pointer;
  width: 100%;
  margin-top: 1rem;
  box-shadow: 0 0 15px rgba(0, 150, 255, 0.5);
  transition: transform 0.2s, box-shadow 0.2s, background-color 0.2s;
}

button:hover:not(:disabled) {
  background-color: #1aa3ff;
  box-shadow: 0 0 25px rgba(0, 150, 255, 0.8);
  transform: translateY(-2px);
}

button:disabled {
  background-color: #333333;
  color: #777777;
  box-shadow: none;
  cursor: not-allowed;
}

/* --- Ajustes Responsivos para Celulares --- */
@media (max-width: 480px) {
  .glow-box {
    padding: 2rem 1.5rem; /* Reducimos espacios internos */
    border-radius: 15px;
  }

  h2 {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .input-group {
    margin-bottom: 1.5rem;
  }

  input {
    font-size: 0.95rem;
  }

  button {
    padding: 0.8rem;
    font-size: 0.95rem;
  }
}
</style>