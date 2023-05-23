<template>
  <div id="div_id_vat_id" class="form-group">
    <label for="id_vat_id">{{ $t("VAT ID")}}</label>
    <input type="text" name="vatId" maxlength="20" id="id_vat_id" class="textinput textInput form-control"
           placeholder="CHE-123.456.789"
           v-model="vatId" />
    <small id="emailHelp" class="form-text text-muted">
      {{ $t("vatNumberHelptext") }}
    </small>

  </div>

  <div class="form-row">
    <div class="col-md-6">
      <div id="div_id_iban" class="form-group">
        <label for="id_iban">IBAN<span class="asteriskField">*</span></label>
        <input type="text" name="iban" maxlength="34" minlength="15" id="id_iban"
               class="textinput textInput form-control"
               placeholder="CH12 1234 5678 9012 3456 7"
               required="required"
               v-model="iban" :class="classIbanValid"
        >
        <span class="invalid-feedback" v-if="ibanInvalid">{{ $t("The IBAN seems invalid") }}</span>
        <span class="invalid-feedback" v-if="v$.iban.$error">{{ $t("This field is required")}}</span>
        <small id="emailHelp" class="form-text text-muted">
          {{ $t("Often displayed on the back of your bank card, or in your ebanking") }}
        </small>
      </div>
    </div>
    <div class="col-md-6">
      <div id="div_id_name_for_bank" class="form-group">
        <label for="id_name_for_bank">
          {{ $t("Bank account's owner name")}}<span class="asteriskField">*</span>
        </label>
        <input type="text" name="nameForBank" maxlength="255" id="id_name_for_bank"
               class="textinput textInput form-control"
               required="required"
               v-model="nameForBank" ref="nameForBankField"
               :class="{ 'is-invalid': v$.nameForBank.$error }"
        >
        <span class="invalid-feedback" v-if="v$.nameForBank.$error">{{ $t("This field is required")}}</span>

      </div>
    </div>
  </div>

  <div class="form-row">
    <div class="col-9">
      <div id="div_id_bank" class="form-group">
        <label for="id_bank">{{ $t("Bank")}}</label>
        <textarea name="bank" cols="40" rows="3" id="id_bank" class="textarea form-control"
                  v-model="bank"
        ></textarea>
      </div>
    </div>
    <div class="col">
      <div id="div_id_bic" class="form-group">
        <label for="id_bic">BIC</label>
        <input type="text" name="swift" maxlength="11" id="id_bic" class="textinput textInput form-control"
               v-model="swift"
        >
      </div>
    </div>
  </div>

  <div class="buttonHolder">
    <input type="button" name="prev-2" :value="$t('Previous')" class="btn btn btn-secondary white"
           @click="handleSubmit(-1)"
    >
    <input type="button" name="next-2" :value="$t('Next')" class="btn btn btn-primary white"
           @click="handleSubmit(+1)"

    >
  </div>
</template>

<script>
import { required } from '@vuelidate/validators'
import useValidate from "@vuelidate/core";

export default {
  name: "BankingForm",
  props: {
    company: {
      type: Object,
      required: true,
    },
    ibanUrl: {
      type: String,
      required: true,
    },
    onUpdate: {
      type: Function,
      required: true
    },
  },
  emits: ["prev", "next"],
  data() {
    return {
      vatId: this.company.vatId,
      iban: this.company.iban,
      nameForBank: this.company.nameForBank? this.company.nameForBank : this.company.name ,
      bank: this.company.bank,
      swift: this.company.swift,

      ibanValid: undefined,
      submitAttempted: false,
      v$: useValidate(),
    };
  },
  computed: {

    classIbanValid() {
      if (this.ibanValid === true) {
        return 'is-valid';
      } else if (this.ibanValid === false || this.v$.iban.$error) {
        return 'is-invalid';
      }
      return '';
    },
    ibanInvalid() {
      return this.ibanValid === false;
    },
  },
  methods:{
    focusFirstInvalidField() {
      const invalidFields = document.querySelectorAll('.is-invalid');
      if (invalidFields.length > 0) {
        invalidFields[0].focus();
      }
    },
    async ibanLookup() {
      /* IBAN can range from as few as 15 characters (in Norway) and up to as many
      as 32 alphanumeric characters
      CH=21 chars, FR=27 chars, DE=22 chars, IT=27 chars, AT=20 chars, ES=24 chars, NL=18 chars,
      BE=16 chars, LU=20 chars, PT=25 chars, DK=18 chars, FI=18 chars, SE=24 chars, NO=15 chars,
      GB=22 chars, GR=27 chars, CY=28 chars, IE=22 chars, IS=26 chars, LI=21 chars, MT=31 chars,
      MC=27 chars, SM=27 chars, AL=28 chars, AD=24 chars, BA=20 chars, BG=22 chars, CR=22 chars,
      HR=21 chars, EE=20 chars, GE=22 chars, GL=18 chars, HU=28 chars, IE=22 chars, IL=23 chars,
      IQ=23 chars, IR=26 chars, JO=30 chars, KW=30 chars, KZ=20 chars, LB=28 chars, LC=32 chars,
      LT=20 chars, LV=21 chars, MK=19 chars, MR=27 chars, MU=30 chars, MD=24 chars, ME=22 chars,
      NL=18 chars, PK=24 chars, PS=29 chars, PL=28 chars, RO=24 chars, RS=22 chars, SA=24 chars,
      SK=24 chars, SI=19 chars, SM=27 chars, TN=24 chars, TR=26 chars, VG=24 chars, XK=20 chars
      */
      if (this.iban.replace(/\s/g, '').length < 15) {
        return;
      }
      if (!this.ibanUrl) {
        console.error('ibanUrl is not defined')
        return;
      }

      const url = `${this.ibanUrl}?q=${this.iban}`;
      const response = await fetch(url);
      const finalRes = await response.json();
      this.ibanValid = finalRes.valid;
      if (this.ibanValid){
        this.bank = `${finalRes.bank.name}
${finalRes.bank.address}
${finalRes.bank.zip_code} ${finalRes.bank.city}`;
        this.swift = finalRes.bank.swift;
        this.$refs.nameForBankField.focus();
      } else {
        this.bank = '';
        this.swift = '';
      }
    },
    handleSubmit(direction) {
      this.submitAttempted = true;
      this.v$.$validate().then((success) => {
        if (success) {
          this.onUpdate({
            vatId: this.vatId,
            iban: this.iban,
            nameForBank: this.nameForBank,
            bank: this.bank,
            swift: this.swift,
          });
          if (direction === -1) {
            this.$emit('prev');
          } else if (direction === +1) {
            this.$emit('next');
          }
        } else {
          this.focusFirstInvalidField();
        }
      });
    },
    setCompany(company) {
      this.vatId = this.vatId? this.vatId: company.vatId;
      this.bank = this.bank? this.bank: company.bank;
      this.swift = this.swift? this.swift: company.swift;
      this.iban = this.iban? this.iban: company.iban;
      if (!this.nameForBank) {
        this.nameForBank = company.nameForBank? company.nameForBank: company.name;
      }
    },
  },

  validations() {
    return {
      iban: { required },
      nameForBank: { required },
    }
  },
  watch: {
    iban: function() {
      this.ibanLookup();
    }
  }

}
</script>

<style scoped>

</style>
