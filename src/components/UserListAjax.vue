<template>
  <el-table
    :data="datatable"
    :border="true"
    style="width: 100%"
    :row-class-name="tableRowClassName"
  >
    <el-table-column type="expand">
      <template #default="props">
        <div>
          <el-container>
            <el-main>
              <p m="t-0 b-2">State: {{ props.row.state }}</p>
              <p m="t-0 b-2">City: {{ props.row.city }}</p>
              <p m="t-0 b-2">Address: {{ props.row.address }}</p>
              <p m="t-0 b-2">Zip: {{ props.row.zip }}</p>
             
            </el-main>
          </el-container>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="Date" prop="date" />
    <el-table-column label="Name" prop="name" />
  </el-table>
</template>

<script setup>

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
// const showItems = ref([])
const data = ref({
  datatable: [], // dataset
  total_records: 0, // numbet of total records
  total_filtered_records: 0, //number of filtered records
  total_pages: 0, // max number of pages
  current_page: 1, // current page - first page=1
  page_size: props.pageSize, // records per page
  serarchString: props.search // search string for local data search. Not used for ajax
})

loadData()

const tableRowClassName = ({ row }) => {
  if (row.hasOrder){
    return 'warning-row'
  }
  return ''
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

  // load data
  const apiUrl = props.api + '?page_size=' + data.value.page_size + '&page=' + page
  axios.get(apiUrl).then((response) => {
    //console.log('ajax', response.data)
    data.value = response.data
  })
