import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const tableHelperStore = function (tblId) {
  return defineStore('tblHelper-' + tblId, () => {
    const data = ref({
      datatable: [], // dataset
      datatable_selected: [], // list of index selected items
      total_records: 0, // numbet of total records
      total_filtered_records: 0, //number of filtered records
      total_pages: 0, // max number of pages
      current_page: 1, // current page - first page=1
      page_size: 3, // records per page
      searchString: '', // search string for local data search. Not used for ajax
      searchCustom: {}
    })
    const conf = ref({
      api: '',
      isServerSide: false,
      // configuration of dataset.
      // format: [{name: '<name of field in dataset>', label: '<Labe of column>', sortable: true},...]
      fields: [],
      bulk: false, // enable/disable checkboxes for multiselect
      showdetails: false
    })

    function config({
      api = '',
      isServerSide = false,
      fields = null,
      datatable = [],
      bulk = false,
      showdetails = false
    } = {}) {
      conf.value.api = api
      conf.value.isServerSide = isServerSide
      data.value.datatable = datatable
      conf.value.bulk = bulk
      conf.value.showdetails = showdetails
      if (fields !== null) {
        // if fields configuration provided
        conf.value.fields = fields
      }
      getFields()
      loadData()
      getFields()
    }

    const select = {
      isSelected: function (ind) {
        const localInd = ind + data.value.current_page * data.value.page_size
        return data.value.datatable_selected.indexOf(localInd) > -1
      },
      toggle: function (ind) {
        const localInd = ind + data.value.current_page * data.value.page_size
        const index = data.value.datatable_selected.indexOf(localInd)
        if (index > -1) data.value.datatable_selected.splice(index, 1)
        else data.value.datatable_selected.push(localInd)
        console.log('toggle=', localInd, data.value.datatable_selected)
      },
      add: function (ind) {
        const localInd = ind + data.value.current_page * data.value.page_size
        data.value.datatable_selected.push(localInd)
      },
      del: function (ind) {
        const localInd = ind + data.value.current_page * data.value.page_size
        const index = data.value.datatable_selected.indexOf(localInd) // get index if value found otherwise -1
        if (index > -1) data.value.datatable_selected.splice(index, 1)
      },
      clear: function () {
        data.value.datatable_selected = []
      }
    }

    const isBulk = computed(() => {
      return conf.value.bulk
    })

    const isShowDetail = computed(() => {
      return conf.value.showdetails
    })

    const pageCurrent = computed(() => {
      return data.value.current_page
    })

    const pageTotal = computed(() => {
      return data.value.total_pages
    })

    const pageSize = computed(() => {
      return data.value.page_size
    })

    const searchString = computed(() => {
      return data.value.searchString
    })

    const fields = computed(() => {
      return conf.value.fields
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

    function* pageDataFiltered() {
      // return list of records for current page
      if (conf.value.isServerSide) {
        for (const line of data.value.datatable) {
          //console.log('line=', line)
          yield line
        }
      } else {
        const start_line = (data.value.current_page - 1) * data.value.page_size
        const end_line = data.value.current_page * data.value.page_size
        let i = 0

        for (const line of localDataFilter()) {
          if (i >= start_line && i < end_line) {
            //console.log('line=', line)
            yield line
          }
          i++
        }
      }
    }

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
      //   type: 'string', 'number', 'boolean'  (Default: string)
      //console.log('conf.value.fields=', conf.value.fields.length)
      if (conf.value.fields.length == 0) {
        conf.value.fields = []
        // update field set if not provided
        if (data.value.datatable.length > 0) {
          //console.log('field list will be empty: ', data.value.datatable[0])
          //console.log(data.value.datatable[0])
          const fieldWidth = Math.floor(100 / Object.keys(data.value.datatable[0]).length)
          for (let key in data.value.datatable[0]) {
            //console.log(key)
            conf.value.fields.push({
              name: key,
              label: key,
              sortable: true,
              searchable: true,
              hidden: false,
              type: typeof data.value.datatable[0][key],
              width: String(fieldWidth) + '%'
            })
          }
          conf.value.fields[conf.value.fields.length - 1].width = '*'
        } else {
          // no data - field list will be empty
          console.log('no data - field list will be empty')
          return
        }
      }
      // if data function is not defined - set it
      const fieldWidth = Math.floor(100 / Object.keys(conf.value.fields).length)
      conf.value.fields.forEach((item) => {
        item.width = item.width || String(fieldWidth) + '%'
        item.data =
          item.data ||
          function (rec) {
            return rec[item.name]
          }
      })
    }

    function loadData({
      page = data.value.current_page,
      pageSize = data.value.page_size,
      search = null
    } = {}) {
      // load data from server of change filters if data is local

      if (data.value.page_size != Number(pageSize)) {
        data.value.page_size = Number(pageSize)
        page = 1
      }
      if (search !== null && data.value.searchString != search) {
        data.value.searchString = search
        page = 1
        select.clear()
      }

      // load data
      if (conf.value.isServerSide) {
        const searchObj = {
          search: data.value.searchString || '',
          name: '',
          phone: '',
          email: '',
          address: '',
          page: page,
          page_size: data.value.page_size,
          is_active: true
        }

        axios.post(conf.value.api, searchObj).then((response) => {
          data.value.datatable = response.data.datatable
          data.value.total_records = response.data.total_records
          data.value.total_filtered_records = response.data.total_filtered_records
          data.value.total_pages = response.data.total_pages
          data.value.current_page = response.data.current_page
          data.value.page_size = response.data.page_size
          data.value.datatable_selected = []
        })
      } else {
        data.value.current_page = page
        data.value.total_records = data.value.datatable.length // number of records
        data.value.total_filtered_records = [...localDataFilter()].length // number of filtered records
        data.value.total_pages = Math.ceil(data.value.total_filtered_records / data.value.page_size)
      }
    }

    function* localDataFilter() {
      // return filtered data as Generator
      const fields = []
      const searchString = data.value.searchString.toLowerCase()

      // create lists of fields for search
      for (let ind in conf.value.fields) {
        if (conf.value.fields[ind].searchable !== false) fields.push(ind)
      }
      for (let recordInx in data.value.datatable) {
        const rec = data.value.datatable[recordInx]
        //console.log(rec)
        for (let ind in fields) {
          const fieldName = conf.value.fields[ind].name
          const fieldType = conf.value.fields[ind].type || 'string'
          const fieldValue =
            'data' in conf.value.fields[ind] ? conf.value.fields[ind].data(rec) : rec[fieldName]
          // console.log('fv=', fieldValue)
          if (fieldType === 'string') {
            // string
            if (fieldValue.toLowerCase().includes(searchString)) {
              yield rec
              break
            }
          } else if (fieldType === 'number') {
            // number
            if (Number(fieldValue) && Number(searchString)) {
              if (Number(fieldValue) == Number(searchString)) {
                yield rec
                break
              }
            }
          } else if (
            fieldType === 'boolean' &&
            (searchString === 'true' || searchString === 'false')
          ) {
            // boolean
            const bool = searchString === 'true'
            if (fieldValue === bool) {
              yield rec
              break
            }
          }
        }
      }
    }

    return {
      config,
      pageFirstRecord,
      pageLastRecord,
      pageTotalRecords,
      pageTotalFilteredRecords,
      pageSize,
      pageCurrent,
      pageTotal,
      searchString,
      isBulk,
      isShowDetail,
      pageDataFiltered,
      //searchString,
      loadData, // re-load data action
      fields, // return list of fields

      select // object with methods to select/unselect
    }
  })
}
