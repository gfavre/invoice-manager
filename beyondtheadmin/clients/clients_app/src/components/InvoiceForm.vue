<template>
  <div class="form-row ">
    <div class="col-md ">
      <div id="div_id_currency" class="form-group">
        <label for="id_currency" class=" requiredField">{{ $t('Currency') }}<span class="asteriskField">*</span></label>
        <select name="currency" class="select custom-select" id="id_currency"
                v-model="currency"
        >
          <option v-for="curr in currencies" :key="curr.value" :value="curr.value">{{ curr.text }}</option>
        </select>
      </div>
    </div>
    <div class="col-md ">
      <div id="div_id_vat_rate" class="form-group">
        <label for="id_vat_rate" class="">{{ $t('VAT rate') }}</label>
        <input type="number" name="vat_rate" step="0.0001"
               class="numberinput form-control" id="id_vat_rate"
               v-model.number="vatRate"
        >
      </div>
    </div>
    <div class="col-md ">
      <div id="div_id_default_hourly_rate" class="form-group">
        <label for="id_default_hourly_rate" class=" requiredField">
          {{ $t('Default hourly rate') }}<span class="asteriskField">*</span>
        </label>
        <input type="number" name="default_hourly_rate" step="0.01"
               class="numberinput form-control" required="" id="id_default_hourly_rate"
               v-model.number="defaultHourlyRate"
        >
      </div>
    </div>
  </div>
  <div id="div_id_language" class="form-group">
    <label for="id_language" class=" requiredField">{{ $t('Language') }}<span class="asteriskField">*</span></label>
    <select name="language" class="select custom-select" id="id_language"
            v-model="language">
      <option v-for="lang in languages" :key="lang.value" :value="lang.value">{{ lang.text }}</option>
    </select>
  </div>
  <div id="div_id_payment_delay_days" class="form-group">
    <label for="id_payment_delay_days" class=" requiredField">
      {{ $t('Payment delay') }}<span class="asteriskField">*</span>
    </label>
    <input type="number" name="payment_delay_days" class="numberinput form-control"
           required="" id="id_payment_delay_days"
           v-model="paymentDelayDays"
    >
    <small id="hint_id_payment_delay_days" class="form-text text-muted">
      {{ $t('Default delay in days to due date') }}
    </small>
  </div>
  <hr>

  <div class="form-row ">
    <div class="col-md ">
      <label for="exampleInvoiceCode">{{ $t('Next invoice code') }}</label>
      <p class="form-control-static" id="exampleInvoiceCode" v-if="slug">
        {{ slug }}-{{ invoiceCurrentCount + 1 }}
      </p>
      <p v-else>n/a</p>
    </div>
    <div class="col-md ">
      <div id="div_id_slug" class="form-group">
        <label for="id_slug" class=" requiredField">
          {{ $t('Slug') }}<span class="asteriskField">*</span>
        </label>
        <input type="text" name="slug" maxlength="15" class="textinput textInput form-control"
               required="" id="id_slug"
               v-model="slug">
        <small id="hint_id_slug" class="form-text text-muted">
          {{ $t("Used to generate invoice code") }}
        </small>
      </div>
    </div>
    <div class="col-md ">
      <div id="div_id_invoice_current_count" class="form-group">
        <label for="id_invoice_current_count" class=" requiredField">
          {{ $t("Current count of invoices") }}<span class="asteriskField">*</span>
        </label>
        <input type="number" name="invoice_current_count"
               class="numberinput form-control" required="" id="id_invoice_current_count"
               v-model="invoiceCurrentCount"
        >
        <small id="hint_id_invoice_current_count" class="form-text text-muted">
          {{ $t("Used to generate invoice code") }}</small>
      </div>
    </div>
  </div>
</template>

<script>
'use strict';

import slugify from "slugify";
import { useI18n } from 'vue-i18n';


export default {
  name: "InvoiceForm.vue",
  data() {
    return {
      currency: 'CHF',
      defaultHourlyRate: 0.0,
      invoiceCurrentCount: 0,
      language: 'fr',
      paymentDelayDays: 30,
      slug: '',
      vatRate: 0.077,
      currencies: [
        {value: 'CHF', text: 'CHF'},
        {value: 'EUR', text: 'Euro'},
      ],
      languages: [
        {value: 'en', text: 'English'},
        {value: 'de', text: 'Deutsch'},
        {value: 'fr', text: 'Français'},
        {value: 'it', text: 'Italiano'},
      ],
    }
  },
  methods: {
    isFormComplete(){
      return this.currency && this.validateNumberInput(this.defaultHourlyRate) &&
          this.language && this.paymentDelayDays !== "" && this.slug &&
          this.validateNumberInput(this.vatRate);
    },
    setClient(client){
      this.currency = client.currency;
      this.invoiceCurrentCount = client.invoice_current_count;
      this.language = client.language;
      this.paymentDelayDays = client.payment_delay_days;
      this.slug = client.slug;
      this.vatRate = client.vat_rate;
      this.defaultHourlyRate = client.default_hourly_rate;
    },
    save() {
      this.$http.patch(this.clientUpdateUrl, {
        currency: this.currency,
        invoice_current_count: this.invoiceCurrentCount,
        language: this.language,
        default_hourly_rate: this.defaultHourlyRate,
        payment_delay_days: this.paymentDelayDays,
        slug: this.slug,
        vat_rate: this.vatRate,
      }).then(response => {
        this.$emit('saved', response.data)
      }).catch(error => {
        console.error(error)
      });
    },
    validateNumberInput(value) {
       return !isNaN(value) && value !== null && value !== '';
    },
    limitSlugify(text){
      const slug = slugify(text, { lower: true, remove: /[*+~.()'"!:@]/g });
      // Check if the slug is longer than 15 characters
      if (slug.length > 15) {
        // Find the first dash (-) in the slug
        const dashIndex = slug.indexOf('-');
        if (dashIndex > 0 && dashIndex <= 15) {
          // If there is a dash before the 15th character, cut the slug there
          return slug.slice(0, dashIndex);
        } else {
          // Otherwise, cut the slug at the 15th character
          return slug.slice(0, 15);
        }
      } else {
        // If the slug is 15 characters or fewer, return it as is
        return slug;
      }
    }
  },
  props: {
    updatedSlug: {
      type: String,
      default: '',
    },
    clientUpdateUrl: String,
  },
  setup(){
    const { t } = useI18n();
    return { t }
  },
  watch: {
    updatedSlug: function (newSlug) {
      this.slug = this.limitSlugify(newSlug);
    }
  }

}
</script>

<style scoped>

</style>
