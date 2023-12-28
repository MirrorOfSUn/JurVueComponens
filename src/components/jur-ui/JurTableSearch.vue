<template>
  <div class="row">
    <div class="col-auto">
      <label for="inputPassword6" class="col-form-label">Search:</label>
    </div>
    <div class="col-auto">
      <input
        class="form-control"
        @keyup="$emit('reload', { search: $event.target.value })"
        :value="search"
      />
    </div>
  </div>
</template>

<script setup>
defineEmits(['reload'])
defineProps(['search'])
</script>
