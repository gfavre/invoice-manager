<template>
  <div class="container-fluid p-0 p-sm-2">
    <header class="page-header page-header-dark bg-gradient-primary">
      <div class="container">
        <div class="page-header-content pt-4">
          <div class="row align-items-center justify-content-between">
            <div class="col-auto mt-4">
              <h1 class="page-header-title">
                Facture {{ invoice.code }}
              </h1>
              <div class="page-header-subtitle">
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
    <section class="container headed-content">
      <div class="card">
        <div class="card-body">
            <div class="form-row form-row">
              <div class="form-group col-md-6 mb-0">
                <div id="div_id_company" class="form-group">
                  <label for="id_company" class=" requiredField">Entreprise<span class="asteriskField">*</span></label>
                  <typeahead-input :items="companies" @select="onCompanySelect" :value="selectedCompany"></typeahead-input>
                </div>
              </div>
              <div class="form-group col-md-6 mb-0">
                <div id="div_id_client" class="form-group">
                  <label for="id_client" class=" requiredField">Client<span class="asteriskField">*</span> </label>
                  <typeahead-input :items="clients" @select="onClientSelect" :value="selectedClient"></typeahead-input>

                </div>
              </div>
            </div>
            <div class="form-row form-row">
              <div class="form-group col-md-6 mb-0">
                <div id="div_id_displayed_date" class="form-group">
                  <label for="id_displayed_date" class="">Date affichée</label>
                  <VueDatePicker v-model="invoice.displayed_date"
                                 :enable-time-picker="false"
                                 :format="formatDate"
                                 locale="ch-fr"
                                 placeholder="Select Date"
                                 @update:model-value="updateDueDate"
                                 close-on-scroll auto-apply
                  ></VueDatePicker>
                </div>
              </div>
              <div class="form-group col-md-6 mb-0">
                <div id="div_id_due_date" class="form-group">
                  <label for="id_due_date" class=" requiredField">Date d'échéance<span class="asteriskField">*</span>
                  </label>
                  <VueDatePicker v-model="invoice.due_date"
                                 :enable-time-picker="false"
                                 :format="formatDate"
                                 :min-date="invoice.displayed_date"
                                 locale="ch-fr"
                                 placeholder="Select Date"
                                 close-on-scroll auto-apply
                  ></VueDatePicker>
                </div>
              </div>
            </div>
            <div id="div_id_title" class="form-group"><label for="id_title" class="">
              Titre
            </label>
              <div>
                <input type="text" name="title" maxlength="100" class="textinput textInput form-control"
                       id="id_title">
              </div>
            </div>
            <div id="div_id_description" class="form-group">
              <label for="id_description" class="">Description</label>
              <QuillEditor theme="snow"
                           :toolbar="[['bold', 'italic', 'underline', 'strike'],
                            [{ 'list': 'ordered'}, { 'list': 'bullet' }], [{ 'script': 'sub'}, { 'script': 'super' }],
                            [{ 'color': [] }], ['link'] ]"
                           :style="{ minHeight: '8em' }"

              />
            </div>
            <div class="form-row form-row">
              <div class="form-group col-md-6 mb-0">
                <div id="div_id_period_start" class="form-group">
                  <label for="id_period_start" class="">Début de la période de facturation</label>
                  <VueDatePicker v-model="invoice.period_start"
                                 :enable-time-picker="false"
                                 :format="formatDate"
                                 locale="ch-fr"
                                 placeholder="Select Date"
                                 @update:model-value="updatePeriodEnd"
                                 close-on-scroll auto-apply
                  ></VueDatePicker>
                </div>
              </div>
              <div class="form-group col-md-6 mb-0">
                <div id="div_id_period_end" class="form-group">
                  <label for="id_period_end" class="">Fin de la période de facturation</label>
                  <VueDatePicker v-model="invoice.period_end"
                                 :enable-time-picker="false"
                                 :format="formatDate"
                                 :min-date="invoice.period_start"
                                 locale="ch-fr"
                                 placeholder="Select Date"
                                 close-on-scroll auto-apply
                  ></VueDatePicker>
                </div>
              </div>
            </div>
            <div class="card border-left-info shadow mb-3">
              <div class="card-body">
                <h5 class="text-xs font-weight-bold text-info text-uppercase mb-4">Lignes</h5>
                <div class="lines">
                    <invoice-line
                      v-for="line in invoice.lines"
                      :key="line.uuid"
                      :description="line.description"
                      :quantity="line.quantity"
                      :unit="line.unit"
                      :price="line.price"
                      :line-id="line.id"
                      :invoice-id="this.invoice.id"
                      :uuid="line.uuid"
                      @update-line="handleUpdateLine(line)"
                      @save="saveLine(index)"
                      @remove="removeLine(index)"
                    />
                  <button type="button" @click="addLine" class="btn btn btn-info">Add Line</button>
                </div>
              </div>
            </div>

            <div id="div_id_vat_rate" class="form-group col-3">
              <label for="id_vat_rate" class="">Taux de TVA</label>
              <div class="input-group">
                <input type="text" v-model="vatRatePercent" @input="validateFloatValue"
                       id="id_vat_rate" class="form-control">
                <div class="input-group-append">
                  <span class="input-group-text">%</span>
                </div>
              </div>
            </div>
            <input type="submit" name="save" value="Enregistrer" class="btn btn-primary" id="submit-id-save">
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import InvoiceLine from './components/InvoiceLine.vue'
import {QuillEditor} from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css';
import TypeaheadInput from '@/components/TypeaheadInput.vue';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import { v4 as uuidv4 } from 'uuid';


