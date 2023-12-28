<template>
  <span class="jur_table_pagination">
    <button
      @click="$emit('reload', { page: data.current_page - 1 })"
      :disabled="data.current_page == 1"
    >
      Previous
    </button>
    <button
      :class="{ active: data.current_page === page }"
      @click="$emit('reload', { page: page })"
      v-for="page in getBeginPages()"
      :key="page"
    >
      {{ page }}
    </button>
    <button v-if="isMidExists" :disabled="true">...</button>
    <button
      :class="{ active: data.current_page === page }"
      @click="$emit('reload', { page: page })"
      v-for="page in getMidPages()"
      :key="page"
    >
      {{ page }}
    </button>
    <button v-if="isEndExists || data.total_pages > 6" :disabled="true">...</button>
    <button
      :class="{ active: data.current_page === page }"
      @click="$emit('reload', { page: page })"
      v-for="page in getEndPages()"
      :key="page"
    >
      {{ page }}
    </button>
    <button
      @click="$emit('reload', { page: data.current_page + 1 })"
      :disabled="data.current_page >= data.total_pages"
    >
      Next
    </button>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps(['data'])
defineEmits(['reload'])

const isMidExists = computed(() => {
  const res =
    props.data.current_page > 4 &&
    props.data.current_page + 4 <= props.data.total_pages &&
    props.data.total_pages > 9
  return res
})

const isEndExists = computed(() => {
  const res =
    props.data.current_page > props.data.total_pages - 4 &&
    props.data.current_page <= props.data.total_pages &&
    props.data.total_pages > 5
  return res
})

const getBeginPages = () => {
  if (isEndExists.value) {
    return [1]
  } else if (isMidExists.value) {
    return [1]
  } else {
    const res = []
    for (let i = 1; i <= props.data.total_pages && i <= 5; i++) res.push(i)
    return res
  }
}

const getMidPages = () => {
  // if (isEndExists.value) {
  //   return []
  // } else
  if (isMidExists.value) {
    return [props.data.current_page - 1, props.data.current_page, props.data.current_page + 1]
  }
  // else {
  //   return []
  // }
  return []
}

const getEndPages = () => {
  if (isEndExists.value) {
    return [
      props.data.total_pages - 4,
      props.data.total_pages - 3,
      props.data.total_pages - 2,
      props.data.total_pages - 1,
      props.data.total_pages
    ]
  } else if (isMidExists.value || props.data.total_pages > 5) {
    return [props.data.total_pages]
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
</style>
