<template>
  <div>CompA: <input :value="zzz.ky" @input="emitValue" /></div>
</template>

<script setup>
const props = defineProps(['zzz'])
const emit = defineEmits(['reload'])

function emitValue(e) {
  let value = e.target.value
  //local_zzz_val.ky = value
  props.zzz.ky = value
  emit('reload', props.zzz)
}
</script>
