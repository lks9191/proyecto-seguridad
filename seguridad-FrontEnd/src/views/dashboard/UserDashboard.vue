<template>
  <div class="dashboard-wrapper">
    <div class="user-dashboard glow-box">
      <header class="dashboard-header">
        <h2>Panel de Usuario (Perfil Privado)</h2>
        <button @click="handleLogout" class="logout-btn">CERRAR SESIÓN</button>
      </header>

      <div v-if="isLoading" class="loading">Cargando tu información...</div>

      <div v-else class="content-grid">
        <section class="card profile-card">
          <h3>Mis Datos Personales</h3>
          <p class="subtitle">Solo tú tienes acceso a esta información (Confidencialidad).</p>
          <div v-if="profile" class="profile-details">
            <p><strong>Nombre:</strong> {{ profile.fullName }}</p>
            <p><strong>Usuario:</strong> {{ profile.username }}</p>
            <p><strong>Email:</strong> {{ profile.email }}</p>
            <p><strong>Ubicación:</strong> {{ profile.location }}</p>
            <p><strong>Carrera:</strong> {{ profile.career }}</p>
            <p><strong>Estado:</strong> <span class="badge active">{{ profile.status }}</span></p>
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
  </div>
</template>

<script setup>
import { useUser } from '@/composables/useUser'

const { profile, publicData, isLoading, handleLogout } = useUser()
</script>

<style scoped>
/* Contenedor principal oscuro forzado a ocupar toda la pantalla */
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

/* Caja principal con resplandor azul */
.glow-box {
  background-color: #111111;
  padding: 2rem 2.5rem;
  border-radius: 20px;
  max-width: 900px;
  margin: 0 auto;
  box-shadow: 0 0 15px rgba(0, 150, 255, 0.2),
              inset 0 0 10px rgba(0, 150, 255, 0.05);
  border: 1px solid rgba(0, 150, 255, 0.2);
  box-sizing: border-box;
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
  margin: 0;
  font-size: 1.5rem;
  color: #0096ff;
  letter-spacing: 1px;
}

h3 {
  color: #ffffff;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.subtitle {
  color: #aaaaaa;
  font-size: 0.85rem;
  margin-bottom: 1.5rem;
}

/* Botón de Logout - Estilo Neón Rojo */
.logout-btn {
  background-color: transparent;
  color: #ff4d4d;
  border: 1px solid #ff4d4d;
  border-radius: 30px;
  padding: 0.5rem 1.2rem;
  font-size: 0.85rem;
  font-weight: bold;
  letter-spacing: 1px;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(255, 77, 77, 0.2);
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background-color: #ff4d4d;
  color: #ffffff;
  box-shadow: 0 0 15px rgba(255, 77, 77, 0.6);
}

/* Grid para las tarjetas */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

/* Estilo de Tarjetas Oscuras */
.card {
  background-color: #1a1a1a;
  border: 1px solid #333;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.profile-details p {
  margin: 0.8rem 0;
  color: #cccccc;
  font-size: 0.95rem;
}

/* Resaltar las etiquetas en azul neón */
strong {
  color: #0096ff;
  font-weight: 600;
}

/* Badge de Estado - Neón Verde */
.badge.active {
  background-color: rgba(40, 167, 69, 0.15);
  color: #28a745;
  border: 1px solid #28a745;
  padding: 4px 10px;
  border-radius: 12px;
  font-weight: bold;
  font-size: 0.85em;
  box-shadow: 0 0 8px rgba(40, 167, 69, 0.3);
  display: inline-block;
  margin-left: 5px;
}

.public-list {
  padding-left: 1.2rem;
  color: #cccccc;
}

.public-list li {
  margin-bottom: 1rem;
  line-height: 1.4;
  font-size: 0.95rem;
}

.loading {
  text-align: center;
  color: #0096ff;
  font-weight: bold;
  padding: 2rem;
}

/* --- Ajustes Responsivos --- */
@media (max-width: 768px) {
  /* En tablets o pantallas más pequeñas, las tarjetas se apilan una debajo de la otra */
  .content-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}

@media (max-width: 600px) {
  .glow-box {
    padding: 1.5rem;
  }
  
  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>