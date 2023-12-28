<template>
  <div class="about">
    <h1>This is an about page</h1>
    <img src="/static/img/example.jpg" />
    {{ aaa }}
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>

<script setup>
let aaa = ky()
</script>
