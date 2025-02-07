import { createApp } from 'vue'
import Vuex from 'vuex'
import router from './router'
import store from './store'
import App from './App.vue'
import axios from 'axios'

axios.defaults.baseURL = 'https://it245151.uni-graz.at'
// axios.defaults.baseURL = 'https://api.cc-explorer.com'
// axios.defaults.baseURL = 'http://127.0.0.1:8000'
// axios.defaults.baseURL = 'http://localhost:8000'
// axios.defaults.baseURL = 'http://django:8000'
// axios.defaults.baseURL = 'http://167.99.251.188:8000'
// axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*'
const app = createApp(App)
app.use(Vuex)
app.use(store)
app.use(router, axios)
app.mount('#app')

document.title = 'CC - Explorer'


