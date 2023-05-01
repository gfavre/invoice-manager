<template>
  <div id="div_id_name" class="form-group">
    <label for="id_name" class="requiredField">
      Nom de l'entreprise<span class="asteriskField">*</span></label>
    <div>
      <input type="text" maxlength="255" required="required" id="id_name" name="name"
             class="textinput textInput form-control"
             v-model="name" @input="updateField('name', $event.target.value)"
                          :class="{ 'is-invalid': v$.name.$error && submitAttempted }"
      />
      <span class="invalid-feedback" v-if="v$.name.$error">{{ $t("This field is required")}}</span>
    </div>
  </div>

  <div id="div_id_address" class="form-group">
    <label for="id_address">Adresse</label>
    <div>
      <textarea name="address" cols="40" rows="2" id="id_address" class="textarea form-control"
                v-model="address" @input="updateField('address', $event.target.value)"
      ></textarea>
    </div>
  </div>

  <div class="form-row">
    <div class="col-md-4">
      <div id="div_id_country" class="form-group">
        <label for="id_country">Pays</label>
        <div>
          <country-select
              v-model="country"
              :country="country"
              :autocomplete="true"
              :removePlaceholder="true"
              topCountry="CH"
              className="lazyselect custom-select"
              @change="updateField('country', $event.target.value)"
          />
        </div>
      </div>

    </div>
    <div class="col-md-8">
      <city-auto-complete
          v-model:city="city"
          v-model:zipcode="zipcode"
          @update:zipcode="updateZipcode"
          :city-label="$t('City')"
          :zipcode-label="$t('Postal code')"
      ></city-auto-complete>
    </div>
  </div>


  <div id="div_id_phone" class="form-group">
    <label for="id_phone">Numéro de téléphone</label>
    <div>
      <input type="tel" maxlength="128" id="id_phone" class="textinput textInput form-control"
             v-model="phone" @input="updateField('phone', $event.target.value)"
      >
    </div>
  </div>

  <div id="div_id_additional_phone" class="form-group">
    <label for="id_additional_phone">Numéro de téléphone supplémentaire</label>
    <div>
      <input type="tel" maxlength="128" id="id_additional_phone" class="textinput textInput form-control"
             v-model="additionalPhone" @input="updateField('additionalPhone', $event.target.value)"
      >
    </div>
  </div>

  <div id="div_id_email" class="form-group">
    <label for="id_email">Email</label>
    <div>
      <input type="email" name="email" maxlength="254" id="id_email" class="emailinput form-control"
             v-model="email" @input="updateField('email', $event.target.value)"
             :class="{ 'is-invalid': v$.email.$error && submitAttempted }"
      />
      <span class="invalid-feedback" v-if="v$.email.$error">{{ $t("Email address is invalid") }}</span>
    </div>
  </div>

  <div id="div_id_website" class="form-group">
    <label for="id_website">Site Web</label>
    <div>
      <input type="url" name="website" maxlength="200" id="id_website" class="urlinput form-control"
             placeholder="https://example.com"
             v-model="website" @input="updateField('website', $event.target.value)"
             :class="{ 'is-invalid': v$.website.$error && submitAttempted }"
      />
      <span class="invalid-feedback" v-if="v$.website.$error">{{ $t("Website address is invalid, it should begin with http[s]://") }}</span>

    </div>
  </div>

  <div class="buttonHolder">
    <input type="submit" name="next-1" value="Suivant" class="btn btn btn-primary white" @click="handleSubmit()">
  </div>
</template>

<script>
import CityAutoComplete from "@/components/CityAutoComplete.vue";
import useValidate from '@vuelidate/core'
import { required, email, url } from '@vuelidate/validators'

export default {
  name: "CompanyForm",
  components: {
    CityAutoComplete,
  },
  props:
    [
      'company'
    ],


  data() {
    return {
      cities: [],
      name: this.company.name,
      address: this.company.address,
      city: this.company.city,
      zipcode: this.company.zipcode,
      country: this.company.country,
      phone: this.company.phone,
      additionalPhone: this.company.additionalPhone,
      email: this.company.email,
      website: this.company.website,

      submitAttempted: false,
      v$: useValidate(),
    };
  },

  methods: {
    focusFirstInvalidField() {
      const invalidFields = document.querySelectorAll('.is-invalid');
      if (invalidFields.length > 0) {
        invalidFields[0].focus();
      }
    },
    updateCompany(){
      this.name = this.company.name;
      this.address = this.company.address;
      this.city = this.company.city;
      this.zipcode = this.company.zipcode;
      this.country = this.company.country;
      this.phone = this.company.phone;
      this.additionalPhone = this.company.additionalPhone;
      this.email = this.company.email;
      this.website = this.company.website;
    },
    handleSubmit() {
      this.submitAttempted = true;
      console.log('handleSubmit');
      this.v$.$validate()
          .then((success) => {
            if (success) {
              this.$emit('submit');
            } else {
              this.focusFirstInvalidField();
            }
          });
    },

    updateField(field, value) {
      this.$emit('update:company', {field: field, value: value});
    },
    updateZipcode(value) {
      console.log('updateZipcode', value);
      this.$emit('update:company', {field: 'zipcode', value: value});
    },
  },
  validations() {
    return {
      name: { required },
      email: { email },
      website: { url },
    }
  }
};
</script>

<style scoped>

</style>
