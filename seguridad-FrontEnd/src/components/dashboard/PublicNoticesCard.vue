<template>
  <section class="gov-card public-card">
    <div class="card-header-titles">
      <h3>Información Pública</h3>
      <p class="subtitle">Avisos generales del Estado.</p>
    </div>
    
    <ul class="public-list">
      <li v-for="item in publicData" :key="item.id">
        <strong>{{ item.title }}:</strong> {{ item.content }}
      </li>
    </ul>
  </section>
</template>

<script setup>
defineProps({
  publicData: Array
})
</script>

<style scoped>
/* Estilo de Tarjeta Gubernamental Blanca */
.gov-card { 
  background-color: #ffffff; 
  padding: 2rem; 
  border-radius: 8px; 
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
  border-top: 4px solid #0056b3; /* Detalle corporativo institucional */
  height: 100%; /* Para que iguale la altura de la otra tarjeta si se usa grid */
  box-sizing: border-box;
}

.card-header-titles {
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #edf2f7;
  padding-bottom: 1rem;
}

h3 { 
  margin: 0; 
  color: #2c3136; /* Gris carbón en lugar de blanco */
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.3rem; 
}

.subtitle { 
  color: #718096; /* Gris texto secundario */
  font-size: 0.85rem; 
  margin: 0; 
}

.public-list { 
  padding-left: 1.2rem; 
  color: #4a5568; /* Texto principal oscuro y legible */
  margin: 0;
}

.public-list li { 
  margin-bottom: 1rem; 
  font-size: 0.95rem; 
  line-height: 1.5;
}

/* Las etiquetas resaltadas ahora usan el azul institucional */
strong { 
  color: #0056b3; 
  font-weight: 600;
}
</style>