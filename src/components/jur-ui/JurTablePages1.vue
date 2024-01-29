<template>
  <span class="jur_table_pagination">
    <button
      @click="tbl.loadData({ page: tbl.pageCurrent - 1 })"
      :disabled="tbl.pageCurrent == 1"
    >
      Previous
    </button>
    <button
      :class="{ active: tbl.pageCurrent === page }"
      @click="tbl.loadData({ page: page })"
      v-for="page in getBeginPages()"
      :key="page"
    >
      {{ page }}
    </button>
    <button v-if="isMidExists" :disabled="true">...</button>
    <button
      :class="{ active: tbl.pageCurrent === page }"
      @click="tbl.loadData({ page: page })"
      v-for="page in getMidPages()"
      :key="page"
    >
      {{ page }}
    </button>
    <button v-if="isEndExists || tbl.pageTotal > 6" :disabled="true">...</button>
    <button
      :class="{ active: tbl.pageCurrent === page }"
      @click="tbl.loadData({ page: page })"
      v-for="page in getEndPages()"
      :key="page"
    >
      {{ page }}
    </button>
    <button
      @click="tbl.loadData({ page: tbl.pageCurrent + 1 })"
      :disabled="tbl.pageCurrent >= tbl.pageTotal"
    >
      Next
    </button>
  </span>
</template>

<script setup>
import { computed } from 'vue'
import { tableHelperStore } from '@/stores/jurTableHelper'

const props = defineProps({ uid: { type: Number } })
const tbl = tableHelperStore(props.uid)()

const isMidExists = computed(() => {
  const res =
    tbl.pageCurrent > 4 &&
    tbl.pageCurrent + 4 <= tbl.pageTotal &&
    tbl.pageTotal > 9
  return res
})

const isEndExists = computed(() => {
  const res =
    tbl.pageCurrent > tbl.pageTotal - 4 &&
    tbl.pageCurrent <= tbl.pageTotal &&
    tbl.pageTotal > 5
  return res
})

const getBeginPages = () => {
  if (isEndExists.value) {
    return [1]
  } else if (isMidExists.value) {
    return [1]
  } else {
    const res = []
    for (let i = 1; i <= tbl.pageTotal && i <= 5; i++) res.push(i)
    return res
  }
}

const getMidPages = () => {
  if (isMidExists.value)
    return [tbl.pageCurrent - 1, tbl.pageCurrent, tbl.pageCurrent + 1]
  return []
}

const getEndPages = () => {
  if (isEndExists.value) {
    return [
      tbl.pageTotal - 4,
      tbl.pageTotal - 3,
      tbl.pageTotal - 2,
      tbl.pageTotal - 1,
      tbl.pageTotal
    ]
  } else if (isMidExists.value || tbl.pageTotal > 5) {
    return [tbl.pageTotal]
  }
  return []
}
</script>

<style scoped>
.jur_table_pagination > button {
  box-sizing: border-box;
  display: inline-block;
  min-width: 1.5em;
  padding: 0.5em 1em;
  margin-left: 2px;
  text-align: center;
  text-decoration: none !important;
  cursor: pointer;
  color: #333 !important;
  border: 1px solid transparent;
  border-radius: 0.375rem;
  background-color: transparent;
}
.jur_table_pagination > button:hover:enabled {
  border: 1px solid #727272;
  /* background-color: #221b30 !important; */
  color: #ffffff important;
}
.jur_table_pagination > .active {
  border: 1px solid #727272;
  background-image: linear-gradient (rgb(238, 238, 238), rgb (189, 189, 189));
}
.jur_table_pagination > button:disabled,
.jur_table_pagination > button[disabled] {
  /* background-color: #cccccc; */
  color: #9c9c9c !important;
  pointer-events: none;
}
</style>
