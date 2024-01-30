<template>
  <div class="form-check">
    <input class="form-check-input" type="checkbox" @change="confFieldsUpd($event)" checked />
    <label class="form-check-label" for="conf_fields"> Add fields to config </label>
  </div>
  <div class="form-check">
    <input class="form-check-input" type="checkbox" @change="confBulkUpd($event)" checked />
    <label class="form-check-label" for="conf_bulk">Bulk </label>
  </div>
  <div class="form-check">
    <input class="form-check-input" type="checkbox" @change="confShowdetailsUpd($event)" checked />
    <label class="form-check-label" for="conf_bulk">Showdetails </label>
  </div>
  <div class="form-check">
    <input class="form-check-input" type="checkbox" @change="confFieldWidthUpd($event)" />
    <label class="form-check-label" for="conf_bulk">Field Width </label>
  </div>
  <div class="form-check">
    <input class="form-check-input" type="checkbox" @change="configServerSideUpd($event)" />
    <label class="form-check-label" for="conf_isServerSide">isServerSide </label>
  </div>
  <div>
    <h1>Table 1</h1>
    <JurTable :config="tblConf"><JurTableDetail pkey="ASD"></JurTableDetail></JurTable>
    <!-- <h1>Table 2</h1>
    <Jur1Table :config="tblConf1"></JurTable>
    <h1>Table 3</h1>
    <Jur1Table :config="tblConf2"></JurTable> -->
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
import { ref } from 'vue'
import JurTable from '@/components/JurTable.vue'
import JurTableDetail from '@/components/JurTableDetail.vue'

const users_db = [
  {
    FirstName: 'FN1',
    LastName: 'LN1',
    MiddleName: '',
    FullName: 'AAAAAA',
    Phone1: '12345',
    Phone2: '',
    Email1: '',
    Email2: '',
    Address: '',
    is_active: true,
    id: 1
  },
  {
    FirstName: 'FN2',
    LastName: 'LN1',
    MiddleName: '',
    FullName: 'AAAAAA',
    Phone1: '12346',
    Phone2: '',
    Email1: '',
    Email2: '',
    Address: '',
    is_active: true,
    id: 2
  },
  {
    FirstName: 'FN3',
    LastName: 'LN1',
    MiddleName: '',
    FullName: 'AAAAAA',
    Phone1: '12345',
    Phone2: '',
    Email1: '',
    Email2: '',
    Address: '',
    is_active: false,
    id: 3
  },
  {
    FirstName: 'FN4',
    LastName: 'LN1',
    MiddleName: '',
    FullName: 'AAAAAA',
    Phone1: '12345',
    Phone2: '',
    Email1: '',
    Email2: '',
    Address: '',
    is_active: true,
    id: 4
  },
  {
    FirstName: 'FN5',
    LastName: 'LN1',
    MiddleName: '',
    FullName: 'AAAAAA',
    Phone1: '12346',
    Phone2: '',
    Email1: '',
    Email2: '',
    Address: '',
    is_active: true,
    id: 8
  }
]
const fields = [
  {
    name: 'FullName',
    label: 'Full Name',
    sortable: true,
    searchable: true,
    type: 'string',
    hidden: false,
    data: (rec) => {
      return rec.FirstName + '-' + rec.LastName
    }
  },
  {
    name: 'Phone1',
    label: 'Phone',
    type: 'string',
    sortable: true,
    search: true,
    hidden: false
  }
]

// helper1.config({ datatable: users_db, fields: fields })
const tblConf = ref({
  colors: {
    even: 'table-light',
    odd: 'table-info',
    opened: 'table-primary'
  },
  fields: fields,
  datatable: users_db,
  bulk: true,
  showdetails: true,
  isServerSide: false,
  api: './api/users'
})
// const tblConf1 = { datatable: users_db }
// const tblConf2 = { fields: fields, datatable: users_db, bulk: true }

function confFieldsUpd(e) {
  if (e.target.checked) tblConf.value.fields = fields
  else tblConf.value.fields = []
}

function confBulkUpd(e) {
  tblConf.value.bulk = e.target.checked
}

function confShowdetailsUpd(e) {
  tblConf.value.showdetails = e.target.checked
}

function configServerSideUpd(e) {
  tblConf.value.isServerSide = e.target.checked
  if (tblConf.value.isServerSide) {
    tblConf.value['api'] = './api/users'
  } else {
    tblConf.value['api'] = ''
  }
}

function confFieldWidthUpd(e) {
  if (e.target.checked) {
    fields[0]['width'] = '300px'
    fields[1]['width'] = '*px'
  } else {
    if (fields[0].width) delete fields.value[0].width
    if (fields[1].width) delete fields.value[1].width
  }
}
</script>
