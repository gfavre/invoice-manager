<template>
  <div class="form-row ">
    <div class="col-md ">
      <div class="form-group">
        <label for="id_first_name" class="requiredField">{{ $t("First name") }}
          <span class="asteriskField">*</span>
        </label>
        <input type="text" name="first_name" maxlength="255"
               class="textinput textInput form-control" id="id_first_name"
               v-model="firstName" ref="FirstName" required="required"
        />
      </div>
    </div>
    <div class="col-md ">
      <div class="form-group">
        <label for="id_last_name"  class="requiredField">
          {{ $t("Last name") }}
          <span class="asteriskField">*</span>
        </label>
        <input type="text" name="contact_last_name" maxlength="255" required="required"
               class="textinput textInput form-control" id="id_last_name"
               v-model="lastName"
               @blur="nameChanged()"
        />
      </div>
    </div>
  </div>
  <div class="form-group">
    <label for="id_address">{{ $t("Address") }}</label>
    <textarea name="address" cols="40" rows="2" class="textarea form-control" id="id_address"
              v-model="address"
    ></textarea>
  </div>
  <div class="form-row">
    <city-auto-complete v-model:city="city"
                        v-model:zipcode="zipCode"
                        :city-label="$t('City')"
                        :zipcode-label="$t('Postal code')"
    ></city-auto-complete>
  </div>
  <div class="form-group">
    <label for="id_country">Pays</label>
    <country-select v-model="country" :country="country" topCountry="CH" :autocomplete="true"
                    class-name="form-control"/>
  </div>
  <div class="form-group">
    <label for="id__email">E-mail</label>
    <input type="email" name="email" maxlength="254"
           class="emailinput form-control" id="id_email"
           v-model="email"
           :class="{ 'is-invalid': emailError }"
    />
    <div class="invalid-feedback">{{ emailErrorMessage }}</div>
  </div>

</template>

<script>
//import axios from 'axios';
import CityAutoComplete from "@/components/CityAutoComplete.vue";
import {CountrySelect} from 'vue3-country-region-select';
import { useI18n } from 'vue-i18n';

export default {
  name: "PersonForm",
  components: {
    CountrySelect,
    CityAutoComplete,
  },
  data() {
    return {
      'client': {},
      'firstName': '',
      'lastName': '',
      'address': '',
      'country': '',
      'city': '',
      'zipCode': '',
      'email': '',
      'errors': {},
    }
  },
  computed: {
    emailError() {
      return !!this.errors.contact_email;
    },
    emailErrorMessage() {
      return this.errors.contact_email ? this.errors.contact_email[0] : '';
    },
  },
  props: {
    clientUpdateUrl: String,
  },
  methods: {
    isFormComplete(){
      return this.firstName.length > 0 && this.lastName.length > 0;
    },
    nameChanged(){
      this.$emit('update:lastName', this.lastName)
    },
    setClient(client) {
      this.client = client;
      this.firstName = client.contact_first_name;
      this.lastName = client.contact_last_name;
      this.address = client.address;
      this.country = client.country;
      this.city = client.city;
      this.zipCode = client.zip_code;
      this.email = client.contact_email;
    },
    save() {
      this.errors = {};
      this.$http.patch(this.clientUpdateUrl, {
        contact_first_name: this.firstName,
        contact_last_name: this.lastName,
        contact_email: this.email,
        address: this.address,
        city: this.city,
        zip_code: this.zipCode,
        country: this.country,
        client_type: 'person',
      }).then(response => {
        this.$emit('saved', response.data)
      }).catch(error => {
        if (error.response && error.response.data) {
            this.errors = error.response.data;
          } else {
            console.error(error);
          }
      })
    },
  },
  setup(){
    const { t } = useI18n();
    return { t }
  }
}
</script>

<style scoped>

</style>
