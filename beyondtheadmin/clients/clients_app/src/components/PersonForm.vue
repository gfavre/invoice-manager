<template>
  <div class="form-row ">
    <div class="col-md ">
      <div class="form-group">
        <label for="id_first_name">Prénom du contact</label>
        <input type="text" name="first_name" maxlength="255"
               class="textinput textInput form-control" id="id_first_name"
               v-model="firstName" ref="FirstName"
        />
      </div>
    </div>
    <div class="col-md ">
      <div class="form-group">
        <label for="id_last_name">Nom du contact</label>
        <input type="text" name="contact_last_name" maxlength="255"
               class="textinput textInput form-control" id="id_last_name"
               v-model="lastName"
        />
      </div>
    </div>
  </div>
  <div class="form-group">
    <label for="id_address">Adresse</label>
    <textarea name="address" cols="40" rows="2" class="textarea form-control" id="id_address"
              v-model="address"
    ></textarea>
  </div>
  <div class="form-row">
    <city-auto-complete v-model:city="city" v-model:zipcode="zipCode"></city-auto-complete>
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
    />
  </div>

</template>

<script>
//import axios from 'axios';
import {CountrySelect} from 'vue3-country-region-select';
import CityAutoComplete from "@/components/CityAutoComplete.vue";

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
    }
  },
  methods: {
    onSelect(country) {
      console.log(country);
      // Check the country object example below.
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
    save(clientId) {
      this.$http.patch(`/api/clients/${clientId}/`, {
        contact_first_name: this.firstName,
        contact_last_name: this.lastName,
        contact_email: this.email,
        address: this.address,
        city: this.city,
        zip_code: this.zipCode,
        country: this.country,
        client_type: 'person',
      }).then(response => {
        this.$emit('company-saved', response.data)
      });
    },
  },
  watch: {
    lastName(value) {
      this.$emit('update:lastName', value)
    },
  }
}
</script>

<style scoped>

</style>
