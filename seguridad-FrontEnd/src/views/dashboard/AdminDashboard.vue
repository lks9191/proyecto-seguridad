<template>
  <div class="dashboard-wrapper">
    <div class="admin-dashboard glow-box">
      <header class="dashboard-header">
        <h2>Panel de Administración (RBAC)</h2>
        <button @click="handleLogout" class="logout-btn">CERRAR SESIÓN</button>
      </header>

      <div v-if="message" class="alert-success">
        {{ message }}
      </div>

      <div v-if="isLoading" class="loading">
        Cargando usuarios...
      </div>

      <div v-else class="table-container">
        <h3>Gestión de Usuarios</h3>
        <p class="subtitle">Aplica el principio de mínimo privilegio asignando los roles correctos.</p>
        
        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Usuario</th>
                <th>Email</th>
                <th>Rol Actual</th>
                <th>Acción (Asignar Rol)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>
                  <span :class="['role-badge', user.role.toLowerCase()]">
                    {{ user.role }}
                  </span>
                </td>
                <td>
                  <select 
                    :value="user.role" 
                    @change="changeUserRole(user.id, $event.target.value)"
                    class="neon-select"
                  >
                    <option value="USER">USER</option>
                    <option value="ADMIN">ADMIN</option>
                    <option value="AUDITOR">AUDITOR</option>
                  </select>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAdmin } from '@/composables/useAdmin'

const { users, isLoading, message, changeUserRole, handleLogout } = useAdmin()
</script>

<style scoped>
/* Contenedor principal oscuro con scroll permitido */
.dashboard-wrapper {
  position: absolute; /* Se escapa de los márgenes por defecto de Vue */
  top: 0;
  left: 0;
  width: 100vw; /* 100% del ancho de la ventana */
  min-height: 100vh; /* Al menos 100% del alto */
  background-color: #0d0d0d;
  padding: 2rem 1rem;
  box-sizing: border-box;
  font-family: sans-serif;
  color: #ffffff;
  overflow-y: auto; /* Asegura que se pueda hacer scroll si la tabla crece */
}

/* Caja principal con resplandor, más ancha para la tabla */
.glow-box {
  background-color: #111111;
  padding: 2rem 2.5rem;
  border-radius: 20px;
  max-width: 900px;
  margin: 0 auto;
  box-shadow: 0 0 15px rgba(0, 150, 255, 0.2),
              inset 0 0 10px rgba(0, 150, 255, 0.05);
  border: 1px solid rgba(0, 150, 255, 0.2);
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
  color: #0096ff; /* Azul neón para títulos */
  letter-spacing: 1px;
}

h3 {
  color: #ffffff;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #aaaaaa;
  font-size: 0.9rem;
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

/* Alerta de éxito al cambiar rol */
.alert-success {
  background-color: rgba(0, 150, 255, 0.1);
  border-left: 4px solid #0096ff;
  color: #0096ff;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
  font-weight: bold;
}

/* --- Estilos de la Tabla Oscura --- */
.table-responsive {
  overflow-x: auto; /* Permite scroll horizontal en celulares */
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  background-color: #1a1a1a;
  border-radius: 8px;
  overflow: hidden; /* Para que los bordes redondeados apliquen al thead */
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

/* Selectores desplegables estilo oscuro */
.neon-select {
  background-color: #0d0d0d;
  color: #ffffff;
  border: 1px solid #444;
  padding: 0.4rem;
  border-radius: 4px;
  outline: none;
  cursor: pointer;
}

.neon-select:focus {
  border-color: #0096ff;
  box-shadow: 0 0 5px rgba(0, 150, 255, 0.5);
}

/* --- Badges de Roles --- */
.role-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.8em;
  font-weight: bold;
  letter-spacing: 0.5px;
  display: inline-block;
}

/* Colores oscuros/neón para los badges */
.admin { 
  background-color: rgba(0, 150, 255, 0.15); 
  color: #0096ff; 
  border: 1px solid #0096ff; 
}
.user { 
  background-color: rgba(255, 255, 255, 0.1); 
  color: #cccccc; 
  border: 1px solid #666666; 
}
.auditor { 
  background-color: rgba(255, 165, 0, 0.15); 
  color: #ffa500; 
  border: 1px solid #ffa500; 
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
    font-size: 0.9rem;
  }
}
</style>