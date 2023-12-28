<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

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

loadData()

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

  // load data
  const apiParam = {
    page_size: data.value.page_size,
    page: page
  }
  axios.post(props.api, apiParam).then((response) => {
    //console.log('ajax', response.data)
    data.value = response.data
  })
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
      const fieldValue = 'data' in props.fields[ind] ? props.fields[ind].data(rec) : rec[fieldName]
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
</script>
<template>
  <div class="page-content page-container" id="page-content">
    <div class="padding">
      <div class="row">
        <div class="col">
          <div class="container-fluid d-flex justify-content-center">
            <div
              class="list list-row card"
              id="sortable"
              data-sortable-id="0"
              aria-dropeffect="move"
            >
              <div
                class="list-item"
                data-id="13"
                data-item-sortable-id="0"
                draggable="true"
                role="option"
                aria-grabbed="false"
                style=""
              >
                <div>
                  <button href="#" data-abc="true" class="w-40 avatar gd-primary">AB</button>
                </div>
                <div class="flex">
                  <a href="#" class="item-author text-color" data-abc="true">Patrick Linod</a>
                  <div class="item-except text-muted text-sm h-1x">
                    For what reason would it be advisable for me to think about business content?
                  </div>
                </div>
                <div class="no-wrap">
                  <div class="item-date text-muted text-sm d-none d-md-block">3 weeks ago</div>
                </div>
                <div>
                  <div class="item-action dropdown">
                    <a href="#" data-toggle="dropdown" class="text-muted" data-abc="true">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="feather feather-more-vertical"
                      >
                        <circle cx="12" cy="12" r="1"></circle>
                        <circle cx="12" cy="5" r="1"></circle>
                        <circle cx="12" cy="19" r="1"></circle>
                      </svg>
                    </a>
                    <div class="dropdown-menu dropdown-menu-right bg-black" role="menu">
                      <a class="dropdown-item" href="#" data-abc="true">See detail </a
                      ><a class="dropdown-item download" data-abc="true">Download </a
                      ><a class="dropdown-item edit" data-abc="true">Edit</a>
                      <div class="dropdown-divider"></div>
                      <a class="dropdown-item trash" data-abc="true">Delete item</a>
                    </div>
                  </div>
                </div>
              </div>
              <div
                class="list-item"
                data-id="9"
                data-item-sortable-id="0"
                draggable="true"
                role="option"
                aria-grabbed="false"
              >
                <div>
                  <a href="#" data-abc="true"
                    ><span class="w-40 avatar gd-info"
                      ><img src="https://img.icons8.com/bubbles/24/000000/user.png" alt="." /></span
                  ></a>
                </div>
                <div class="flex">
                  <a href="#" class="item-author text-color" data-abc="true">Steven Hmpire</a>
                  <div class="item-except text-muted text-sm h-1x">
                    Build a progressive web app using jQuery
                  </div>
                </div>
                <div class="no-wrap">
                  <div class="item-date text-muted text-sm d-none d-md-block">2 days ago</div>
                </div>
                <div>
                  <div class="item-action dropdown">
                    <a href="#" data-toggle="dropdown" class="text-muted" data-abc="true">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="feather feather-more-vertical"
                      >
                        <circle cx="12" cy="12" r="1"></circle>
                        <circle cx="12" cy="5" r="1"></circle>
                        <circle cx="12" cy="19" r="1"></circle>
                      </svg>
                    </a>
                    <div class="dropdown-menu dropdown-menu-right bg-black" role="menu">
                      <a class="dropdown-item" href="#" data-abc="true">See detail </a
                      ><a class="dropdown-item download" data-abc="true">Download </a
                      ><a class="dropdown-item edit" data-abc="true">Edit</a>
                      <div class="dropdown-divider"></div>
                      <a class="dropdown-item trash" data-abc="true">Delete item</a>
                    </div>
                  </div>
                </div>
              </div>
              <div
                class="list-item"
                data-id="17"
                data-item-sortable-id="0"
                draggable="true"
                role="option"
                aria-grabbed="false"
                style=""
              >
                <div>
                  <a href="#" data-abc="true"><span class="w-40 avatar gd-warning">A</span></a>
                </div>
                <div class="flex">
                  <a href="#" class="item-author text-color" data-abc="true">Alan musk</a>
                  <div class="item-except text-muted text-sm h-1x">
                    it be advisable for me to think about business content?
                  </div>
                </div>
                <div class="no-wrap">
                  <div class="item-date text-muted text-sm d-none d-md-block">13/12 18</div>
                </div>
                <div>
                  <div class="item-action dropdown">
                    <a href="#" data-toggle="dropdown" class="text-muted" data-abc="true">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="feather feather-more-vertical"
                      >
                        <circle cx="12" cy="12" r="1"></circle>
                        <circle cx="12" cy="5" r="1"></circle>
                        <circle cx="12" cy="19" r="1"></circle>
                      </svg>
                    </a>
                    <div class="dropdown-menu dropdown-menu-right bg-black" role="menu">
                      <a class="dropdown-item" href="#" data-abc="true">See detail </a
                      ><a class="dropdown-item download" data-abc="true">Download </a
                      ><a class="dropdown-item edit" data-abc="true">Edit</a>
                      <div class="dropdown-divider"></div>
                      <a class="dropdown-item trash" data-abc="true">Delete item</a>
                    </div>
                  </div>
                </div>
              </div>
              <div
                class="list-item"
                data-id="8"
                data-item-sortable-id="0"
                draggable="true"
                role="option"
                aria-grabbed="false"
              >
                <div>
                  <a href="#" data-abc="true"
                    ><span class="w-40 avatar gd-success"
                      ><img
                        src="https://img.icons8.com/doodle/24/000000/user-male.png"
                        alt="." /></span
                  ></a>
                </div>
                <div class="flex">
                  <a href="#" class="item-author text-color" data-abc="true">Lawrence Telon</a>
                  <div class="item-except text-muted text-sm h-1x">
                    For what reason would it be advisable for me to think
                  </div>
                </div>
                <div class="no-wrap">
                  <div class="item-date text-muted text-sm d-none d-md-block">02/11 18</div>
                </div>
                <div>
                  <div class="item-action dropdown">
                    <a href="#" data-toggle="dropdown" class="text-muted" data-abc="true">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="feather feather-more-vertical"
                      >
                        <circle cx="12" cy="12" r="1"></circle>
                        <circle cx="12" cy="5" r="1"></circle>
                        <circle cx="12" cy="19" r="1"></circle>
                      </svg>
                    </a>
                    <div class="dropdown-menu dropdown-menu-right bg-black" role="menu">
                      <a class="dropdown-item" href="#" data-abc="true">See detail </a
                      ><a class="dropdown-item download" data-abc="true">Download </a
                      ><a class="dropdown-item edit" data-abc="true">Edit</a>
                      <div class="dropdown-divider"></div>
                      <a class="dropdown-item trash" data-abc="true">Delete item</a>
                    </div>
                  </div>
                </div>
              </div>
              <div
                class="list-item"
                data-id="10"
                data-item-sortable-id="0"
                draggable="true"
                role="option"
                aria-grabbed="false"
                style=""
              >
                <div>
                  <a href="#" data-abc="true"
                    ><span class="w-40 avatar gd-danger"
                      ><img
                        src="https://img.icons8.com/color/16/000000/administrator-male.png"
                        alt="." /></span
                  ></a>
                </div>
                <div class="flex">
                  <a href="#" class="item-author text-color" data-abc="true">Stuart Clark</a>
                  <div class="item-except text-muted text-sm h-1x">
                    For what reason would, i think about business content?
                  </div>
                </div>
                <div class="no-wrap">
                  <div class="item-date text-muted text-sm d-none d-md-block">1 day ago</div>
                </div>
                <div>
                  <div class="item-action dropdown">
                    <a href="#" data-toggle="dropdown" class="text-muted" data-abc="true">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="feather feather-more-vertical"
                      >
                        <circle cx="12" cy="12" r="1"></circle>
                        <circle cx="12" cy="5" r="1"></circle>
                        <circle cx="12" cy="19" r="1"></circle>
                      </svg>
                    </a>
                    <div class="dropdown-menu dropdown-menu-right bg-black" role="menu">
                      <a class="dropdown-item" href="#" data-abc="true">See detail </a
                      ><a class="dropdown-item download" data-abc="true">Download </a
                      ><a class="dropdown-item edit" data-abc="true">Edit</a>
                      <div class="dropdown-divider"></div>
                      <a class="dropdown-item trash" data-abc="true">Delete item</a>
                    </div>
                  </div>
                </div>
              </div>
              <div
                class="list-item"
                data-id="3"
                data-item-sortable-id="0"
                draggable="true"
                role="option"
                aria-grabbed="false"
              >
                <div>
                  <a href="#" data-abc="true"
                    ><span class="w-40 avatar gd-primary"
                      ><img
                        src="https://img.icons8.com/bubbles/16/000000/administrator-male.png"
                        alt="." /></span
                  ></a>
                </div>
                <div class="flex">
                  <a href="#" class="item-author text-color" data-abc="true">Jordan Stephens</a>
                  <div class="item-except text-muted text-sm h-1x">
                    For what reason would it be advisable for me to think about business
                  </div>
                </div>
                <div class="no-wrap">
                  <div class="item-date text-muted text-sm d-none d-md-block">1 hour ago</div>
                </div>
                <div>
                  <div class="item-action dropdown">
                    <a href="#" data-toggle="dropdown" class="text-muted" data-abc="true">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="feather feather-more-vertical"
                      >
                        <circle cx="12" cy="12" r="1"></circle>
                        <circle cx="12" cy="5" r="1"></circle>
                        <circle cx="12" cy="19" r="1"></circle>
                      </svg>
                    </a>
                    <div class="dropdown-menu dropdown-menu-right bg-black" role="menu">
                      <a class="dropdown-item" href="#" data-abc="true">See detail </a
                      ><a class="dropdown-item download" data-abc="true">Download </a
                      ><a class="dropdown-item edit" data-abc="true">Edit</a>
                      <div class="dropdown-divider"></div>
                      <a class="dropdown-item trash" data-abc="true">Delete item</a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
