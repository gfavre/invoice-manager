<template>
  <div id="div_id_company" class="form-group" v-if="companies.length > 1">
    <label for="id_company_0" class=" requiredField">
      {{ $t('Client for')}}<span class="asteriskField">*</span>
    </label>
    <div>
      <div class="custom-control custom-radio custom-control-inline"
           v-for="cItem in companies" :key="cItem.id">
        <input type="radio" class="custom-control-input" name="company" required=""
               :value="cItem.id" :id="'company-' + cItem.id" v-model="company"
        />
        <label class="custom-control-label"
               :for="'company-' + cItem.id">
          {{ cItem.name }}
        </label>
      </div>
    </div>
    <hr>
  </div>

  <div id="div_id_client_type" class="form-group">
    <label for="id_client_type_0" class=" requiredField">
      {{ $t("Type of client") }}<span class="asteriskField">*</span>
    </label>
    <div>
      <div class="custom-control custom-radio custom-control-inline">
        <input type="radio" class="custom-control-input" name="client_type" value="company"
               id="id_client_type_0" required=""
               v-model="clientType"/>
        <label class="custom-control-label" for="id_client_type_0">
          <i class="bi bi-buildings"></i> {{ $t("Company") }}
        </label>
      </div>
      <div class="custom-control custom-radio custom-control-inline">
        <input type="radio" class="custom-control-input" name="client_type" value="person"
               id="id_client_type_1" required=""
               v-model="clientType"/>
        <label class="custom-control-label" for="id_client_type_1">
          <i class="bi bi-person-fill"></i>
          {{ $t("Person") }}
        </label>
      </div>
    </div>
  </div>

  <section v-show="isPerson">
    <fieldset class="border-left-info shadow" id="company_infos">
      <legend class=" mb-1">{{ $t("Person") }}</legend>
      <person-form ref="personForm"
                   @saved="handleComponentSaved"
                   @update:lastName="slugUpdate"></person-form>
    </fieldset>
  </section>

  <section v-show="isCompany">
    <fieldset class="border-left-primary shadow" id="company_infos">
      <legend class=" mb-1">{{ $t("Company") }}</legend>
      <company-form ref="companyForm"
                    @saved="handleComponentSaved"
                    @update:name="slugUpdate"></company-form>
    </fieldset>
  </section>

  <section>
    <fieldset class="border-left-success shadow ">
      <legend class=" mb-1">{{ $t("Invoices") }}</legend>
      <InvoiceForm ref="invoiceForm"
                   @saved="handleComponentSaved"
                   :company="selectedCompany"
                   :default-language="defaultLanguage"
                   :is-vat-enabled="vatEnabled"
                   :updated-slug="slug"></InvoiceForm>
    </fieldset>
  </section>

  <div class="buttonHolder">
    <input type="submit" name="submit" value="Enregistrer"
           class="btn btn-primary button white" id="submit-id-submit"
           :class="{disabled: !isFormComplete}"
           @click.prevent="isFormComplete? saveClient(): focusFirstError()"/>

  </div>

</template>

<script>
'use strict';

import PersonForm from '@/components/PersonForm.vue';
import CompanyForm from '@/components/CompanyForm.vue';
import InvoiceForm from "@/components/InvoiceForm.vue";
import {useI18n} from 'vue-i18n'


