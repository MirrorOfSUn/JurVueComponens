// import './assets/main.css'
// bootstrap
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
// Elements
//import ElementPlus from 'element-plus'
// import './styles/element/jur_theme_colors.css'
// import './styles/element/jur_theme.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
// app.use(ElementPlus) // add Element Plus
app.use(router)

app.mount('#app')
