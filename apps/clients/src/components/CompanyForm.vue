<template>
  <company-search append="toto" placeholder="company lookup"
                  autocompleteUrl="http://127.0.0.1:8000/api/companies/"
                  companyDetailUrl="http://127.0.0.1:8000/api/company-detail/"
                  @callback="companyDetailLookupResult"></company-search>


  <div id="div_id_company_name" class="form-group">
    <label for="id_company_name" class="requiredField">
      Nom de l'entreprise
      <span class="asteriskField">*</span>
    </label>
    <input type="text" name="company_name" maxlength="255"
           class="textinput textInput form-control" id="id_company_name" required=""
           v-model="name"/>

  </div>
  <div id="div_id_address" class="form-group">
    <label for="id_address">Adresse</label>
    <textarea name="address" cols="40" rows="2" class="textarea form-control" id="id_address"
              v-model="address"
    ></textarea>
  </div>
  <div class="form-row">
    <city-auto-complete></city-auto-complete>
  </div>
  <div id="div_id_country" class="form-group">
    <label for="id_country">Pays</label>
    <country-select v-model="country" :country="country" topCountry="CH" :autocomplete="true"
                    class-name="form-control"/>
  </div>
  <hr>
  <div class="form-row ">
    <div class="col-md ">
      <div id="div_id_contact_first_name" class="form-group">
        <label for="id_contact_first_name">Prénom du contact</label>
        <input type="text" name="contact_first_name" maxlength="255"
                 class="textinput textInput form-control" id="id_contact_first_name"
                v-model="contactFirstName" ref="contactFirstName"
          />
      </div>
    </div>
    <div class="col-md ">
      <div id="div_id_contact_last_name" class="form-group">
        <label for="id_contact_last_name">Nom du contact</label>
        <input type="text" name="contact_last_name" maxlength="255"
               class="textinput textInput form-control" id="id_contact_last_name"
               v-model="contactLastName"
        />
      </div>
    </div>
  </div>
  <div id="div_id_contact_email" class="form-group">
    <label for="id_contact_email">E-mail de contact</label>
    <input type="email" name="contact_email" maxlength="254"
           class="emailinput form-control" id="id_contact_email"
           v-model="contactEmail"
    />
  </div>
</template>

<script>
import {CountrySelect} from 'vue3-country-region-select'
import CityAutoComplete from "@/components/CityAutoComplete.vue";
import CompanySearch from "@/components/CompanySearch.vue";

export default {
  name: "CompanyForm",
  components: {
    CompanySearch,
    CountrySelect,
    CityAutoComplete,
  },

  data() {
    return {
      name: "",
      address: "",
      country: "CH",
      zipcode: "",
      cities: [],
      city: "",
      contactFirstName: "",
      contactLastName: "",
      contactEmail: "",
    };
  },
  methods: {
    companyDetailLookupResult(company) {
      this.name = company.name;
      this.address = company.address;
      this.country = company.country;
      this.city = company.city;
      this.zipcode = company.zip_code;
      this.$refs.contactFirstName.focus();
    },
    onSelect(country) {
      console.log(country);
      // Check the country object example below.
    },

  },


}
</script>

<style scoped>

</style>
