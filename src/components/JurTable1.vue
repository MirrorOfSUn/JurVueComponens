<template>
  <div class="row header">
    <div class="col-3"><jurTablePageSize :uid="uid" /></div>
    <div class="col-3"></div>
    <div class="col-auto">
      <jurTableSearch :uid="uid" />
    </div>
  </div>
  <table class="table table-hover">
    <thead>
      <tr>
        <th class="detail-nav" v-if="tbl.isShowDetail"></th>
        <th class="detail-nav" v-if="tbl.isBulk">
          <input class="form-check-input" type="checkbox" value="{{ index }}" v-if="tbl.isBulk" />
        </th>
        <th
          scope="col"
          v-for="(field, index) in tbl.fields"
          :key="index"
          :style="'width: ' + field.width"
        >
          {{ field.label }}
        </th>
      </tr>
    </thead>
    <tbody>
      <template v-for="(obj, index) in tbl.pageDataFiltered()" :key="index">
        <tr :class="{ [config.colors.odd]: index % 2, [config.colors.even]: !(index % 2) }">
          <td v-if="tbl.isShowDetail" class="td-m">
            <div
              class="icon-play3 icon"
              @click="tbl.select.toggle(index)"
              :class="{ 'icon-active': tbl.select.isSelected(index) }"
            ></div>
          </td>
          <td v-if="tbl.isBulk" class="td-m">
            <input class="form-check-input" type="checkbox" value="{{ index }}" />
          </td>
          <td v-for="(field, ind) in tbl.fields" :key="index + ind / 10">
            {{ field.data(obj) }}
          </td>
        </tr>
        <tr v-if="tbl.select.isSelected(index)">
          <td :colspan="tbl.fields.length + (tbl.isShowDetail ? 1 : 0) + (tbl.isBulk ? 1 : 0)">
            <slot></slot>
          </td>
        </tr>
      </template>
    </tbody>
  </table>

  <div class="row footer">
    <div class="col-4">
      <slot name="footer">
        Showing {{ tbl.pageFirstRecord }} to {{ tbl.pageLastRecord }} of
        {{ tbl.pageTotalFilteredRecords }} entries
        <span v-if="tbl.pageTotalFilteredRecords != tbl.pageTotalRecords"
          >(filtered from {{ tbl.pageTotalRecords }} total entries)</span
        >
      </slot>
    </div>
    <div class="col-8 text-end">
      <jurTablePages :uid="uid"></jurTablePages>
    </div>
  </div>
</template>

<script setup>
import { getCurrentInstance, watch } from 'vue'
import jurTablePages from '@/components/jur-ui/JurTablePages1.vue'
import jurTablePageSize from '@/components/jur-ui/JurTablePageSize1.vue'
import jurTableSearch from '@/components/jur-ui/JurTableSearch1.vue'
import { tableHelperStore } from '@/stores/jurTableHelper'

const props = defineProps({
  config: {
    type: Object,
    default: null
  }
})

watch(props, () => {
  // watch(props, (newVal, oldVal) => {
  tbl.config(props.config)
})

const uid = props.config.id || getCurrentInstance().uid
// console.log('table uid=', uid)
const tbl = tableHelperStore(uid)()
tbl.config(props.config)

//"datatable":[],"total_records":4,"total_filtered_records":4,"total_pages":1,"current_page":0,"page_size":100
</script>

<style scoped>
table {
  table-layout: auto;
}
.footer {
  padding-left: 8px;
  padding-right: 8px;
}

.detail-nav {
  width: 5px;
}

@font-face {
  font-family: 'icomoon';
  src: url('@/assets/fonts/icomoon.eot?jewo5n');
  src:
    url('@/assets/fonts/icomoon.eot?jewo5n#iefix') format('embedded-opentype'),
    url('@/assets/fonts/icomoon.ttf?jewo5n') format('truetype'),
    url('@/assets/fonts/icomoon.woff?jewo5n') format('woff'),
    url('@/assets/fonts/icomoon.svg?jewo5n#icomoon') format('svg');
  font-weight: normal;
  font-style: normal;
  font-display: block;
}

[class^='icon-'],
[class*=' icon-'] {
  /* use !important to prevent issues with browser extensions that change fonts */
  font-family: 'icomoon' !important;
  /* speak: never; */
  font-style: normal;
  font-weight: normal;
  font-variant: normal;
  text-transform: none;
  line-height: 1;

  /* Better Font Rendering =========== */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.icon-plus:before {
  content: '\ea0a';
}
.icon-minus:before {
  content: '\ea0b';
}
.icon-play3:before {
  padding-top: 5px;
  content: '\ea1c';
}

/* .panel-heading  a:before {
   font-family: 'Glyphicons Halflings';
   content: "\e114";
   float: right;
   transition: all 0.5s;
} */
.td-m {
  /* transition: all 0.5s; */
  vertical-align: middle;
}
.icon-active {
  transition: all 0.5s;
  -webkit-transform: rotate(90deg);
  -moz-transform: rotate(90deg);
  transform: rotate(90deg);
}
</style>
