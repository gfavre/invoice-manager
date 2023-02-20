<template>
  <div id="div_id_client_type" class="form-group">
    <label for="id_client_type_0" class=" requiredField">
      {{ t("Type of client") }}<span class="asteriskField">*</span>
    </label>
    <div>
      <div class="custom-control custom-radio custom-control-inline">
        <input type="radio" class="custom-control-input" name="client_type" value="company"
               id="id_client_type_0" required=""
               v-model="clientType" />
        <label class="custom-control-label" for="id_client_type_0">
          <i class="bi bi-journal"></i> {{ t("company") }}
        </label>
      </div>
      <div class="custom-control custom-radio custom-control-inline">
        <input type="radio" class="custom-control-input" name="client_type" value="person"
               id="id_client_type_1" required=""
               v-model="clientType" />
        <label class="custom-control-label" for="id_client_type_1">
          <i class="bi bi-person-fill"></i>
          {{ t("person") }}
        </label>
      </div>
    </div>
  </div>

  <section v-if="clientType=='person'">
    <h1>{{ t("person") }}</h1>
    <person-form></person-form>
  </section>

  <section v-else>
    <fieldset class="border-left-primary shadow" id="company_infos">
    <legend class=" mb-1">Entreprise</legend>
    <h1>Company</h1>
    <company-search append="toto" placeholder="company lookup"
                    autocompleteUrl="http://127.0.0.1:8000/api/companies/"
                    companyDetailUrl="http://127.0.0.1:8000/api/company-detail/"
                    @callback="companyDetailLookupResult"></company-search>
    <company-form></company-form>
    </fieldset>
    <dl v-if="selectedCompany != null">
      <dt>The company</dt>
      <dd>{{ selectedCompany }}</dd>
    </dl>

  </section>


</template>

<script>
import PersonForm from './components/person-form.vue';
import CompanyForm from './components/company-form.vue';
import companySearch from "./components/company-search.vue";

import {useI18n} from 'vue-i18n'


export default {
  name: 'App',
  //i18n,
  components: {
    'person-form': PersonForm,
    'company-form': CompanyForm,
    'company-search': companySearch
  },
  data() {
    return {
      selectedCompany: null,
      clientType: 'company'

    }
  },
  methods: {
    companyDetailLookupResult(company) {
      this.selectedCompany = company;
    }
  },
  setup() {
    const {t} = useI18n({
      inheritLocale: true,
      useScope: 'local'
    })

    return {t}
  }
}
</script>

<style>

@import 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css';
</style>

<i18n>
{
  "fr": {
    "company": "Entreprise",
    "person": "Personne",
    "Type of client": "Type de client"
  },
  "en": {
    "company": "Company",
    "person": "Person",
    "Type of client": "Type of client"
  }
}
</i18n>
