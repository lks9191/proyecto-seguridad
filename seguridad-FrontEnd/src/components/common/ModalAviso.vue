<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-content notice-modal" :class="type">
      <div class="modal-header">
        <span class="modal-icon">{{ icon }}</span>
        <h3>{{ title }}</h3>
      </div>
      <div class="modal-body">
        <p>{{ message }}</p>
      </div>
      <div class="modal-footer">
        <button @click="$emit('close')" class="gov-btn-primary" :class="type">{{ buttonText }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  show: Boolean,
  title: {
    type: String,
    default: 'Aviso'
  },
  message: String,
  buttonText: {
    type: String,
    default: 'Entendido'
  },
  type: {
    type: String,
    default: 'info' // success, error, info
  }
})

defineEmits(['close'])

const icon = computed(() => {
  switch (props.type) {
    case 'success': return '✅'
    case 'error': return '❌'
    default: return 'ℹ️'
  }
})
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

.modal-content.success { border-top-color: #38a169; }
.modal-content.error { border-top-color: #c53030; }
.modal-content.info { border-top-color: #3182ce; }

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
}

.gov-btn-primary {
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
  background-color: #0056b3;
}

.gov-btn-primary.success { background-color: #38a169; }
.gov-btn-primary.error { background-color: #c53030; }
.gov-btn-primary.info { background-color: #3182ce; }

.gov-btn-primary:hover {
  filter: brightness(90%);
}
</style>
