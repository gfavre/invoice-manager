<template>
  <div id="div_id_name" class="form-group">
    <label for="id_name" class="requiredField">
      Nom de l'entreprise<span class="asteriskField">*</span>
    </label>
    <div>
      <input type="text" maxlength="255" required="required" id="id_name" name="name"
             class="textinput textInput form-control"
             v-model="name"
             :class="{ 'is-invalid': v$.name.$error && submitAttempted }"
      />
      <span class="invalid-feedback" v-if="v$.name.$error">{{ $t("This field is required")}}</span>
    </div>
  </div>

  <div id="div_id_address" class="form-group">
    <label for="id_address">Adresse</label>
    <div>
      <textarea name="address" cols="40" rows="2" id="id_address" class="textarea form-control"
                v-model="address"
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
          />
        </div>
      </div>

    </div>
    <div class="col-md-8">
      <city-auto-complete
          v-model:city="city"
          v-model:zipCode="zipCode"
          :city-label="$t('City')"
          :zipCode-label="$t('Postal code')"
      ></city-auto-complete>
    </div>
  </div>


  <div id="div_id_phone" class="form-group">
    <label for="id_phone">Numéro de téléphone</label>
    <input type="tel" maxlength="128" id="id_phone" class="textinput textInput form-control"
           v-model="phone" :class="{ 'is-invalid': v$.phone.$error && submitAttempted }"
    >
    <span class="invalid-feedback" v-if="v$.phone.$error">{{ $t("Phone number is invalid") }}</span>

  </div>

  <div id="div_id_additional_phone" class="form-group">
    <label for="id_additional_phone">Numéro de téléphone supplémentaire</label>
    <input type="tel" maxlength="128" id="id_additional_phone" class="textinput textInput form-control"
           v-model="additionalPhone"
           :class="{ 'is-invalid': v$.additionalPhone.$error && submitAttempted }"
    >
    <span class="invalid-feedback" v-if="v$.additionalPhone.$error">{{ $t("Phone number is invalid") }}</span>

  </div>

  <div id="div_id_email" class="form-group">
    <label for="id_email">Email</label>
    <div>
      <input type="email" name="email" maxlength="254" id="id_email" class="emailinput form-control"
             v-model="email"
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
             v-model="website"
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
import { defineComponent } from 'vue'
import CityAutoComplete from "@/components/CityAutoComplete.vue";
import useValidate from '@vuelidate/core'
import { required, email, url } from '@vuelidate/validators'
import {isValidPhoneNumber} from 'libphonenumber-js';


const validatePhoneNumber = (value) => {
  if (!value) {
    return true;
  }
  return isValidPhoneNumber(value, 'CH');
}
export default defineComponent({
  name: "CompanyForm",
  components: {
    CityAutoComplete,
  },
  emits: {

    next: null,
  },
  props:
    {
      company: {
        type: Object,
        required: true,
      },
      onUpdate: {
        type: Function,
        required: true
      },
    },


  data() {
    return {
      cities: [],
      name: this.company.name,
      address: this.company.address,
      city: this.company.city,
      zipCode: this.company.zipCode,
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
    setCompany(company){
      this.name = company.name;
      this.address = company.address;
      this.city = company.city;
      this.zipCode = company.zipCode;
      this.country = company.country;
      this.phone = company.phone;
      this.additionalPhone = company.additionalPhone;
      this.email = company.email;
      this.website = company.website;
    },
    handleSubmit() {
      this.submitAttempted = true;
      this.v$.$validate()
          .then((success) => {
            if (success) {
              this.onUpdate({
                name: this.name,
                address: this.address,
                city: this.city,
                zipCode: this.zipCode,
                country: this.country,
                phone: this.phone,
                additionalPhone: this.additionalPhone,
                email: this.email,
                website: this.website,
              });
              this.$emit('next');
            } else {
              this.focusFirstInvalidField();
            }
          });
    },
  },
  validations() {
    return {
      name: { required },
      email: { email },
      website: { url },
      phone: { validatePhoneNumber },
      additionalPhone: { validatePhoneNumber },
    }
  }
});
</script>

<style scoped>

</style>
