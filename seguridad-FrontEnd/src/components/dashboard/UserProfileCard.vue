<template>
  <section class="gov-card profile-card">
    <div class="card-header">
      <h3>Mis Datos Personales</h3>
      <button @click="$emit('open-edit')" class="gov-btn-small">Editar Perfil</button>
    </div>
    <p class="subtitle">Solo usted tiene acceso a esta información (Confidencialidad).</p>

    <div v-if="profile" class="profile-details">
      <p><strong>Nombres:</strong> {{ profile.names }}</p>
      <p><strong>Apellidos:</strong> {{ profile.paternal_surname }} {{ profile.maternal_surname || '' }}</p>
      <p><strong>Carnet de Identidad (CI):</strong> {{ profile.carnet }}</p>
      <p><strong>Correo Electrónico:</strong> {{ profile.email }}</p>
      <p><strong>Roles asignados:</strong>
        <span v-for="r in profile.roles" :key="r" class="role-badge">{{ r }}</span>
      </p>

      <div class="two-fa-row">
        <p><strong>Seguridad 2FA:</strong>
          <span :class="['status-badge', profile.is_2fa_enabled ? 'success' : 'danger']">
            {{ profile.is_2fa_enabled ? 'Activado (Email)' : 'Desactivado' }}
          </span>
        </p>
        <button v-if="!profile.is_2fa_enabled" @click="$emit('setup-2fa')" class="gov-btn-outline-small">
          Activar 2FA
        </button>
        <button v-else @click="$emit('disable-2fa')" class="disable-2fa-link">
          Desactivar 2FA
        </button>
      </div>

      <p><strong>Miembro desde:</strong> {{ formatDate(profile.created_at) }}</p>
    </div>
  </section>
</template>

<script setup>
defineProps({
  profile: Object
})

defineEmits(['open-edit', 'setup-2fa', 'disable-2fa'])

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString()
}
</script>

<style scoped>
/* Estilo de Tarjeta Gubernamental Blanca */
.gov-card {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
  border-top: 4px solid #0056b3;
  height: 100%;
  box-sizing: border-box;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  border-bottom: 1px solid #edf2f7;
  padding-bottom: 1rem;
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
  margin-top: 0.5rem;
  margin-bottom: 1.5rem;
}

.gov-btn-small {
  background: #0056b3;
  color: white;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 600;
  transition: background 0.2s;
}

.gov-btn-small:hover {
  background: #004494;
}

.profile-details p {
  margin: 1rem 0;
  color: #4a5568;
  font-size: 0.95rem;
}

strong {
  color: #0056b3;
  font-weight: 600;
}

/* Badges de Roles */
.role-badge {
  background: #e6f7ff;
  color: #0056b3;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  margin-left: 5px;
  border: 1px solid #91d5ff;
}

/* Caja especial para el 2FA */
.two-fa-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin: 1.5rem 0;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

.two-fa-row p {
  margin: 0;
}

/* Badges de Estado (Pastel) */
.status-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.8em;
  display: inline-block;
  letter-spacing: 0.5px;
  margin-left: 5px;
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

.gov-btn-outline-small {
  background: transparent;
  color: #0056b3;
  border: 1px solid #0056b3;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 600;
  transition: all 0.2s;
}

.gov-btn-outline-small:hover {
  background: #0056b3;
  color: #ffffff;
}

.disable-2fa-link {
  background: transparent;
  border: none;
  color: #c53030;
  text-decoration: underline;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0;
}

.disable-2fa-link:hover {
  color: #9b1c1c;
}

@media (max-width: 480px) {
  .two-fa-row {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>