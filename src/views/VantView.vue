<template>
  <van-button type="primary">{{ isMobilewidth }}</van-button>
  {{ screenWidth }}
  <van-row>
    <van-col :span="isMobilewidth ? 24 : 8">span: 8</van-col>
    <van-col :span="isMobilewidth ? 24 : 8">span: 8</van-col>
    <van-col :span="isMobilewidth ? 24 : 8">span: 8</van-col>
  </van-row>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { showToast } from 'vant'

const chosenContactId = ref('1')
const list = ref([
  {
    id: '1',
    name: 'John Snow',
    tel: '13000000000',
    isDefault: true
  },
  {
    id: '2',
    name: 'Ned Stark',
    tel: '1310000000'
  }
])

const onAdd = () => showToast('Add')
const onEdit = (contact) => showToast('Edit' + contact.id)
const onSelect = (contact) => showToast('Select' + contact.id)

const isMobilewidth = computed(() => {
  return screenWidth.value <= 1500
})

const screenWidth = ref(window.screen.width)

onMounted(() => {
  window.addEventListener('resize', handleWindowSizeChange)
  handleWindowSizeChange()
})
onUnmounted(() => {
  window.removeEventListener('resize', handleWindowSizeChange)
})
const handleWindowSizeChange = () => {
  console.log('Resize', window.screen.width)
  screenWidth.value = window.screen.width
}
</script>
