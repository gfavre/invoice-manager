<template>
  <div id="div_id_company" class="form-group" v-if="companies.length > 1">
    <label for="id_company_0" class=" requiredField">
      Client pour<span class="asteriskField">*</span>
    </label>
    <div>
      <div class="custom-control custom-radio custom-control-inline"
           v-for="cItem in companies" :key="cItem.id">
        <input type="radio" class="custom-control-input" name="company" required=""
               :value="cItem.id" :id="'company-' + cItem.id" v-model="company"
        />
        <label class="custom-control-label"
               :for="'company-' + cItem.id">
          {{ cItem.name }}
        </label>
      </div>
    </div>
    <hr>
  </div>

  <div id="div_id_client_type" class="form-group">
    <label for="id_client_type_0" class=" requiredField">
      {{ t("Type of client") }}<span class="asteriskField">*</span>
    </label>
    <div>
      <div class="custom-control custom-radio custom-control-inline">
        <input type="radio" class="custom-control-input" name="client_type" value="company"
               id="id_client_type_0" required=""
               v-model="clientType"/>
        <label class="custom-control-label" for="id_client_type_0">
          <i class="bi bi-journal"></i> {{ t("company") }}
        </label>
      </div>
      <div class="custom-control custom-radio custom-control-inline">
        <input type="radio" class="custom-control-input" name="client_type" value="person"
               id="id_client_type_1" required=""
               v-model="clientType"/>
        <label class="custom-control-label" for="id_client_type_1">
          <i class="bi bi-person-fill"></i>
          {{ t("person") }}
        </label>
      </div>
    </div>
  </div>

  <section v-show="isPerson">
    <fieldset class="border-left-info shadow" id="company_infos">
      <legend class=" mb-1">Personne</legend>
      <person-form ref="personForm" @update:lastName="slugUpdate"></person-form>
    </fieldset>
  </section>

  <section v-show="isCompany">
    <fieldset class="border-left-primary shadow" id="company_infos">
      <legend class=" mb-1">Entreprise</legend>
      <company-form ref="companyForm" @update:name="slugUpdate"></company-form>
    </fieldset>
    <dl v-if="selectedCompany != null">
      <dt>The company</dt>
      <dd>{{ selectedCompany }}</dd>
    </dl>
  </section>

  <section>
    <fieldset class="border-left-success shadow ">
      <legend class=" mb-1">Factures</legend>
      <InvoiceForm ref="invoiceForm"></InvoiceForm>
    </fieldset>
  </section>

  <div class="buttonHolder">
    <input type="submit" name="submit" value="Enregistrer"
           class="btn btn-primary button white" id="submit-id-submit"
           @click.prevent="saveClient" />

  </div>

</template>

<script>
import PersonForm from '@/components/PersonForm.vue';
import CompanyForm from '@/components/CompanyForm.vue';
import InvoiceForm from "@/components/InvoiceForm.vue";
import {useI18n} from 'vue-i18n'
import slugify from "slugify";


export default {
  name: 'App',
  //i18n,
  components: {
    PersonForm,
    CompanyForm,
    InvoiceForm,

  },
  computed: {
    isCompany() {
      return this.clientType === 'company';
    },
    isPerson() {
      return this.clientType === 'person';
    },
  },

  data() {
    return {
      clientType: 'company',
      slug: "",
      client: null,
      clientId: null,
      companies: [],
      company: ""
    }
  },
  methods: {
    async saveClient() {
      if (this.clientId === null) {
        try {
          const data = {
            client_type: this.clientType,
            company: this.company,
          }
          const response = await this.$http.post('/api/clients/', data)
          this.clientId = response.data.id;
        } catch (error) {
          console.log(error);
        }
      }
      if (this.clientId !== null) {
        await this.$nextTick();
        if (this.clientType === 'company') {
          this.$refs.companyForm.save(this.clientId);
        } else {
          this.$refs.personForm.save(this.clientId);
        }
        this.$refs.invoiceForm.save(this.clientId);
      }
    },
    slugUpdate(name) {
      this.slug = slugify(name, {
        lower: true, // convert to lowercase
        strict: true // remove special characters
      });
    },
  },
  created() {
    this.$http.get('/api/companies/').then( response => {
      this.companies = response.data.results;
      if (this.companies.length == 1) {
        this.company = this.companies[0].id
      }
    }).catch(error => {
      console.log(error)
    });

    const path = window.location.pathname;
    const match = path.match(/\/clients\/([\da-fA-F]{8}-([\da-fA-F]{4}-){3}[\da-fA-F]{12})\/edit/);
    if (match)  {
      this.clientId = match[1];
        this.$http.get(`/api/clients/${this.clientId}/`).then(response => {
          this.client = response.data;
          this.clientType = this.client.client_type;
          this.company = this.client.company;
          this.$refs.companyForm.setClient(this.client);
          this.$refs.invoiceForm.setClient(this.client);
          this.$refs.personForm.setClient(this.client);
        }).catch(error => {
          console.log(error)
        });
    }
  },
  setup() {
    const {t} = useI18n({
      inheritLocale: true,
      useScope: 'local'
    })

    return {t}
  }
}
</script>

<style>
</style>

<i18n>
{
  "fr": {
    "company": "Entreprise",
    "person": "Personne",
    "Type of client": "Type de client"
  },
  "en": {
    "company": "Company",
    "person": "Person",
    "Type of client": "Type of client"
  }
}
</i18n>
