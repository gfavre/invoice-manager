import { createApp } from 'vue'
import App from './App.vue'
import i18n from './i18n'
import axios from 'axios';
import VueCookies from "vue-cookies";

//import './axios-config.js'

//axios.defaults.xsrfCookieName = 'csrftoken';
//axios.defaults.xsrfHeaderName = 'X-CSRFToken';
//axios.defaults.withCredentials = true
axios.get('/api/csrf-token/').then(response => {
  const csrfToken = response.data.csrf_token;
  axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
})
const app = createApp(App)
app.config.globalProperties.$http = axios;
app.use(i18n).use(VueCookies).mount('#app');