<template>
  <div class="col-md-3">
    <div id="div_id_zip_code" class="form-group">
      <label for="id_zip_code">Code postal</label>
      <div class="input-group">
        <input type="text" name="zip_code" maxlength="10"
               class="textinput textInput form-control" id="id_zip_code"
               @input="onZipcodeInput" v-model="zipcode">
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
      <label for="id_city">Localité</label>
      <input type="text" name="city" maxlength="255" class="textinput textInput form-control" id="id_city"
             v-model="city">
    </div>
  </div>
</template>

<script>
import {cityFromZip} from "swiss-zipcodes";

export default {
  name: "CityAutoComplete.vue",
  computed: {
    isCitiesDropdownVisible() {
      return this.cities.length > 0;
    },
  },
  data() {
    return {
      zipcode: "",
      cities: [],
      city: "",
    };
  },
  methods: {
    onCitySelected(city) {
      this.city = city;
      this.cities = [];
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