body {
  background-color: #f9f9fa;
}

.flex {
  -webkit-box-flex: 1;
  -ms-flex: 1 1 auto;
  flex: 1 1 auto;
}

@media (max-width: 991.98px) {
  .padding {
    padding: 1.5rem;
  }
}

@media (max-width: 767.98px) {
  .padding {
    padding: 1rem;
  }
}

.padding {
  padding: 5rem;
}

.card {
  background: #fff;
  border-width: 0;
  border-radius: 0.25rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  margin-bottom: 1.5rem;
}

.card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
  border: 1px solid rgba(19, 24, 44, 0.125);
  border-radius: 0.25rem;
}

.list-item {
  position: relative;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-direction: column;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
}

.list-item.block .media {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}

.list-item.block .list-content {
  padding: 1rem;
}

.w-40 {
  width: 40px !important;
  height: 40px !important;
}

.avatar {
  position: relative;
  line-height: 1;
  border-radius: 500px;
  white-space: nowrap;
  font-weight: 700;
  border-radius: 100%;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-pack: center;
  justify-content: center;
  -ms-flex-align: center;
  align-items: center;
  -ms-flex-negative: 0;
  flex-shrink: 0;
  border-radius: 500px;
  box-shadow: 0 5px 10px 0 rgba(50, 50, 50, 0.15);
}

.avatar img {
  border-radius: inherit;
  width: 100%;
}

.gd-primary {
  color: #fff;
  border: none;
  background: #448bff linear-gradient(45deg, #448bff, #44e9ff);
}

.gd-primary:hover {
  background: #448bff linear-gradient(45deg, #0062ff, #44e9ff);
}

.flex {
  -webkit-box-flex: 1;
  -ms-flex: 1 1 auto;
  flex: 1 1 auto;
}

.text-color {
  color: #5e676f;
}

.text-sm {
  font-size: 0.825rem;
}

.h-1x {
  height: 1.25rem;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
}

.no-wrap {
  white-space: nowrap;
}

.list-row .list-item {
  -ms-flex-direction: row;
  flex-direction: row;
  -ms-flex-align: center;
  align-items: center;
  padding: 0.75rem 0.625rem;
}

.list-item {
  position: relative;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-direction: column;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
}

.list-row .list-item > * {
  padding-left: 0.625rem;
  padding-right: 0.625rem;
}

.dropdown {
  position: relative;
}

a:focus,
a:hover {
  text-decoration: none;
}

list-item {
  background: white;
}
</style>
