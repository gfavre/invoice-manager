const app = new Vue({
  el: '#app',
  data: {
      bank: window.bank ? window.bank : '',
      iban: window.iban ? window.iban : '',
      ibanValid: undefined,
      swift: window.swift ? window.swift : '',
  },
  computed: {
    classIbanValid() {
      if (this.ibanValid === true) {
        return 'is-valid';
      } else if (this.ibanValid === false) {
        return 'is-invalid';
      }
      return '';
    }
  },
  methods: {
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

      const url = this.$refs.app.dataset.ibanUrl + this.iban;
      const response = await fetch(url);
      const finalRes = await response.json();
      this.ibanValid = finalRes.valid;
      if (this.ibanValid){
        this.bank = `${finalRes.bank.name}
${finalRes.bank.address}
${finalRes.bank.zip_code} ${finalRes.bank.city}`;
      this.swift = finalRes.bank.swift;
      } else {
        this.bank = '';
        this.swift = '';
      }

    }
  },
  watch: {
    iban: function() {
      this.ibanLookup();
    }
  }
});
