<template>
  <div class="row">
    <div class="col-auto">
      <label for="inputPassword6" class="col-form-label">Search:</label>
    </div>
    <div class="col-auto">
      <input
        class="form-control"
        @keyup="tbl.loadData({ search: $event.target.value })"
        :value="tbl.searchString"
      />
    </div>
  </div>
</template>

<script setup>
import { tableHelperStore } from '@/stores/jurTableHelper'

const props = defineProps({ uid: { type: Number } })
// console.log('search=', props.uid)
const tbl = tableHelperStore(props.uid)()
</script>
