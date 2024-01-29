<template>
  <div class="row g-3 align-items-center">
    <div class="col-auto">Show</div>
    <div class="col-auto">
      <select
        class="form-select form-select-sm"
        @change="tbl.loadData({ pageSize: $event.target.value })"
      >
        <option v-for="i in defSizes" :value="i" :key="i" :selected="i === tbl.pageSize">
          {{ i }}
        </option>
      </select>
    </div>
    <div class="col-auto">entries</div>
  </div>
</template>

<script setup>
import { tableHelperStore } from '@/stores/jurTableHelper'

const props = defineProps({
  uid: {
    type: Number
  }
})

// console.log('pageSize=', props.uid)
const tbl = tableHelperStore(props.uid)()

const defSizes = [1, 2, 3, 50, 100]
</script>
