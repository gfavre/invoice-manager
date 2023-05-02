<template>
  <fieldset class="border-left-info shadow">
    <legend>Étape 1</legend>
    <p class="lead">Configurer les informations de contact de votre entreprise</p>
    <company-search
            autocompleteUrl="/api/companies-search/"
            companyDetailUrl="/api/company-detail/"
            :placeholder="$t('Search on company register')"
            @callback="companyDetailLookupResult"></company-search>

    <CompanyForm ref="companyForm"
                 :company="company"
                 @update:company="updateCompany"
    />
  </fieldset>
  <fieldset class="border-left-warning shadow">
    <legend>Étape 2</legend>
    <p class="lead">Configurez vos informations bancaires pour recevoir les paiements</p>
    <BankingForm ref="bankingForm"
                 :company="company"
                 :ibanUrl="urls.ibanUrl"
                 @update:company="updateCompany"
    />
  </fieldset>
  <fieldset>
    <legend>Étape 3</legend>
    <p class="lead">Configurer l'aspect des factures</p>
    <InvoiceSettingsForm ref="invoiceSettingsForm"
                         company="company"
                         @update:company="updateCompany"

    />
  </fieldset>

  <pre>
  {{ company }}
    {{ urls }}
  </pre>
</template>

<script>
import CompanyForm from './components/CompanyForm.vue'
import {useI18n} from 'vue-i18n'
//import CompanySearch from "@/../../../clients/clients_app/src/components/CompanySearch.vue";
import CompanySearch from "@/components/CompanySearch.vue";
import BankingForm from "@/components/BankingForm.vue";
import InvoiceSettingsForm from "@/components/InvoiceSettingsForm.vue";

export default {
  name: 'App',
  components: {
    InvoiceSettingsForm,
    CompanySearch,
    CompanyForm,
    BankingForm,
  },
  data() {
    return {
      searchTerm: '',
      company: {
        name: 'test',
        address: 'rue ',
        zipcode: '1272',
        city: 'Genolier',
        country: 'CH',
        phone: '0795990906',
        additionalPhone: '',
        email: '',
        website: '',

        vatId: '',
        iban: 'CH37 0900 0000 1481 6523 4',
        nameForBank: '',
        bank: '',
        swift: '',
      },
      urls: {
        companiesUrl: '',
        ibanUrl: '',
      }
    }
  },
  methods: {
    companyDetailLookupResult(company) {
      this.company.name = company.name;
      this.company.address = company.address;
      this.company.country = company.country;
      this.company.city = company.city;
      this.company.zipcode = company.zip_code;
      this.company.vatId = company.vat_id;
      this.$refs.companyForm.updateCompany();
      this.$refs.bankingForm.updateCompany();

    },
    updateCompany({field, value}) {
      this.company[field] = value
    }
  },
  mounted() {
    const mainAppNode = this.$root.$el.parentElement;
    this.urls.companiesUrl = mainAppNode.getAttribute('data-companies-url');
    this.urls.ibanUrl = mainAppNode.getAttribute('data-iban-url');
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
input::placeholder {
  color: #aaaaaa !important;
}
</style>
