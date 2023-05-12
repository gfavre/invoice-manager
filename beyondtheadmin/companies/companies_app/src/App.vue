<template>
  <fieldset class="border-left-info shadow" v-if="stepIndex === 1">
    <legend>Étape 1</legend>
    <p class="lead">Configurer les informations de contact de votre entreprise</p>
    <company-search
            autocompleteUrl="/api/companies-search/"
            companyDetailUrl="/api/company-detail/"
            :placeholder="$t('Search on company register')"
            @callback="companyDetailLookupResult"></company-search>

    <CompanyForm ref="companyForm"
                 :company="company"
                 @next="nextStep"
                 @update="onCompanyUpdate"
    />
  </fieldset>
  <fieldset class="border-left-warning shadow" v-if="stepIndex === 2">
    <legend>Étape 2</legend>
    <p class="lead">Configurez vos informations bancaires pour recevoir les paiements</p>
    <BankingForm ref="bankingForm"
                 :company="company"
                 :ibanUrl="urls.ibanUrl"
                 @next="nextStep"
                 @prev="previousStep"
                 @update="onCompanyUpdate"
    />
  </fieldset>
  <fieldset  class="border-left-primary shadow" v-if="stepIndex === 3">
    <legend>Étape 3</legend>
    <p class="lead">Configurer l'aspect des factures</p>
    <InvoiceSettingsForm ref="invoiceSettingsForm"
                         :company="company"
                         :update-logo-url="urls.updateLogoUrl"
                         :update-signature-image-url="urls.updateSignatureImageUrl"
                         @next="nextStep"
                         @prev="previousStep"
                         @submit="submit"
                         @update:company="onCompanyUpdate"

    />
  </fieldset>
</template>

<script>
import CompanyForm from './components/CompanyForm.vue'
import {useI18n} from 'vue-i18n'
import CompanySearch from "@/components/CompanySearch.vue";
import BankingForm from "@/components/BankingForm.vue";
import InvoiceSettingsForm from "@/components/InvoiceSettingsForm.vue";

const localToServerFieldMapping = {
        "zipCode": "zip_code",
        "additionalPhone": "additional_phone",
        "vatId": "vat_id",
        "nameForBank": "name_for_bank",
        "swift": "bic",
        "contrastColor": "contrast_color",
        "invoiceNote": "invoice_note",
        "signatureText": "signature_text",
        "signatureImage": "signature_image",
        "thanksMessage": "thanks",
        "emailSignature": "email_signature",
        "fromEmail": "from_email",
        "bccEmail": "bcc_email",
      };
const ServerToLocalFieldMapping = {};
for (const [key, value] of Object.entries(localToServerFieldMapping)) {
  ServerToLocalFieldMapping[value] = key;
}

export default {
  name: 'App',
  components: {
    CompanySearch,
    CompanyForm,
    BankingForm,
    InvoiceSettingsForm,
  },
  data() {
    return {
      searchTerm: '',
      stepIndex: 1,

      company: {
        id: '',
        name: '',
        address: '',
        zipCode: '',
        city: '',
        country: '',
        phone: '',
        additionalPhone: '',
        email: '',
        website: '',

        vatId: '',
        iban: '',
        nameForBank: '',
        bank: '',
        swift: '',

        logo: '',
        contrastColor: '#000000',
        invoiceNote: '',
        signatureText: '',
        signatureImage: '',
        thanksMessage: '',

        emailSignature: '',
        fromEmail: '',
        bccEmail: '',
      },
      urls: {
        companiesUrl: '',
        companyUpdateUrl: '',
        ibanUrl: '',
        successUrl: '',
        updateLogoUrl: '',
        updateSignatureImageUrl: '',
      }
    }
  },
  methods: {
    companyDetailLookupResult(company) {
      this.company.name = company.name;
      this.company.address = company.address;
      this.company.country = company.country;
      this.company.city = company.city;
      this.company.zipCode = company.zip_code;
      this.company.vatId = company.vat_id;
      this.$refs.companyForm.setCompany(this.company);
      this.$refs.bankingForm.setCompany(this.company);
    },
    nextStep() {
      this.stepIndex += 1;
    },
    previousStep() {
      this.stepIndex -= 1;
    },
    submit() {
      window.location.href = this.urls.successUrl;
    },
    onCompanyUpdate(fields) {
      console.log("app is receiving update")
      console.log(fields)
      let serverFields = {};
      for (const [field, value] of Object.entries(fields)) {
        this.company[field] = value; // update locally (for instant feedback, will be overwritten by server response)
        serverFields[localToServerFieldMapping[field] || field] = value // prepare server value
      }
      const url = this.company.id ? this.urls.companyUpdateUrl : this.urls.companiesUrl;

      const httpMethod = this.company.id ? 'patch' : 'post';
      this.$http[httpMethod](url, serverFields)
        .then(response => {
          this.setCompany(response.data)
        })
      .catch(error => {
        // Handle the error
        console.error('Error:', error);
        // ... handle the error in a consistent manner ...
      });
    },
    cleanCompany(companyServerData) {
      return Object.fromEntries(
        Object.entries(companyServerData).map(([key, value]) => [ServerToLocalFieldMapping[key] || key, value])
      )
    },
    setCompany(companyServerData) {
      this.urls.companyUpdateUrl = this.urls.companiesUrl + companyServerData.id + '/';
      this.company = this.cleanCompany(companyServerData);
    },
    loadCompany(){
      this.$http.get(this.urls.companyUpdateUrl).then(response => {
        const company = response.data;
        this.setCompany(company)
        this.$refs.companyForm.setCompany(this.company);
      }).catch(error => {
        console.log(error)
      });
    },
    saveCompany() {
      console.log("saving company")
      console.log(this.company)
    }
  },
  mounted() {
    const mainAppNode = this.$root.$el.parentElement;
    this.urls.companiesUrl = mainAppNode.getAttribute('data-companies-url');
    this.urls.ibanUrl = mainAppNode.getAttribute('data-iban-url');
    this.urls.companyUpdateUrl = mainAppNode.getAttribute('data-company-update-url');
    this.urls.successUrl = mainAppNode.getAttribute('data-success-url');
    if (this.urls.companyUpdateUrl) {
      this.urls.updateLogoUrl = this.urls.companyUpdateUrl + 'update_logo/';
      this.urls.updateSignatureImageUrl = this.urls.companyUpdateUrl + 'update_signature_image/';
      this.loadCompany();
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
input::placeholder {
  color: #aaaaaa !important;
}
</style>
