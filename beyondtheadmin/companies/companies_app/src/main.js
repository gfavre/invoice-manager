import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios';
import vueCountryRegionSelect from 'vue3-country-region-select'
import { VeeValidatePlugin } from 'vee-validate';

import i18n from './i18n'
//mport VueCookies from "vue-cookies";
const API_DOMAIN = process.env.VUE_APP_API_DOMAIN;
axios.defaults.baseURL = API_DOMAIN;

axios.get(API_DOMAIN + '/api/csrf-token/').then(response => {
  const csrfToken = response.data.csrf_token;
  axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
})
const app = createApp(App)
app.config.globalProperties.$http = axios;
app.config.globalProperties.$formatAmount = function(float) {
  let formatted = float.toFixed(2);
  formatted = formatted.replace(/\.00$/, '.-');
  return formatted;
}
app.use(vueCountryRegionSelect);
app.use(VeeValidatePlugin);
app.use(i18n).mount('#app')