export default {
  name: 'App',
  components: {
    InvoiceLine,
    VueDatePicker,
    QuillEditor,
    TypeaheadInput,
  },
  data() {
    return {
      companies: [
        {
          id: 1,
          name: 'Company 1',
        },
        {
          id: 2,
          name: 'Company 2',
        },
        {
          id: 3,
          name: 'Company 3',
        }
      ],
      company: {
        name: '',
        address: '',
        zip_code: '',
        city: '',
        country: '',

        phone: '',
        additional_phone: '',
        email: '',
        website: '',
        vat_id: '',

        name_for_bank: '',
        bank: '',
        bic: '',
        iban: '',

        logo: '',
        contrast_color: '',

        signature_text: '',
        signature_image: '',
        invoice_note: '',
        thanks: '',
      },
      selectedCompany: 'Company 1',
      clients: [
        {
          id: 1,
          name: 'Twist Lab',
        },
        {
          id: 2,
          name: 'Montreux',
        },
        {
          id: 3,
          name: 'Nyon',
        },
          {
          id: 4,
          name: 'Twisted inc',
        },
      ],
      selectedClient: 'Twist',
      client: {
        name: '',
        address: '',
        zip_code: '',
        city: '',
        country: '',

        language: '',
        currency: '',
        payment_delay_days: 30,
        vat_rate: 0.077,
        default_hourly_rate: 0.0,

        slug: '',
      },
      invoice: {
        id: 1, // FIXME!!
        code: "",
        due_date: "",
        displayed_date: new Date(),
        vat_rate: "",
        total: 0,
        title: "",
        description: "",
        period_start: "",
        period_end: "",
        lines: [],
      },
      vatRatePercent: "",
      urls: {
        companiesUrl: "",
      },
    }
  },
  methods: {
    addLine() {
      this.invoice.lines.push({
          uuid: uuidv4(),
        description:"", quantity:0, unit:"hour", price:0, id: null
      });

    },
    removeLine(index) {
      this.invoice.lines.splice(index, 1);
    },
    saveLine(line) {
      console.log(line)
    },
    formatDate(date) {
      const day = date.getDate();
      const month = date.getMonth() + 1;
      const year = date.getFullYear();
      return `${day}.${month}.${year}`;
    },
    handleUpdateLine(line) {
      console.log(line)
    },
    onClientSelect(client) {
      // Handle client selection here
      console.log(client)
    },
    onCompanySelect(company) {
      // Handle company selection here
      console.log(company)
    },
    updateDueDate() {
      if (!this.invoice.due_date || this.invoice.due_date < this.invoice.displayed_date) {
        // Calculate the new due date based on the payment_delay_days
        const new_due_date = new Date(this.invoice.displayed_date.getTime() + (this.client.payment_delay_days * 24 * 60 * 60 * 1000));
        this.invoice.due_date = new_due_date;
      }
    },
    updatePeriodEnd() {
      if (!this.invoice.period_end || this.invoice.period_end < this.invoice.period_start) {
        const year = this.invoice.period_start.getFullYear();
        const month = this.invoice.period_start.getMonth();

        if (this.invoice.period_start.getDate() === 1) {
          const lastDayOfMonth = new Date(
              this.invoice.period_start.getFullYear(),
              this.invoice.period_start.getMonth() + 1,
              0
          );
          this.invoice.period_end = lastDayOfMonth
        } else {
          let endYear, endMonth;
          if (month === 11) {
            endMonth = 0;
            endYear = year + 1;
          } else {
            endMonth = month + 1;
            endYear = year;
          }
          this.invoice.period_end = new Date(endYear, endMonth, this.invoice.period_start.getDate() - 1);
        }
      }
    },
    validateFloatValue() {
      // Remove any non-digit or non-decimal characters
      let value = this.vatRatePercent.replace(/[^0-9.]/g, '');

      // Only allow one decimal point
      const decimalIndex = value.indexOf('.');
      if (decimalIndex !== -1) {
        value = value.slice(0, decimalIndex + 1) + value.slice(decimalIndex + 1).replace(/\./g, '');
      }

      // Set the validated value back to the component
      this.vatRatePercent = value;
    },
  },

  mounted() {
    this.urls.companiesUrl = this.$el.parentNode.dataset.companiesUrl;
    this.$http.get(this.urls.companiesUrl).then(response => {
      this.companies = response.data.results;
      if (this.companies.length === 1) {
        this.company = this.companies[0].id
      }
    }).catch(error => {
      console.error(error)
    });
    this.updateDueDate();
    this.vatRatePercent = 7.7
    this.addLine();

  },
  watch: {
    vatRatePercent: function (value) {
      this.invoice.vat_rate = value / 100;
    },
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
