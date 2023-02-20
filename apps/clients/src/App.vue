<template>
  <div id="div_id_client_type" class="form-group">
    <label for="id_client_type_0" class=" requiredField">
      Type de client<span class="asteriskField">*</span> </label>
    <div>
      <div class="custom-control custom-radio custom-control-inline">
        <input type="radio" class="custom-control-input" name="client_type" value="company" id="id_client_type_0"
               required="" checked=""> <label class="custom-control-label" for="id_client_type_0"> <i
          class="bi bi-journal"></i> Entreprise
      </label></div>
      <div class="custom-control custom-radio custom-control-inline"><input type="radio" class="custom-control-input"
                                                                            name="client_type" value="person"
                                                                            id="id_client_type_1" required=""> <label
          class="custom-control-label" for="id_client_type_1"> <i class="bi bi-person-fill"></i> Personne
      </label></div>
    </div>
  </div>
  <div v-if="clientType=='person'">
    <h1>{{ $t('Person') }}</h1>
    <person-form></person-form>
  </div>
  <div v-else>
    <h1>Company</h1>
    <company-search append="toto" placeholder="company lookup"
                    autocompleteUrl="http://127.0.0.1:8000/api/companies/"
                    companyDetailUrl="http://127.0.0.1:8000/api/company-detail/"
                    @callback="companyDetailLookupResult"></company-search>
    <company-form></company-form>
    <dl v-if="selectedCompany != null">
      <dt>The company</dt>
      <dd>{{ selectedCompany }}</dd>
    </dl>

  </div>


</template>

<script>
import PersonForm from './components/person-form.vue';
import CompanyForm from './components/company-form.vue';
import companySearch from "./components/company-search.vue";

import VueI18n from 'vue-i18n';


const i18n = new VueI18n({
  locale: 'fr',
  messages: {
    fr: {
      'Company': 'Entreprise',
      'Person': 'Personne'
    }
  }
});

export default {
  name: 'App',
  i18n,
  components: {
    'person-form': PersonForm,
    'company-form': CompanyForm,
    'company-search': companySearch
  },
  data() {
    return {
      selectedCompany: null,
      clientType: 'person'

    }
  },
  methods: {
    companyDetailLookupResult(company) {
      this.selectedCompany = company;
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
