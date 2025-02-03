import { createApp } from 'vue'
import Vuex from 'vuex'
import router from './router'
import store from './store'
import App from './App.vue'
import axios from 'axios'


console.log('Current NODE_ENV:', process.env.NODE_ENV)
const isDevelopment = process.env.NODE_ENV

if (isDevelopment === 'development') {
  axios.defaults.baseURL = 'http://localhost:8000'
} else {
  axios.defaults.baseURL = 'https://it245151.uni-graz.at:8000'
}
// axios.defaults.baseURL = 'https://it245151.uni-graz.at'
// axios.defaults.baseURL = 'http://localhost:8000'
// axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*'
const app = createApp(App)
app.use(Vuex)
app.use(store)
app.use(router, axios)
app.mount('#app')

document.title = 'CC - Explorer'


