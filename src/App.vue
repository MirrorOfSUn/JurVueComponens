<script setup>
import { RouterView } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
// import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <NavBar />
  <div class="container">
    <RouterView />
  </div>
</template>

<style scoped>
.container {
  margin-top: 15px !important;
}
</style>
