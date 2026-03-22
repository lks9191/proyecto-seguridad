<template>
  <div class="login-wrapper">
    <div class="glow-box">
      <h2>Autenticación 2FA</h2>
      <p class="subtitle">Hemos enviado un código a su correo electrónico institucional. Por favor, ingréselo a
        continuación.</p>

      <form @submit.prevent="verifyCode">
        <div class="input-group">
          <label for="totp">Código de 6 dígitos</label>
          <input id="totp" v-model="totpCode" type="text" maxlength="6" required placeholder="123456" class="code-input"
            autocomplete="off" />
        </div>

        <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>

        <button type="submit" :disabled="isLoading">
          {{ isLoading ? 'VERIFICANDO...' : 'ACCEDER AL SISTEMA' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { useTwoFactor } from '@/composables/useTwoFactor'

const { totpCode, errorMessage, isLoading, verifyCode } = useTwoFactor()
</script>

<style scoped>
/* Contenedor principal que cubre toda la pantalla */
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
  box-sizing: border-box;
}

h2 {
  text-align: center;
  color: #ffffff;
  margin-bottom: 0.5rem;
  font-family: sans-serif;
  font-size: 1.8rem;
  font-weight: 600;
  letter-spacing: 1px;
}

/* Estilo para el texto explicativo */
.subtitle {
  text-align: center;
  color: #aaaaaa;
  font-size: 0.9rem;
  margin-bottom: 2rem;
  line-height: 1.4;
  font-family: sans-serif;
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
  text-align: center;
  /* Centrado para el 2FA */
}

/* Input específico para códigos */
input.code-input {
  background: transparent;
  border: none;
  border-bottom: 2px solid #444;
  color: #ffffff;
  font-size: 1.5rem;
  /* Más grande para números */
  padding: 0.5rem 0;
  outline: none;
  transition: border-bottom-color 0.3s;
  text-align: center;
  /* Números al centro */
  letter-spacing: 5px;
  /* Separación entre números */
}

input.code-input:focus {
  border-bottom-color: #0096ff;
}

/* Ocultar el placeholder cuando hace foco para que no se vea raro con el letter-spacing */
input.code-input:focus::placeholder {
  color: transparent;
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
    padding: 2rem 1.5rem;
    border-radius: 15px;
  }

  h2 {
    font-size: 1.5rem;
  }

  .subtitle {
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
  }

  .input-group {
    margin-bottom: 1.5rem;
  }

  input.code-input {
    font-size: 1.3rem;
  }

  button {
    padding: 0.8rem;
    font-size: 0.95rem;
  }
}
</style>