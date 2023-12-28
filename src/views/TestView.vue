<template>
  <div>
    <input v-model="vvv.ky" />
    {{ vvv.ky }}
    <hr />
    <TestCompA v-model:zzz="vvv" @reload="reload"/>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TestCompA from '@/components/TestCompA.vue'

const vvv = ref({ ky: 'aaa' })

const reload = (obj) => {
  console.log("reload", obj)
}
</script>
