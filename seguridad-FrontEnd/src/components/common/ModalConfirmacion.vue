<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-content confirm-modal">
      <div class="modal-header">
        <span class="modal-icon">❓</span>
        <h3>{{ title }}</h3>
      </div>
      <div class="modal-body">
        <p>{{ message }}</p>
      </div>
      <div class="modal-footer">
        <button @click="$emit('cancel')" class="gov-btn-secondary">{{ cancelText }}</button>
        <button @click="$emit('confirm')" class="gov-btn-primary danger">{{ confirmText }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: Boolean,
  title: {
    type: String,
    default: 'Confirmación'
  },
  message: {
    type: String,
    default: '¿Está seguro de realizar esta acción?'
  },
  confirmText: {
    type: String,
    default: 'Confirmar'
  },
  cancelText: {
    type: String,
    default: 'Cancelar'
  }
})

defineEmits(['confirm', 'cancel'])
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(2px);
}

.modal-content {
  background: white;
  padding: 2.5rem;
  width: 90%;
  max-width: 450px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  border-top: 5px solid #0056b3;
}

.modal-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.modal-icon {
  font-size: 2rem;
}

.modal-header h3 {
  margin: 0;
  color: #2c3136;
  font-size: 1.4rem;
}

.modal-body p {
  color: #4a5568;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.gov-btn-primary.danger {
  background-color: #c53030;
}

.gov-btn-primary.danger:hover {
  background-color: #9b2c2c;
}

.gov-btn-secondary {
  background-color: #edf2f7;
  color: #4a5568;
  border: 1px solid #cbd5e0;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.gov-btn-secondary:hover {
  background-color: #e2e8f0;
}

.gov-btn-primary {
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}
</style>
