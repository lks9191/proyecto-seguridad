<template>
  <section class="gov-card mt-2">
    <div class="card-header">
      <h3>Mis Trámites Electrónicos</h3>
      <button @click="$emit('open-new-tramite')" class="gov-btn-primary">INICIAR NUEVO TRÁMITE</button>
    </div>
    <p class="subtitle">Historial y seguimiento de sus solicitudes ciudadanas.</p>
    
    <div class="table-responsive">
      <table>
        <thead>
          <tr>
            <th>Nro. Trámite</th>
            <th>Tipo de Documento</th>
            <th>Fecha de Ingreso</th>
            <th>Estado Actual</th>
            <th>Acción</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tramite in tramites" :key="tramite.id">
            <td class="fw-bold">{{ tramite.id }}</td>
            <td>{{ tramite.tipo }}</td>
            <td>{{ tramite.fecha }}</td>
            <td>
              <span :class="['status-badge', tramite.estadoClass]">{{ tramite.estado }}</span>
            </td>
            <td>
              <button class="gov-btn-outline">VER DETALLE</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
defineProps({
  tramites: Array
})
defineEmits(['open-new-tramite'])
</script>

<style scoped>
/* Estilo de Tarjeta Gubernamental Blanca */
.gov-card { 
  background-color: #ffffff; 
  padding: 2rem; 
  border-radius: 8px; 
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
  border-top: 4px solid #0056b3; 
}

.mt-2 { 
  margin-top: 2rem; 
}

.card-header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  margin-bottom: 0.5rem; 
}

h3 { 
  margin: 0; 
  color: #2c3136; 
  font-size: 1.3rem;
  font-weight: 600;
}

.subtitle { 
  color: #718096; 
  font-size: 0.85rem; 
  margin-bottom: 1.5rem; 
  margin-top: 0;
}

/* Botón Principal */
.gov-btn-primary { 
  background-color: #0056b3; 
  color: #ffffff; 
  border: none; 
  padding: 0.6rem 1.2rem; 
  border-radius: 4px; 
  cursor: pointer; 
  font-size: 0.85rem; 
  font-weight: 600; 
  transition: background-color 0.2s; 
}

.gov-btn-primary:hover { 
  background-color: #004494; 
}

/* --- TABLA LIMPIA Y CORPORATIVA --- */
.table-responsive { 
  overflow-x: auto; 
}

table { 
  width: 100%; 
  border-collapse: collapse; 
  margin-top: 0.5rem; 
  background-color: #ffffff; 
  border: 1px solid #e2e8f0;
  border-radius: 4px; 
}

th, td { 
  border-bottom: 1px solid #e2e8f0; 
  padding: 12px 15px; 
  text-align: left; 
  font-size: 0.9rem; 
  color: #4a5568;
}

th { 
  background-color: #edf2f7; 
  color: #2c3136; 
  font-weight: 600; 
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.5px;
}

tr:hover { 
  background-color: #f8fafc; 
}

.fw-bold {
  font-weight: 600;
  color: #2c3136;
}

/* Botón de acción en la tabla */
.gov-btn-outline { 
  background: transparent; 
  color: #0056b3; 
  border: 1px solid #cbd5e0; 
  padding: 4px 10px; 
  border-radius: 4px; 
  cursor: pointer; 
  font-size: 0.75rem; 
  font-weight: 600;
  transition: all 0.2s; 
}

.gov-btn-outline:hover { 
  background-color: #edf2f7;
  border-color: #0056b3; 
}

/* Badges de Estado (Colores pastel para GovTech) */
.status-badge { 
  padding: 4px 10px; 
  border-radius: 12px; 
  font-weight: 600; 
  font-size: 0.75em; 
  display: inline-block; 
  letter-spacing: 0.5px; 
}

.success { 
  background-color: #def7ec; 
  color: #03543f; 
  border: 1px solid #84e1bc; 
}

.danger { 
  background-color: #fde8e8; 
  color: #9b1c1c; 
  border: 1px solid #f8b4b4; 
}

.warning { 
  background-color: #fef3c7; 
  color: #92400e; 
  border: 1px solid #fde68a; 
}

/* Responsive */
@media (max-width: 600px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style>