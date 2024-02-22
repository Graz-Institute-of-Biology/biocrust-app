import { createApp } from 'vue'
import Vuex from 'vuex'
import router from './router'
import store from './store'
import App from './App.vue'
import axios from 'axios'

// axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.baseURL = 'http://167.99.251.188:8000'
// axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*'
const app = createApp(App)
app.use(Vuex)
app.use(store)
app.use(router, axios)
app.mount('#app')


