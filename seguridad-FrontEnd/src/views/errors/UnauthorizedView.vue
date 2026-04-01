<template>
  <div class="unauthorized-wrapper">
    <div class="glow-box error-box">
      <div class="icon-block">
        <span class="lock-icon">🚫</span>
      </div>

      <h1>403 - ACCESO DENEGADO</h1>
      <h2>Lo sentimos, no tienes permisos suficientes.</h2>

      <p class="description">
        Has intentado acceder a una ruta protegida. El <strong>Principio de Mínimo Privilegio</strong> y el control de
        acceso basado en roles (<strong>RBAC</strong>) de este sistema han bloqueado tu solicitud.
      </p>

      <div class="details-box">
        <p><strong>Carnet de Identidad (CI):</strong> {{ authStore.carnet || 'Sesión no iniciada' }}</p>
        <p><strong>Tu Rol asignado:</strong> <span class="role-badge">{{ authStore.role || 'Ninguno' }}</span></p>
      </div>

      <div class="action-block">
        <button @click="goBackToSafety" class="home-btn">
          VOLVER A MI DASHBOARD SEGURO
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// Lógica para redirigir al usuario según su rol actual (si está logueado)
const goBackToSafety = () => {
  if (!authStore.isAuthenticated) {
    router.push({ name: 'login' })
    return
  }

  // Si está logueado, lo mandamos a "su lugar seguro" según su rol
  switch (authStore.role) {
    case 'ADMIN':
      router.push({ name: 'admin-dashboard' })
      break
    case 'AUDITOR':
      router.push({ name: 'auditor-dashboard' })
      break
    case 'USER':
    default:
      router.push({ name: 'user-dashboard' })
      break
  }
}
</script>

<style scoped>
/* Contenedor principal oscuro que cubre toda la pantalla */
.unauthorized-wrapper {
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
  font-family: sans-serif;
}

/* Caja principal con resplandor ROJO de alerta */
.glow-box.error-box {
  background-color: #111111;
  padding: 3rem 2.5rem;
  border-radius: 20px;
  max-width: 500px;
  width: 100%;
  text-align: center;
  box-shadow: 0 0 15px rgba(220, 53, 69, 0.4),
    0 0 30px rgba(220, 53, 69, 0.2),
    inset 0 0 10px rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.3);
  box-sizing: border-box;
}

.icon-block {
  font-size: 4rem;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 15px rgba(220, 53, 69, 0.6);
}

h1 {
  color: #ff4d4d;
  /* Rojo neón */
  margin: 0;
  font-size: 1.8rem;
  letter-spacing: 1px;
}

h2 {
  color: #ffffff;
  margin-top: 0.5rem;
  font-size: 1.1rem;
  font-weight: normal;
}

.description {
  color: #aaaaaa;
  margin: 1.5rem 0;
  line-height: 1.5;
  font-size: 0.95rem;
}

/* Destacando texto de seguridad en rojo */
.description strong {
  color: #ff4d4d;
  font-weight: bold;
}

.details-box {
  background-color: #1a1a1a;
  border: 1px solid #333;
  padding: 1.2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  text-align: left;
  color: #cccccc;
}

.details-box p {
  margin: 0.5rem 0;
  font-size: 0.95rem;
}

.details-box strong {
  color: #0096ff;
  /* Etiquetas en azul */
}

.role-badge {
  background-color: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  border: 1px solid #666;
  padding: 3px 10px;
  border-radius: 12px;
  font-weight: bold;
  font-size: 0.85em;
  margin-left: 5px;
  letter-spacing: 1px;
}

/* Botón estilo píldora con resplandor AZUL (Camino seguro) */
.home-btn {
  background-color: #0096ff;
  color: #ffffff;
  border: none;
  border-radius: 30px;
  padding: 1rem 1.5rem;
  font-size: 0.95rem;
  font-weight: bold;
  letter-spacing: 1px;
  cursor: pointer;
  width: 100%;
  box-shadow: 0 0 15px rgba(0, 150, 255, 0.5);
  transition: transform 0.2s, box-shadow 0.2s, background-color 0.2s;
}

.home-btn:hover {
  background-color: #1aa3ff;
  box-shadow: 0 0 25px rgba(0, 150, 255, 0.8);
  transform: translateY(-2px);
}

/* --- Ajustes Responsivos --- */
@media (max-width: 480px) {
  .glow-box.error-box {
    padding: 2rem 1.5rem;
  }

  h1 {
    font-size: 1.5rem;
  }

  .icon-block {
    font-size: 3rem;
  }
}
</style>