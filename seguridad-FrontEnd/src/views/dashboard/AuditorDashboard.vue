<template>
  <div class="dashboard-wrapper">
    <div class="auditor-dashboard glow-box">
      <header class="dashboard-header">
        <h2>Panel de Auditoría (Solo Lectura)</h2>
        <button @click="handleLogout" class="logout-btn">CERRAR SESIÓN</button>
      </header>

      <div class="info-banner">
        <strong>Principio de Mínimo Privilegio:</strong> Este rol únicamente tiene permisos para consultar los registros de seguridad. Garantizando la integridad, los logs no pueden ser modificados.
      </div>

      <div v-if="isLoading" class="loading">Cargando registros de auditoría...</div>

      <div v-else class="table-container">
        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>ID Log</th>
                <th>Fecha y Hora</th>
                <th>Usuario</th>
                <th>Evento</th>
                <th>Dirección IP</th>
                <th>Detalle</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in logs" :key="log.id">
                <td>{{ log.id }}</td>
                <td>{{ log.date }}</td>
                <td class="highlight-user">{{ log.user }}</td>
                <td>
                  <span :class="['event-badge', getEventClass(log.event)]">
                    {{ log.event }}
                  </span>
                </td>
                <td class="ip-text">{{ log.ip }}</td>
                <td>{{ log.detail }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuditor } from '@/composables/useAuditor'

const { logs, isLoading, handleLogout } = useAuditor()

// Función visual sencilla para darle color a las etiquetas de eventos
const getEventClass = (event) => {
  if (event.includes('SUCCESS')) return 'success'
  if (event.includes('FAILED') || event.includes('UNAUTHORIZED')) return 'danger'
  if (event.includes('CHANGED')) return 'warning'
  return 'default'
}
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

/* Caja principal con resplandor azul, un poco más ancha para los logs */
.glow-box {
  background-color: #111111;
  padding: 2rem 2.5rem;
  border-radius: 20px;
  max-width: 1050px;
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
  margin-bottom: 1.5rem;
}

h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #0096ff;
  letter-spacing: 1px;
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

/* Banner Informativo Estilo Neón */
.info-banner {
  background-color: rgba(0, 150, 255, 0.05);
  color: #cccccc;
  padding: 1rem 1.5rem;
  border-left: 4px solid #0096ff;
  margin-bottom: 2rem;
  border-radius: 4px;
  font-size: 0.95rem;
  line-height: 1.5;
}

.info-banner strong {
  color: #0096ff;
}

.loading {
  text-align: center;
  color: #0096ff;
  font-weight: bold;
  padding: 2rem;
}

/* --- Estilos de la Tabla Oscura --- */
.table-responsive {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9em;
  background-color: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
}

th, td {
  border-bottom: 1px solid #333;
  padding: 12px 15px;
  text-align: left;
}

th {
  background-color: #222222;
  color: #0096ff;
  font-weight: bold;
  letter-spacing: 1px;
}

tr:hover {
  background-color: #252525;
}

.highlight-user {
  color: #ffffff;
  font-weight: bold;
}

.ip-text {
  color: #aaaaaa;
  font-family: monospace; /* Estilo terminal para IPs */
  font-size: 1em;
}

/* --- Badges de Eventos (Neón) --- */
.event-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-weight: bold;
  font-size: 0.8em;
  display: inline-block;
  letter-spacing: 0.5px;
}

.success {
  background-color: rgba(40, 167, 69, 0.15);
  color: #28a745;
  border: 1px solid #28a745;
}

.danger {
  background-color: rgba(255, 77, 77, 0.15);
  color: #ff4d4d;
  border: 1px solid #ff4d4d;
}

.warning {
  background-color: rgba(255, 165, 0, 0.15);
  color: #ffa500;
  border: 1px solid #ffa500;
}

.default {
  background-color: rgba(255, 255, 255, 0.1);
  color: #cccccc;
  border: 1px solid #666666;
}

/* --- Ajustes Responsivos --- */
@media (max-width: 600px) {
  .glow-box {
    padding: 1.5rem;
  }
  
  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  th, td {
    padding: 10px;
    font-size: 0.85rem;
  }
  
  .info-banner {
    font-size: 0.85rem;
    padding: 1rem;
  }
}
</style>