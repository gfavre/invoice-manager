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
    <div>
      <input type="text" name="company_name" maxlength="255"
             class="textinput textInput form-control" id="id_company_name" required=""
             v-model="name"/>

    </div>
  </div>
  <div id="div_id_address" class="form-group">
    <label for="id_address" class="">
      Adresse
    </label>
    <textarea name="address" cols="40" rows="2" class="textarea form-control" id="id_address"
              v-model="address"
    ></textarea>
  </div>
  <div class="form-row ">
    <div class="col-md-4">
      <div id="div_id_country" class="form-group"><label for="id_country" class="">
        Pays
      </label>
        <div>
          <country-select v-model="country" :country="country" topCountry="CH" :autocomplete="true"
                          class-name="form-control"/>


        </div>
      </div>
    </div>
    <div class="col-md-2">
      <div id="div_id_zip_code" class="form-group"><label for="id_zip_code" class="">
        Code postal
      </label>
        <div>
          <div class="input-group">
            <input type="text" name="zip_code" maxlength="10" class="textinput textInput form-control"
                   id="id_zip_code"
                   @input="onZipcodeInput" v-model="zipcode">
            <ul class="dropdown-menu  shadow" :class="{show: isCitiesDropdownVisible}" ref="dropdown">
              <li v-for="city in cities" :key="city">
                <a class="dropdown-item" @click="onCitySelected(city)">{{ city }}</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="col-md ">
      <div id="div_id_city" class="form-group">
        <label for="id_city">
          Localité
        </label>
        <div>
          <input type="text" name="city" maxlength="255" class="textinput textInput form-control" id="id_city"
                 v-model="city">
        </div>
      </div>
    </div>
  </div>
  <hr>
  <div class="form-row ">
    <div class="col-md ">
      <div id="div_id_contact_first_name" class="form-group"><label for="id_contact_first_name" class="">
        Prénom du contact
      </label>
        <div>
          <input type="text" name="contact_first_name" maxlength="255"
                 class="textinput textInput form-control" id="id_contact_first_name"
                v-model="contactFirstName" ref="contactFirstName"
          />
        </div>
      </div>
    </div>
    <div class="col-md ">
      <div id="div_id_contact_last_name" class="form-group">
        <label for="id_contact_last_name">
          Nom du contact
        </label>
        <div>
          <input type="text" name="contact_last_name" maxlength="255"
                 class="textinput textInput form-control" id="id_contact_last_name"
                 v-model="contactLastName"
          />
        </div>
      </div>
    </div>
  </div>
  <div id="div_id_contact_email" class="form-group">
    <label for="id_contact_email" class="">
      E-mail de contact
    </label>
    <div>
      <input type="email" name="contact_email" maxlength="254"
             class="emailinput form-control" id="id_contact_email"
             v-model="contactEmail"
      />
    </div>
  </div>
</template>

<script>
import {CountrySelect} from 'vue3-country-region-select'
//import { search, validate, cityFromZip, allZips } from 'swiss-zipcodes'
import {cityFromZip} from "swiss-zipcodes";
import CompanySearch from "./CompanySearch.vue";

export default {
  name: "CompanyForm",
  components: {
    CompanySearch,
    CountrySelect,
  },
  computed: {
    isCitiesDropdownVisible() {
      return this.cities.length > 0;
    },
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
    onZipcodeInput() {
      if (this.city !== '') {
        return;
      }

      if (this.zipcode.length < 3) {
        return;
      }
      this.cities = cityFromZip(this.zipcode);
      if (this.cities.length === 1) {
        this.city = this.cities[0];
        this.cities = [];
      }
    },
    onCitySelected(city) {
      this.city = city;
      this.cities = [];
    },
    onWindowClick(event) {
      if (this.$refs.dropdown && !this.$refs.dropdown.contains(event.target)) {
        this.cities = [];
      }
    },
  },
  mounted() {
    window.addEventListener('click', this.onWindowClick);
  },
  beforeUnmount() {
    window.removeEventListener('click', this.onWindowClick);
  },

}
</script>

<style scoped>

</style>
