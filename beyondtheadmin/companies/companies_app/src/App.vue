<template>

  <div class="card-header border-bottom">
    <!-- Wizard navigation-->
    <div class="nav nav-pills nav-justified flex-column flex-xl-row nav-wizard" id="wizard-steps" role="tablist">
      <!-- Wizard navigation item 1-->

      <!-- find a way to add aria-selected="true" -->
      <a class="nav-item nav-link" href="#wizard1" data-bs-toggle="tab" role="tab"
         aria-controls="wizard1"
         :class="{'active': stepIndex === 1}" @click="stepIndex=1">
        <div class="wizard-step-icon">1</div>
        <div class="wizard-step-text">
          <div class="wizard-step-text-name">{{ $t("Company") }}</div>
          <div class="wizard-step-text-details">{{ $t("Contact informations") }}</div>
        </div>
      </a>
      <!-- Wizard navigation item 2-->
      <a class="nav-item nav-link" id="wizard2-tab" href="#wizard2" data-bs-toggle="tab" role="tab"
         aria-controls="wizard2"
         :class="{'active': stepIndex === 2, disabled: !stepsFinished[1]}" @click="stepIndex=2">
        <div class="wizard-step-icon">2</div>
        <div class="wizard-step-text">
          <div class="wizard-step-text-name">{{ $t("Payment") }}</div>
          <div class="wizard-step-text-details">{{ $t("How you will get paid") }}</div>
        </div>
      </a>
      <!-- Wizard navigation item 3-->
      <a class="nav-item nav-link" id="wizard3-tab" href="#wizard3" data-bs-toggle="tab" role="tab"
         aria-controls="wizard3"
         :class="{'active': stepIndex === 3, disabled: !stepsFinished[2]}" @click="stepIndex=3">
        <div class="wizard-step-icon">3</div>
        <div class="wizard-step-text">
          <div class="wizard-step-text-name">{{ $t("Invoices") }}</div>
          <div class="wizard-step-text-details">{{ $t("What invoices will look like") }}</div>
        </div>
      </a>

       <a class="nav-item nav-link" id="wizard3-tab" href="#wizard4" data-bs-toggle="tab" role="tab"
         aria-controls="wizard3"
         :class="{'active': stepIndex === 4, disabled: !stepsFinished[3]}" @click="stepIndex=4">
        <div class="wizard-step-icon">4</div>
        <div class="wizard-step-text">
          <div class="wizard-step-text-name">{{ $t("Emails") }}</div>
          <div class="wizard-step-text-details">{{ $t("How are the invoices sent") }}</div>
        </div>
      </a>


    </div>
  </div>

  <fieldset class="border-left-info shadow" v-if="stepIndex === 1">
    <legend>{{ $t("Step 1") }}</legend>
    <p class="lead">{{ $t("Setup your company's contact informations") }}</p>
    <div class="form-group">
      <company-search
          autocompleteUrl="/api/companies-search/"
          companyDetailUrl="/api/company-detail/"
          :placeholder="$t('Search on company register')"
          @callback="companyDetailLookupResult"></company-search>
    </div>
    <CompanyForm ref="companyForm"
                 :company="company"
                 @next="nextStep"
                 @update="onCompanyUpdate"
    />
  </fieldset>
  <fieldset class="border-left-warning shadow" v-if="stepIndex === 2">
    <legend>{{ $t("Step 2") }}</legend>
    <p class="lead">{{ $t("Setup your payment and banking informations") }}</p>
    <BankingForm ref="bankingForm"
                 :company="company"
                 :ibanUrl="urls.ibanUrl"
                 @prev="previousStep"
                 @next="nextStep"
                 @update="onCompanyUpdate"
    />
  </fieldset>
  <fieldset class="border-left-primary shadow" v-if="stepIndex === 3">
    <legend>{{ $t("Step 3") }}</legend>
    <p class="lead">{{ $t("Setup the invoices' look and feel") }}</p>
    <InvoiceSettingsForm ref="invoiceSettingsForm"
                         :company="company"
                         :update-logo-url="urls.updateLogoUrl"
                         :update-signature-image-url="urls.updateSignatureImageUrl"
                         @prev="previousStep"
                         @next="nextStep"
                         @update="onCompanyUpdate"
    />
  </fieldset>

    <fieldset class="border-left-primary shadow" v-if="stepIndex === 4">
    <legend>{{ $t("Step 4") }}</legend>
    <p class="lead">{{ $t("Setup the email used to send invoices") }}</p>
    <InvoiceEmailForm ref="invoiceEmailForm"
                         :company="company"
                         @prev="previousStep"
                         @submit="submit"
                         @update="onCompanyUpdate"
    />
  </fieldset>

