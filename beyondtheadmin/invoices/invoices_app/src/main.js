import { createApp } from "vue";
import App from "./App.vue";
import i18n from "./i18n";
import axios from "axios";
import VueCookies from "vue-cookies";

axios.get("/api/csrf-token/").then((response) => {
  const csrfToken = response.data.csrf_token;
  axios.defaults.headers.common["X-CSRFToken"] = csrfToken;
});
const app = createApp(App);
app.config.globalProperties.$http = axios;
app.config.globalProperties.$formatAmount = function (float) {
  let formatted = float.toFixed(2);
  formatted = formatted.replace(/\.00$/, ".-");
  return formatted;
};
app.use(i18n).use(VueCookies).mount("#app");
