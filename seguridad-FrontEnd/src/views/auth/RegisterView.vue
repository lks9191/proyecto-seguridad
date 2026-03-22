<template>
  <div class="login-wrapper">
    <div class="glow-box">
      <h2>Registro</h2>
      <form @submit.prevent="submitRegister">
        
        <div class="input-group">
          <label for="username">Username</label>
          <input id="username" v-model="username" type="text" required autocomplete="username" />
        </div>

        <div class="input-group">
          <label for="email">Email</label>
          <input id="email" v-model="email" type="email" required autocomplete="email" />
        </div>
        
        <div class="input-group">
          <label for="password">Password</label>
          <input id="password" v-model="password" type="password" required autocomplete="new-password" />
        </div>

        <div class="input-group">
          <label for="confirmPassword">Confirm Password</label>
          <input id="confirmPassword" v-model="confirmPassword" type="password" required autocomplete="new-password" />
        </div>

        <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
        
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? 'CREANDO...' : 'REGISTRARSE' }}
        </button>

        <p class="login-link">
          ¿Ya tienes cuenta? <router-link to="/login">Inicia sesión</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { useRegister } from '@/composables/useRegister'

const { 
  username, 
  email, 
  password, 
  confirmPassword, 
  errorMessage, 
  isLoading, 
  submitRegister 
} = useRegister()
</script>

<style scoped>
/* Exactamente el mismo estilo de LoginView para mantener consistencia */
.login-wrapper { display: flex; justify-content: center; align-items: center; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: #0d0d0d; padding: 1rem; box-sizing: border-box; z-index: 9999; overflow-y: auto; }
.glow-box { background-color: #111111; padding: 2.5rem 2.5rem; border-radius: 20px; width: 100%; max-width: 400px; box-shadow: 0 0 15px rgba(0, 150, 255, 0.4), 0 0 30px rgba(0, 150, 255, 0.2), inset 0 0 10px rgba(0, 150, 255, 0.1); border: 1px solid rgba(0, 150, 255, 0.3); box-sizing: border-box; margin: auto; }
h2 { text-align: center; color: #ffffff; margin-bottom: 2rem; font-family: sans-serif; font-size: 1.8rem; font-weight: 600; letter-spacing: 1px; }
.input-group { display: flex; flex-direction: column; margin-bottom: 1.2rem; }
label { color: #cccccc; font-size: 0.85rem; margin-bottom: 0.5rem; font-family: sans-serif; }
input { background: transparent; border: none; border-bottom: 2px solid #444; color: #ffffff; font-size: 1rem; padding: 0.5rem 0; outline: none; transition: border-bottom-color 0.3s; }
input:focus { border-bottom-color: #0096ff; }
.error-msg { color: #ff4d4d; font-size: 0.85rem; text-align: center; margin-bottom: 1rem; }
button { background-color: #0096ff; color: #ffffff; border: none; border-radius: 30px; padding: 0.9rem; font-size: 1rem; font-weight: bold; letter-spacing: 2px; cursor: pointer; width: 100%; margin-top: 0.5rem; box-shadow: 0 0 15px rgba(0, 150, 255, 0.5); transition: transform 0.2s, box-shadow 0.2s, background-color 0.2s; }
button:hover:not(:disabled) { background-color: #1aa3ff; box-shadow: 0 0 25px rgba(0, 150, 255, 0.8); transform: translateY(-2px); }
button:disabled { background-color: #333333; color: #777777; box-shadow: none; cursor: not-allowed; }

.login-link { text-align: center; margin-top: 1.5rem; font-size: 0.85rem; color: #aaaaaa; }
.login-link a { color: #0096ff; text-decoration: none; font-weight: bold; transition: color 0.3s; }
.login-link a:hover { color: #1aa3ff; text-decoration: underline; }

@media (max-width: 480px) {
  .glow-box { padding: 1.5rem; border-radius: 15px; }
  h2 { font-size: 1.5rem; margin-bottom: 1.2rem; }
  .input-group { margin-bottom: 1.2rem; }
  input { font-size: 0.95rem; }
}
</style>