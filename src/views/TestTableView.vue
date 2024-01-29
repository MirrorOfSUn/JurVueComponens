<template>
  <!-- <div class="container">
      <jur-table :datatable="users_db" :fields="fields" :page-size="2" v-model:search="searchString">
        <template #footer>Showing 1 to 10 of {{ data.total_records }} entries </template>
      </jur-table>
    </div> -->
  <hr />
  <div class="container">
    <jur-table1 :config="config">
      <!--template #footer>Showing 1 to 10 of {{ data.total_records }} entries </template-->
    </jur-table1>
  </div>
</template>

<script setup>
import JurTable1 from '../components/JurTable1.vue'

const config = {
  api: './api/users',
  fields: fields,
  isServerSide: true,
  pageSize: 1
}

// import { ref } from 'vue'
// import axios from 'axios'
// let searchString = ref('FN')

// const emit = defineEmits(['change', 'delete'])
// {"users":[{"FirstName":"FN1","LastName":"LN1","MiddleName":"","FullName":"AAAAAA","Phone1":"12345","Phone2":"","Email1":"","Email2":"","Address":"","is_active":true,"id":1},{"FirstName":"FN2","LastName":"LN2","MiddleName":"","FullName":"Full Name","Phone1":"67890","Phone2":"","Email1":"","Email2":"","Address":"","is_active":true,"id":2},{"FirstName":"FN3","LastName":"LN3","MiddleName":"","FullName":"FN3 LN3","Phone1":"12345","Phone2":"","Email1":"","Email2":"","Address":"","is_active":true,"id":3},{"FirstName":"FN4","LastName":"LN4","MiddleName":"","FullName":"FN4 LN4","Phone1":"67890","Phone2":"","Email1":"","Email2":"","Address":"","is_active":true,"id":4}],"total_records":4,"total_filtered_records":4,"total_pages":1,"current_page":0,"page_size":100}
// let users_db = ref([
//   {
//     FirstName: 'FN1',
//     LastName: 'LN1',
//     MiddleName: '',
//     FullName: 'AAAAAA',
//     Phone1: '12345',
//     Phone2: '',
//     Email1: '',
//     Email2: '',
//     Address: '',
//     is_active: true,
//     id: 1
//   },
//   {
//     FirstName: 'FN2',
//     LastName: 'LN1',
//     MiddleName: '',
//     FullName: 'AAAAAA',
//     Phone1: '12345',
//     Phone2: '',
//     Email1: '',
//     Email2: '',
//     Address: '',
//     is_active: true,
//     id: 2
//   },
//   {
//     FirstName: 'FN3',
//     LastName: 'LN1',
//     MiddleName: '',
//     FullName: 'AAAAAA',
//     Phone1: '12345',
//     Phone2: '',
//     Email1: '',
//     Email2: '',
//     Address: '',
//     is_active: true,
//     id: 3
//   },
//   {
//     FirstName: 'FN4',
//     LastName: 'LN1',
//     MiddleName: '',
//     FullName: 'AAAAAA',
//     Phone1: '12345',
//     Phone2: '',
//     Email1: '',
//     Email2: '',
//     Address: '',
//     is_active: true,
//     id: 4
//   },
//   {
//     FirstName: 'FN5',
//     LastName: 'LN1',
//     MiddleName: '',
//     FullName: 'AAAAAA',
//     Phone1: '12345',
//     Phone2: '',
//     Email1: '',
//     Email2: '',
//     Address: '',
//     is_active: true,
//     id: 5
//   }
// ])
const fields = [
  {
    name: 'FullName',
    label: 'Full Name',
    sortable: true,
    searchable: true,
    data: (rec) => {
      return rec.FirstName + '-' + rec.LastName
    }
  },
  { name: 'Phone1', label: 'Phone', sortable: true, search: true }
]
</script>