</template>

<script>

/* How does this thing work?
1. The main app.vue includes 4 components: CompanyForm, BankingForm, InvoiceSettingsForm, InvoiceEmailForm for
the for steps of the wizard. Actions on one component do not touch data for other components at the exception to
search company (see 4.)

2. In the mounted() section of the app.vue, the company object is initialized with the data from the server. The
incoming data is mapped to the local company object using the localToServerFieldMapping object (mostly because
the python serializers outputs snake_case whereas JS is more friendly with camelCase).

3. When the user hits a next/prev button, the component calls a callback function via @update (function is named
onCompanyUpdate here). The component will then fire a prev/next event, which modifies the stepIndex.

4. Selecting a company in the search box will trigger the update of the company object and its transmission to
components via the setCompany method.
 */

import CompanyForm from './components/CompanyForm.vue'
import {useI18n} from 'vue-i18n'
import CompanySearch from "@/components/CompanySearch.vue";
import BankingForm from "@/components/BankingForm.vue";
import InvoiceSettingsForm from "@/components/InvoiceSettingsForm.vue";
import InvoiceEmailForm from "@/components/InvoiceEmailForm.vue";

const localToServerFieldMapping = {
  "zipCode": "zip_code",
  "additionalPhone": "additional_phone",

  "vatEnabled": "enable_vat",
  "vatId": "vat_id",
  "vatRate": "vat_rate",

  "hourlyRate": "default_hourly_rate",
  "paymentDelay": "payment_delay_days",

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
    InvoiceEmailForm,
  },
  data() {
    return {
      searchTerm: '',
      stepIndex: 1,
      stepsFinished: [false, false, false, false],
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
        vatEnabled: true,
        vatRate: 0.077,

        hourlyRate: 0.0,
        paymentDelay: 30,

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
      userEmail: '',
      userName: '',
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
      /* This method is called when the user selects a company from the search results, to update our local fields */
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
      this.stepsFinished[this.stepIndex] = true;
      this.stepIndex += 1;
    },
    previousStep() {
      this.stepIndex -= 1;
    },
    submit() {
      this.stepsFinished[3] = true;
      window.location.href = this.urls.successUrl;
    },
    onCompanyUpdate(fields) {
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
          console.error('Error:', error);
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
      this.company.fromEmail = this.defaultFromEmail;
    },
    loadCompany() {
      this.$http.get(this.urls.companyUpdateUrl).then(response => {
        const company = response.data;
        this.setCompany(company);
        this.$refs.companyForm.setCompany(this.company);
      }).catch(error => {
        console.log(error)
      });
    },
  },
  computed: {
    defaultFromEmail() {
      if (this.company.fromEmail) {
        return this.company.fromEmail;
      }
      if (this.userName) {
        return `${this.userName} <${this.userEmail}>`;
      }
      return this.userEmail;
    },
  },
  mounted() {
    const mainAppNode = this.$root.$el.parentElement;
    this.$i18n.locale = mainAppNode.getAttribute("data-language-code");

    this.urls.companiesUrl = mainAppNode.getAttribute('data-companies-url');
    this.urls.ibanUrl = mainAppNode.getAttribute('data-iban-url');
    this.urls.companyUpdateUrl = mainAppNode.getAttribute('data-company-update-url');
    this.urls.successUrl = mainAppNode.getAttribute('data-success-url');
    this.userEmail = mainAppNode.getAttribute('data-user-email');
    this.userName = mainAppNode.getAttribute('data-user-name');

    if (this.urls.companyUpdateUrl) {
      this.urls.updateLogoUrl = this.urls.companyUpdateUrl + 'update_logo/';
      this.urls.updateSignatureImageUrl = this.urls.companyUpdateUrl + 'update_signature_image/';
      this.loadCompany();
      this.stepsFinished = [true, true, true, true];
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
