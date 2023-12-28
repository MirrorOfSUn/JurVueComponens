<template>
  <div class="row header">
    <div class="col-3"><jurTablePageSize :def="pageSize" @reload="loadData" /></div>
    <div class="col-3"></div>
    <div class="col-auto"><jurTableSearch :search="search" @reload="loadData" /></div>
  </div>
  <table class="table table-hover">
    <thead>
      <tr>
        <th scope="col" v-for="(field, index) in tableFields" :key="index">{{ field.label }}</th>
      </tr>
    </thead>
    <tbody>
      <template v-for="(obj, index) in pageDataFiltered" :key="index">
        <tr>
          <td
            v-for="(field, ind) in tableFields"
            :key="index + ind / 10"
            @click="showItems.append(index)"
          >
            {{ field.data(obj) }}
          </td>
        </tr>
        <tr>
          <td :colspan="tableFields.length" v-if="showItems.includes(index)">test</td>
        </tr>
      </template>
    </tbody>
  </table>

  <div class="row footer">
    <div class="col-6">
      <slot name="footer">
        Showing {{ pageFirstRecord }} to {{ pageLastRecord }} of
        {{ pageTotalFilteredRecords }} entries
        <span v-if="pageTotalFilteredRecords != pageTotalRecords"
          >(filtered from {{ pageTotalRecords }} total entries)</span
        >
      </slot>
    </div>
    <div class="col-6 text-end">
      <jurTablePages v-model:data="data" @reload="loadData"></jurTablePages>
    </div>
  </div>
</template>

<script setup>
/**
 * jur-table component
 * show data table
 * have 2 options: ajax server side or client side only
 * for client side use:
 * <jur-table :datatable="<array of objects>" :fields="<array of fields>"/>
 *
 * for ajax server side use:
 * <jur-table :fields="<array of fields>" :api="'<get url for ajax call>'" :is-server-side="true" />
 *
 * where fields have format:
 * [
        {
            name: <name of field in dataset>',
            label: <label of field in the table>,
            sortable: true/false,
            // data is not required
            data: (rec) => {   // function to return data. rec - current record.
                return rec.FieldName
            }
        },
        { ... }
   ]
 * if  fields is not provided - used field names form dataset
 */
import { ref, computed } from 'vue'
import axios from 'axios'
import jurTablePages from '@/components/jur-ui/JurTablePages.vue'
import jurTablePageSize from '@/components/jur-ui/JurTablePageSize.vue'
import jurTableSearch from '@/components/jur-ui/JurTableSearch.vue'

const props = defineProps({
  fields: {
    // configuration of dataset.
    // format: [{name: '<name of field in dataset>', label: '<Labe of column>', sortable: true},...]
    type: Array,
    default: null
  },
  datatable: {
    type: Array,
    default: null
  },
  api: {
    type: String,
    default: ''
  },
  isServerSide: {
    type: Boolean,
    default: false
  },
  pageSize: {
    type: Number,
    default: 2
  },
  search: {
    type: String,
    default: ''
  },
  searchCustom: {
    type: Object,
    default: () => ({})
  }
})

const tableFields = ref([])
const showItems = ref([])
const data = ref({
  datatable: [], // dataset
  total_records: 0, // numbet of total records
  total_filtered_records: 0, //number of filtered records
  total_pages: 0, // max number of pages
  current_page: 1, // current page - first page=1
  page_size: props.pageSize, // records per page
  serarchString: props.search // search string for local data search. Not used for ajax
})

const pageFirstRecord = computed(() => {
  if (data.value.total_filtered_records > 0) {
    return (data.value.current_page - 1) * data.value.page_size + 1
  } else {
    return 0
  }
})

const pageLastRecord = computed(() => {
  if (pageFirstRecord.value + data.value.page_size - 1 <= data.value.total_filtered_records) {
    return pageFirstRecord.value + data.value.page_size - 1
  } else {
    return data.value.total_filtered_records
  }
})

const pageTotalRecords = computed(() => {
  return data.value.total_records
})

const pageTotalFilteredRecords = computed(() => {
  return data.value.total_filtered_records
})

const pageDataFiltered = computed(() => {
  if (props.isServerSide) {
    return data.value.datatable
  } else {
    return data.value.datatable.slice(
      (data.value.current_page - 1) * data.value.page_size,
      data.value.current_page * data.value.page_size
    )
  }
})
//"datatable":[],"total_records":4,"total_filtered_records":4,"total_pages":1,"current_page":0,"page_size":100

// initial load data - begin
if (props.fields) getFields()
loadData()
if (!props.fields) getFields()
// initial load data - ens

function getFields() {
  // get list of fields
  // 1. check if fields list provided in props "fields" - if yes - use it
  // 2. if not -read first record of datatable and use field names
  // format of fields:
  // [{name: <field name in dataset>,
  //   label: <label of column>,
  //   sort: <T/F if we can sort by this field>,
  //   search: <T/F serch by this field>,
  //   hidden: <T/F do not show this field in table>}]
  if (props.fields) {
    // if field set provided
    tableFields.value = props.fields
  } else {
    // update field set if not provided
    if (data.value.datatable.length > 0) {
      for (let key in data.value.datatable[0]) {
        tableFields.value.push({ name: key, label: key, sort: true, search: true, hidden: false })
      }
    } else {
      // no data - field list will be empty
      return
    }
  }
  // if data function is not defined - set it
  tableFields.value.forEach((item) => {
    item.data =
      item.data ||
      function (rec) {
        return rec[item.name]
      }
  })
}

function loadData(param = {}) {
  let page = param.page || data.value.current_page
  if (param.pageSize) {
    data.value.page_size = param.pageSize
    page = 1
  }
  if ('search' in param) {
    data.value.serarchString = param.search
    page = 1
  }
  console.log('sss=', param.search)

  // load data
  if (props.isServerSide) {
    const apiUrl = props.api + '?page_size=' + data.value.page_size + '&page=' + page
    axios.get(apiUrl).then((response) => {
      //console.log('ajax', response.data)
      data.value = response.data
    })
  } else {
    data.value.current_page = page
    //data.value.page_size = props.pageSize // set pageSize
    data.value.datatable = [...localDataFilter()]
    //data.value.datatable = props.datatable // set data
    // generate page data
    data.value.total_records = props.datatable.length // number of records
    data.value.total_filtered_records = data.value.datatable.length // number of filtered records
    data.value.total_pages = Math.ceil(data.value.datatable.length / data.value.page_size)
  }

  function* localDataFilter() {
    const fields = []
    const searchString = data.value.serarchString

    // create lists of fields for search
    for (let ind in props.fields) {
      if (props.fields[ind].searchable !== false) fields.push(ind)
    }
    for (let recordInx in props.datatable) {
      const rec = props.datatable[recordInx]
      for (let ind in fields) {
        const fieldName = props.fields[ind].name
        const fieldType = props.fields[ind].type === 'number' ? 'number' : 'string'
        const fieldValue =
          'data' in props.fields[ind] ? props.fields[ind].data(rec) : rec[fieldName]
        if (fieldType === 'string') {
          if (fieldValue.includes(searchString)) {
            yield rec
            break
          }
        } else {
          // number
          if (Number(fieldValue) && Number(searchString)) {
            if (Number(fieldValue) == Number(searchString)) {
              console.log('s2', rec)
              yield rec
              break
            }
          }
        }
      }
    }
  }
}
</script>

<style scoped>
.footer {
  padding-left: 8px;
  padding-right: 8px;
}
</style>
