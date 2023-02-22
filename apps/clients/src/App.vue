<template>
  <div id="div_id_client_type" class="form-group">
    <label for="id_client_type_0" class=" requiredField">
      {{ t("Type of client") }}<span class="asteriskField">*</span>
    </label>
    <div>
      <div class="custom-control custom-radio custom-control-inline">
        <input type="radio" class="custom-control-input" name="client_type" value="company"
               id="id_client_type_0" required=""
               v-model="clientType"/>
        <label class="custom-control-label" for="id_client_type_0">
          <i class="bi bi-journal"></i> {{ t("company") }}
        </label>
      </div>
      <div class="custom-control custom-radio custom-control-inline">
        <input type="radio" class="custom-control-input" name="client_type" value="person"
               id="id_client_type_1" required=""
               v-model="clientType"/>
        <label class="custom-control-label" for="id_client_type_1">
          <i class="bi bi-person-fill"></i>
          {{ t("person") }}
        </label>
      </div>
    </div>
  </div>

  <section v-if="clientType=='person'">
    <fieldset class="border-left-primary shadow" id="company_infos">
    <legend class=" mb-1">Personne</legend>
    <person-form></person-form>
    </fieldset>
  </section>

  <section v-else>
    <fieldset class="border-left-primary shadow" id="company_infos">
      <legend class=" mb-1">Entreprise</legend>
      <company-form></company-form>
    </fieldset>
    <dl v-if="selectedCompany != null">
      <dt>The company</dt>
      <dd>{{ selectedCompany }}</dd>
    </dl>
  </section>

  <section>
    <fieldset class="border-left-success shadow ">
      <legend class=" mb-1">Factures</legend>
      <div class="form-row ">
        <div class="col-md ">
          <div id="div_id_currency" class="form-group">
            <label for="id_currency" class=" requiredField">Devise<span class="asteriskField">*</span></label>
            <select name="currency" class="select custom-select" id="id_currency">
              <option value="CHF" selected="">CHF</option>
              <option value="EUR">Euro</option>
            </select>
          </div>
        </div>
        <div class="col-md ">
          <div id="div_id_vat_rate" class="form-group">
            <label for="id_vat_rate" class="">Taux de TVA</label>
            <input type="number" name="vat_rate" value="0.077" step="0.0001"
                   class="numberinput form-control" id="id_vat_rate">
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
        <select name="language" class="select custom-select" id="id_language">
          <option value="en">English</option>
          <option value="de">Deutsch</option>
          <option value="fr" selected="">Français</option>
          <option value="it">Italiano</option>
        </select>
      </div>
      <div id="div_id_payment_delay_days" class="form-group">
        <label for="id_payment_delay_days" class=" requiredField">
          Délai de paiement<span class="asteriskField">*</span>
        </label>
        <input type="number" name="payment_delay_days" value="30" class="numberinput form-control"
               required="" id="id_payment_delay_days">
        <small id="hint_id_payment_delay_days" class="form-text text-muted">
          Délai par défaut en jours jusqu'à la date d'échéance
        </small>
      </div>
      <div class="form-row ">
        <div class="col-md ">
          <div id="div_id_slug" class="form-group">
            <label for="id_slug" class=" requiredField">Slug<span class="asteriskField">*</span></label>
            <input type="text" name="slug" maxlength="15" class="textinput textInput form-control"
                   required="" id="id_slug">
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
            <input type="number" name="invoice_current_count" value="0"
                   class="numberinput form-control" required="" id="id_invoice_current_count">
            <small id="hint_id_invoice_current_count" class="form-text text-muted">
              Utilisé pour générer le code de la facture</small>
          </div>
        </div>
      </div>
    </fieldset>
  </section>

</template>

<script>
import PersonForm from './components/PersonForm.vue';
import CompanyForm from './components/CompanyForm.vue';
//import companySearch from "./components/company-search.vue";

import {useI18n} from 'vue-i18n'


export default {
  name: 'App',
  //i18n,
  components: {
    PersonForm,
    CompanyForm,
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
