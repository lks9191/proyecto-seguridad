<template>
  <div class="app-container">
    <router-view />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
// Más adelante, si quieres un menú de navegación global (Navbar),
// este será el lugar perfecto para ponerlo.
</script>

<style>
/* Aquí puedes poner estilos muy generales que afecten a toda la app */
.app-container {
  font-family: Arial, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}
</style>