<template>
  <div class="col-md-3">
    <div id="div_id_zip_code" class="form-group">
      <label for="id_zip_code">{{ zipcodeLabel }}</label>
      <div class="input-group">
        <input type="text" name="zip_code" maxlength="10"
               class="textinput textInput form-control" id="id_zip_code"
               @input="onZipcodeInput" v-model="localZipcode">
        <ul class="dropdown-menu  shadow" :class="{show: isCitiesDropdownVisible}" ref="dropdown">
          <li v-for="city in cities" :key="city">
            <a class="dropdown-item" @click="onCitySelected(city)">{{ city }}</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div class="col-md-9">
    <div id="div_id_city" class="form-group">
      <label for="id_city">{{ cityLabel }}</label>
      <input type="text" name="city" maxlength="255" class="textinput textInput form-control" id="id_city"
             v-model="localCity">
    </div>
  </div>
</template>

<script>
import {cityFromZip} from "swiss-zipcodes";

export default {
  name: "CityAutoComplete.vue",
  props: {
    zipcode: String,
    city: String,
    zipcodeLabel: {
      type: String,
      required: true,
    },
    cityLabel:  {
      type: String,
      required: true,
    },
  },
  computed: {
    isCitiesDropdownVisible() {
      return this.cities.length > 0;
    },
  },
  data() {
    return {
      localCity: this.city,
      localZipcode: this.zipcode,
      cities: [],
    };
  },

  methods: {
    onCitySelected(city) {
      this.localCity = city;
      this.cities = [];
    },
    onZipcodeInput() {
      if (this.localCity !== '') {
        return;
      }

      if (this.localZipcode.length < 3) {
        return;
      }
      this.cities = cityFromZip(this.localZipcode);
      if (this.cities.length === 1) {
        this.localCity = this.cities[0];
        this.cities = [];
      }
    },
    onWindowClick(event) {
      if (this.$refs.dropdown && !this.$refs.dropdown.contains(event.target)) {
        this.cities = [];
      }
    },
  },
  watch: {
    localCity(val) {
      this.$emit('update:city', val);
    },
    localZipcode(val) {
      this.$emit('update:zipcode', val);
    },
    city(newParentCity){
      this.localCity = newParentCity;
    },
    zipcode(newParentZipcode){
      this.localZipcode = newParentZipcode;
    }

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
