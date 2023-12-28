<template>
  <div class="row g-3 align-items-center">
    <div class="col-auto">Show</div>
    <div class="col-auto">
      <select
        class="form-select form-select-sm"
        @change="$emit('reload', { pageSize: $event.target.value })"
      >
        <option v-for="i in defSizes" :value="i" :key="i" :selected="i === def">
          {{ i }}
        </option>
      </select>
    </div>
    <div class="col-auto">entries</div>
  </div>
</template>

<script setup>
defineProps({
  def: {
    type: Number,
    default: 1
  }
})
defineEmits(['reload'])

const defSizes = [1, 2, 3, 50, 100]
</script>
