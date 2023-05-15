import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";
import vueCountryRegionSelect from "vue3-country-region-select";
import { plugin, defaultConfig } from "@formkit/vue";
import customConfig from "./formkit.config.js";
import i18n from "./i18n";
import VueCookies from "vue-cookies";

const API_DOMAIN = process.env.VUE_APP_API_DOMAIN;
axios.defaults.baseURL = API_DOMAIN;

axios.get(API_DOMAIN + "/api/csrf-token/").then((response) => {
  const csrfToken = response.data.csrf_token;
  axios.defaults.headers.common["X-CSRFToken"] = csrfToken;
});

const isCheckboxAndRadioMultiple = (node) =>
  (node.props.type === "checkbox" || node.props.type === "radio") &&
  node.props.options;

function addAsteriskPlugin(node) {
  node.on("created", () => {
    const schemaFn = node.props.definition.schema;
    node.props.definition.schema = (sectionsSchema = {}) => {
      const isRequired = node.props.parsedRules.some(
        (rule) => rule.name === "required"
      );

      if (isRequired) {
        if (isCheckboxAndRadioMultiple(node)) {
          sectionsSchema.legend = {
            children: ["$label", "*"],
          };
        } else {
          sectionsSchema.label = {
            children: ["$label", "*"],
          };
        }
      }
      return schemaFn(sectionsSchema);
    };
  });
}

const app = createApp(App);
app.config.globalProperties.$http = axios;
app.config.globalProperties.$formatAmount = function (float) {
  let formatted = float.toFixed(2);
  formatted = formatted.replace(/\.00$/, ".-");
  return formatted;
};
app.config.globalProperties.$filename = function (url) {
  if (!url) return "";
  return url.split("/").pop().split("#")[0].split("?")[0];
};
app
  .use(i18n)
  .use(
    plugin,
    defaultConfig({
      config: customConfig.config,
      plugins: [addAsteriskPlugin],
    })
  )
  .use(vueCountryRegionSelect)
  .use(VueCookies)
  .mount("#app");
