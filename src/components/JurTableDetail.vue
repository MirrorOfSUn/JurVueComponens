<template>
  <div class="container-flex border border-primary bg-primary bg-opacity-10">
    <div class="row">
      <div class="col">FirstName</div>
      <div class="col">{{ res.FirstName }}</div>
    </div>
    <div class="row">
      <div class="col">LastName</div>
      <div class="col">{{ res.LastName }}</div>
    </div>
    <div class="row">
      <div class="col">MiddleName</div>
      <div class="col">{{ res.MiddleName }}</div>
    </div>
    <div class="row">
      <div class="col">FullName</div>
      <div class="col">{{ res.FullName }}</div>
    </div>
    <div class="row">
      <div class="col">Phone1</div>
      <div class="col">{{ res.Phone1 }}</div>
    </div>
    <div class="row">
      <div class="col">Phone2</div>
      <div class="col">{{ res.Phone2 }}</div>
    </div>
    <div class="row">
      <div class="col">Email1</div>
      <div class="col">{{ res.Email1 }}</div>
    </div>
    <div class="row">
      <div class="col">Email2</div>
      <div class="col">{{ res.Email2 }}</div>
    </div>
    <div class="row">
      <div class="col">Address</div>
      <div class="col">{{ res.Address }}</div>
    </div>
    <div class="row">
      <div class="col">Is Active</div>
      <div class="col">{{ res.is_active }}</div>
    </div>
    <div class="row">
      <div class="col">ID</div>
      <div class="col">{{ res.is_active }}</div>
    </div>
  </div>
</template>
<script setup>
import axios from 'axios'
import { ref } from 'vue'

const props = defineProps(['api', 'pkey'])
const res = ref({})
console.log(props)

// axios.get(props.value.api + '/' + props.value.id).then((response) => {
//   res.value = response
// })
</script>
