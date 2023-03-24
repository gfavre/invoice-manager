import { createApp } from 'vue'
import App from './App.vue'
import i18n from './i18n'
import axios from 'axios';
import VueCookies from "vue-cookies";

axios.get('http://127.0.0.1:8000/api/csrf-token/').then(response => {
  const csrfToken = response.data.csrf_token;
  axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
})
axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://127.0.0.1:8000';

const app = createApp(App)
app.config.globalProperties.$http = axios;
app.use(i18n).use(VueCookies).mount('#app');
