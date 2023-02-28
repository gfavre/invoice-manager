<template>
  <div class="form-row ">
    <div class="col-md ">
      <div id="div_id_currency" class="form-group">
        <label for="id_currency" class=" requiredField">Devise<span class="asteriskField">*</span></label>
        <select name="currency" class="select custom-select" id="id_currency"
                v-model="currency"
        >
          <option v-for="curr in currencies" :key="curr.value" :value="curr.value">{{ curr.text }}</option>
        </select>
      </div>
    </div>
    <div class="col-md ">
      <div id="div_id_vat_rate" class="form-group">
        <label for="id_vat_rate" class="">Taux de TVA</label>
        <input type="number" name="vat_rate" step="0.0001"
               class="numberinput form-control" id="id_vat_rate"
               v-model="vat_rate"
        >
      </div>
    </div>
    <div class="col-md ">
      <div id="div_id_default_hourly_rate" class="form-group">
        <label for="id_default_hourly_rate" class=" requiredField">
          Tarif horaire par défaut<span class="asteriskField">*</span>
        </label>
        <input type="number" name="default_hourly_rate" value="0.00" step="0.01"
               class="numberinput form-control" required="" id="id_default_hourly_rate">
      </div>
    </div>
  </div>
  <div id="div_id_language" class="form-group">
    <label for="id_language" class=" requiredField">Langue<span class="asteriskField">*</span></label>
    <select name="language" class="select custom-select" id="id_language"
            v-model="language">
      <option v-for="lang in languages" :key="lang.value" :value="lang.value">{{ lang.text }}</option>
    </select>
  </div>
  <div id="div_id_payment_delay_days" class="form-group">
    <label for="id_payment_delay_days" class=" requiredField">
      Délai de paiement<span class="asteriskField">*</span>
    </label>
    <input type="number" name="payment_delay_days" class="numberinput form-control"
           required="" id="id_payment_delay_days"
           v-model="paymentDelayDays"
    >
    <small id="hint_id_payment_delay_days" class="form-text text-muted">
      Délai par défaut en jours jusqu'à la date d'échéance
    </small>
  </div>
  <hr>

  <div class="form-row ">
    <div class="col-md ">
      <label for="exampleInvoiceCode">Prochain code de facture</label>
      <p class="form-control-static" id="exampleInvoiceCode" v-if="slug">
        {{ slug }}-{{ invoiceCurrentCount + 1 }}
      </p>
      <p v-else>n/a</p>
    </div>
    <div class="col-md ">
      <div id="div_id_slug" class="form-group">
        <label for="id_slug" class=" requiredField">
          Slug<span class="asteriskField">*</span>
        </label>
        <input type="text" name="slug" maxlength="15" class="textinput textInput form-control"
               required="" id="id_slug"
               v-model="slug">
        <small id="hint_id_slug" class="form-text text-muted">
          Utilisé pour générer le code de la facture
        </small>
      </div>
    </div>
    <div class="col-md ">
      <div id="div_id_invoice_current_count" class="form-group">
        <label for="id_invoice_current_count" class=" requiredField">
          Décompte actuel de factures<span class="asteriskField">*</span>
        </label>
        <input type="number" name="invoice_current_count"
               class="numberinput form-control" required="" id="id_invoice_current_count"
               v-model="invoiceCurrentCount"
        >
        <small id="hint_id_invoice_current_count" class="form-text text-muted">
          Utilisé pour générer le code de la facture</small>
      </div>
    </div>
  </div>
</template>

<script>
import slugify from "slugify";
export default {
  name: "InvoiceForm.vue",
  data() {
    return {
      currency: 'CHF',
      invoiceCurrentCount: 0,
      language: 'fr',
      paymentDelayDays: 30,
      slug: '',
      vat_rate: 0.077,
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
    setClient(client){
      this.currency = client.currency;
      this.invoiceCurrentCount = client.invoice_current_count;
      this.language = client.language;
      this.paymentDelayDays = client.payment_delay_days;
      this.slug = client.slug;
      this.vat_rate = client.vat_rate;
    },
    save(clientId) {
      this.$http.patch(`/api/clients/${clientId}/`, {
        currency: this.currency,
        invoice_current_count: this.invoiceCurrentCount,
        language: this.language,
        payment_delay_days: this.paymentDelayDays,
        slug: this.slug,
        vat_rate: this.vat_rate,
      }).then(response => {
        this.$emit('company-saved', response.data)
      })
    },
    slugUpdate(name) {
      this.slug = slugify(name, {
        lower: true, // convert to lowercase
        strict: true // remove special characters
      });
    },
  },
  props: {
    defaultLanguage: {
      type: String,
      default: 'fr',
      required: false,
    },
  }
}
</script>

<style scoped>

</style>