export default {
  name: 'App',
  components: {
    PersonForm,
    CompanyForm,
    InvoiceForm,

  },
  computed: {
    isCompany() {
      return this.clientType === 'company';
    },
    isPerson() {
      return this.clientType === 'person';
    },
    isFormComplete() {
      let dataForm = this.isPerson ? this.$refs.personForm : this.$refs.companyForm;
      //if (dataForm === undefined ||  this.$refs.invoiceForm === undefined) {
      //  return false;
      //}
      return this.company.length > 0 && dataForm.isFormComplete() && this.$refs.invoiceForm.isFormComplete();
    }
  },

  data() {
    return {
      clientType: 'company',
      slug: "",
      client: null,
      clientId: null,
      companies: [],
      company: "",
      selectedCompany: {},
      vatRate: 0,
      vatEnabled: true,

      savedComponentCount: 0,
      expectedComponentCount: 2,
      defaultLanguage: '',
      urls: {
        clientCreateUrl: '',
        clientUpdateUrl: '',
        clientRedirectUrl: '',
        companiesUrl: '',
      }
    }
  },
  methods: {
    handleComponentSaved() {
      /*
      Whether to use push() to navigate to a new route or window.location to redirect to a new page depends
      on your use case and the desired behavior.
      If you are using Vue Router to manage client-side navigation in your app, you should generally use
      push() to navigate to a new route. Vue Router is designed to handle client-side navigation in a
      single-page application (SPA) by updating the URL and rendering the appropriate components without
      triggering a full page reload. When you use push() to navigate to a new route, Vue Router will handle
      the navigation and update the URL in the address bar without causing a full page reload.

      On the other hand, if you want to redirect to a completely new page outside of your Vue app, you should
      use window.location to redirect to the new page. This will cause a full page reload and navigate the browser
      to the new page.

      this.$router.push({name: 'clients-list'});
      */
      this.savedComponentCount ++;
      if (this.savedComponentCount === this.expectedComponentCount) {
        window.location = this.urls.clientRedirectUrl;
      }
    },
    focusFirstError(){
      const formInputs = document.querySelectorAll('input[required]');
      const invalidInputs = Array.from(formInputs).filter(input => !input.validity.valid);
      invalidInputs.forEach(input => {
        input.classList.add('is-invalid');
      });
      const validInputs = Array.from(formInputs).filter(input => input.validity.valid);
      validInputs.forEach(input => {
        input.classList.remove('is-invalid');
      });
      invalidInputs[0].focus();
    },

    async saveClient() {
      this.savedComponentCount = 0;

      if (!this.clientId) {
        try {
          const data = {
            client_type: this.clientType,
            company: this.company,
          }
          const response = await this.$http.post(this.urls.clientCreateUrl, data)
          this.clientId = response.data.id;
          this.urls.clientUpdateUrl = response.data.url;
        } catch (error) {
          console.error(error);
        }
      } else {
        this.expectedComponentCount += 1;
        this.save();
      }
      if (this.clientId !== null) {
        this.save();
        this.$refs.invoiceForm.save(this.urls.clientUpdateUrl);
        if (this.isCompany) {
          this.$refs.companyForm.save(this.urls.clientUpdateUrl);
        } else {
          this.$refs.personForm.save(this.urls.clientUpdateUrl);
        }
      }
    },
    save() {
      const data = {
        company: this.company,
      }
      this.$http.patch(this.urls.clientUpdateUrl, data).then(() => {
        this.handleComponentSaved();
      }).catch(error => {
        console.error(error);
      });
    },
    slugUpdate(name) {
      if (this.slug === "") {
        this.slug = name;
      }
    },
  },
  mounted() {
    this.$i18n.locale = this.$el.parentNode.dataset.languageCode;
    this.defaultLanguage = this.$el.parentNode.dataset.languageCode;
    this.urls.clientCreateUrl = this.$el.parentNode.dataset.clientCreateUrl;
    this.urls.clientUpdateUrl = this.$el.parentNode.dataset.clientUpdateUrl;
    this.urls.clientRedirectUrl = this.$el.parentNode.dataset.clientRedirectUrl;
    this.urls.companiesUrl = this.$el.parentNode.dataset.companiesUrl;
    this.clientId = this.$el.parentNode.dataset.clientId;

    this.$http.get(this.urls.companiesUrl).then(response => {
      this.companies = response.data.results;
      if (this.companies.length === 1) {
        this.company = this.companies[0].id
      }
    }).catch(error => {
      console.error(error);
    });

    if (this.urls.clientUpdateUrl) {
      this.$http.get(this.urls.clientUpdateUrl).then(response => {
        this.client = response.data;
        this.clientType = this.client.client_type;
        this.company = this.client.company;
        this.selectedCompany = this.companies.find(company => company.id === this.company);
        this.slug = this.client.slug;
        this.$refs.companyForm.setClient(this.client);
        this.$refs.invoiceForm.setClient(this.client);
        this.$refs.personForm.setClient(this.client);
      }).catch(error => {
        console.error(error);
      });
    }
  },
  watch:{
    company(companyId) {
      this.selectedCompany = this.companies.find(company => company.id === companyId);
      if (this.selectedCompany !== undefined) {
        this.vatEnabled = this.selectedCompany.enable_vat;
        this.vatRate = this.selectedCompany.vat_rate;
      }
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
</style>
