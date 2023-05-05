<template>
  <div class="container-fluid p-0 p-sm-2">
    <header class="page-header page-header-dark bg-gradient-primary">
      <div class="container">
        <div class="page-header-content pt-4">
          <div class="row align-items-center justify-content-between">
            <div class="col-auto mt-4">
              <h1 class="page-header-title">
                {{ $t('Invoice') }}
              </h1>
              <div class="page-header-subtitle">{{ invoice.code }}</div>
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
                <label for="id_company" class=" requiredField">
                  {{ $t("Company") }}<span class="asteriskField">*</span>
                </label>
                <typeahead-input :items="companies" @select="handleCompanySelect"
                                 :value="selectedCompany"></typeahead-input>
              </div>
            </div>
            <div class="form-group col-md-6 mb-0">
              <div id="div_id_client" class="form-group">
                <label for="id_client" class=" requiredField">
                  {{ $t("Client") }}<span class="asteriskField">*</span>
                </label>
                <typeahead-input :items="clients" @select="handleClientSelect"
                                 :value="selectedClient"></typeahead-input>
              </div>
            </div>
          </div>
          <div class="form-row form-row">
            <div class="form-group col-md-6 mb-0">
              <div id="div_id_displayed_date" class="form-group">
                <label for="id_displayed_date" class="">{{ $t("Displayed date") }}</label>
                <VueDatePicker v-model="invoice.displayed_date"
                               :enable-time-picker="false"
                               :format="formatDate"
                               :locale="datePickerLang"
                               :placeholder="$t('Select date')"
                               @update:model-value="updateDueDate"
                               close-on-scroll auto-apply
                ></VueDatePicker>
              </div>
            </div>
            <div class="form-group col-md-6 mb-0">
              <div id="div_id_due_date" class="form-group">
                <label for="id_due_date" class="requiredField">
                  {{ $t("Due date") }}<span class="asteriskField">*</span>
                </label>
                <VueDatePicker v-model="invoice.due_date"
                               :enable-time-picker="false"
                               :format="formatDate"
                               :min-date="invoice.displayed_date"
                               :locale="datePickerLang"
                               :placeholder="$t('Select date')"
                               @update:model-value="saveInvoice"
                               close-on-scroll auto-apply
                ></VueDatePicker>
                <small id="due_date_help" class="form-text text-muted" v-if="client.id">
                  {{
                    $t("Usual payment delay for {client} is {nb_days} days", {
                      "client": client.name,
                      "nb_days": client.payment_delay_days
                    })
                  }}
                </small>

              </div>
            </div>
          </div>
          <div id="div_id_title" class="form-group">
            <label for="id_title" class="">
              {{ $t("Title") }}
            </label>
            <div>
              <input type="text" name="title" maxlength="100"
                     class="textinput textInput form-control" id="id_title"
                     v-model="invoice.title" @blur="saveInvoice"/>
            </div>
          </div>
          <div id="div_id_description" class="form-group">
            <label for="id_description" class="">{{ $t("Description") }}</label>
            <Editor v-model="invoice.description"
                    api-key="nf16mminr724hh5tj7jgizwldbt3wy1rhmriy9trfwefr4wq"
                    :init="{
      language: tinyMCELang,
      height: '16em',
      menubar: false,
      plugins: [
        'lists', 'link', 'searchreplace'
      ],
      toolbar:
        'undo redo | bold italic underline strikethrough | forecolor |\
        bullist numlist outdent indent | removeformat'
    }"
                    @blur="saveInvoice"/>
          </div>
          <div class="form-row form-row">
            <div class="form-group col-md-6 mb-0">
              <div id="div_id_period_start" class="form-group">
                <label for="id_period_start" class="">{{ $t("Start of invoice period") }}</label>
                <VueDatePicker v-model="invoice.period_start"
                               :enable-time-picker="false"
                               :format="formatDate"
                               :locale="datePickerLang"
                               :placeholder="$t('Select date')"
                               @update:model-value="updatePeriodEnd"
                               close-on-scroll auto-apply
                ></VueDatePicker>
              </div>
            </div>
            <div class="form-group col-md-6 mb-0">
              <div id="div_id_period_end" class="form-group">
                <label for="id_period_end" class="">{{ $t("End of invoice period") }}</label>
                <VueDatePicker v-model="invoice.period_end"
                               :enable-time-picker="false"
                               :format="formatDate"
                               :min-date="invoice.period_start"
                               :locale="datePickerLang"
                               :placeholder="$t('Select date')"
                               @update:model-value="saveInvoice"
                               close-on-scroll auto-apply
                ></VueDatePicker>
              </div>
            </div>
          </div>
          <div class="card border-left-info shadow mb-3">
            <div class="card-body">
              <h5 class="text-info text-uppercase mb-4">{{ $t("Lines") }}</h5>
              <p>
                <small id="price_help" class="form-text text-muted" v-if="client.id">
                  {{
                    $t("Usual hourly rate for {client} is {amount} ", {
                      "client": client.name,
                      "amount": client.default_hourly_rate
                    })
                  }}
                </small>
              </p>

              <div class="lines">
                <invoice-line
                    v-for="line in invoice.lines"
                    :key="line.uuid"
                    :description="line.description"
                    :quantity="line.quantity"
                    :unit="line.unit"
                    :price="line.price_per_unit"
                    :line-id="line.id"
                    :invoice-id="invoice.id"
                    :uuid="line.uuid"
                    :api-url="urls.linesUrl"
                    @update-line="handleUpdateLine"
                    @remove="removeLine"
                    ref="invoiceLines"
                />
                <button type="button" @click="addLine" class="btn btn btn-info">{{ $t("Add line") }}</button>
              </div>
            </div>
          </div>

          <div id="div_id_vat_rate" class="form-group col-3">
            <label for="id_vat_rate">{{ $t("VAT rate") }}</label>
            <div class="input-group">
              <input type="text" id="id_vat_rate" class="form-control"
                     v-model="vatRatePercent" @input="validateFloatValue" @blur="saveInvoice">
              <div class="input-group-append">
                <span class="input-group-text">%</span>
              </div>
            </div>
          </div>
          <hr>
          <dl class="row">
            <dt class="col-3 text-right">{{ $t("Total before tax") }}</dt>
            <dd class="col-9 text-left">{{ currency }} {{ $formatAmount(invoice.subtotal) }}</dd>
            <dt class="col-3 text-right">{{ $t("VAT") }} ({{ vatRatePercent }}%)</dt>
            <dd class="col-9 text-left">{{ currency }} {{ $formatAmount(invoice.vat) }}</dd>
            <dt class="col-3 text-right">{{ $t("Total including tax") }}</dt>
            <dd class="col-9 text-left">{{ currency }} {{ $formatAmount(invoice.total) }}</dd>
          </dl>
          <a href="#" @click.prevent="preview" class="btn btn-primary">{{ $t('Preview') }}</a>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import moment from 'moment';
import {v4 as uuidv4} from 'uuid';
import {useI18n} from 'vue-i18n'
import Editor from '@tinymce/tinymce-vue'
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

import InvoiceLine from '@/components/InvoiceLine.vue'
import TypeaheadInput from '@/components/TypeaheadInput.vue';

export default {
  name: 'App',
  components: {
    InvoiceLine,
    VueDatePicker,
    Editor,
    TypeaheadInput,
  },
  computed: {
    currency() {
      if (this.client && this.client.currency) {
        return this.client.currency;
      } else if (this.company.currency) {
        return this.company.currency;
      } else {
        return 'CHF';
      }
    },
    datePickerLang() {
      const {locale} = useI18n();
      return locale.value + '-CH';
    },
    tinyMCELang() {
      const {locale} = useI18n();
      switch (locale.value) {
        case 'de':
          return 'de';
        case 'fr':
          return 'fr_FR';
        case 'it':
          return 'it';
        default:
          return 'en_US';
      }
    },
  },
  data() {
    return {
      companies: [],
      company: {
        id: '',
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
      selectedCompany: '',
      clients: [],
      selectedClient: '',
      client: {
        id: null,
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
        id: null,
        code: "",
        due_date: "",
        displayed_date: new Date(),
        vat_rate: 0.077,
        title: "",
        description: "",
        period_start: "",
        period_end: "",
        lines: [],
        subtotal: 0,
        vat: 0,
        total: 0,
      },
      vatRatePercent: 7.7,
      urls: {
        companiesUrl: "",
        clientsUrl: "",
        invoiceUrl: "",
        linesUrl: "",
        previewUrl: "",
      },
      saving: false,
      waitResolve: null

    }
  },
  methods: {
    addLine() {
      this.invoice.lines.push({
        uuid: uuidv4(), description: "", quantity: 0.0, unit: "h",
        price_per_unit: this.client.default_hourly_rate, id: null, total: 0
      });
      this.$nextTick(() => {
        this.$refs.invoiceLines[this.$refs.invoiceLines.length - 1].focus();
      });
    },
    removeLine(index) {
      this.invoice.lines.splice(index, 1);
      this.updateTotal();
    },
    formatDate(date) {
      const day = date.getDate();
      const month = date.getMonth() + 1;
      const year = date.getFullYear();
      return `${day}.${month}.${year}`;
    },
    handleUpdateLine(line) {
      const index = this.invoice.lines.findIndex((l) => l.uuid === line.uuid);
      this.invoice.lines[index] = line;
      this.updateTotal()
    },
    handleClientSelect(client) {
      if (!client) {
        this.client = {};
        this.saveInvoice();
        return;
      }
      // Handle client selection here
      this.fetchClient(client.id).then(() => {
        this.$refs.invoiceLines.forEach((line) => {
          if (line.localQuantity === 0) {
            line.localPrice = this.client.default_hourly_rate;
          }
        });
        this.invoice.vat_rate = this.client.vat_rate;
        this.vatRatePercent = this.invoice.vat_rate * 100;
        this.updateTotal();
        this.saveInvoice();
      });
    },
    handleCompanySelect(company) {
      if (!company) {
        this.company = {};
        this.saveInvoice();
        return;
      }
      this.fetchCompany(company.id).then(() => {
        this.updateClientsList();
        this.saveInvoice();
      });
    },
    async fetchCompany(companyId) {
      const response = await this.$http.get(`${this.urls.companiesUrl}${companyId}/`);
      this.company = response.data;
      this.selectedCompany = this.company.name;
    },
    async fetchClient(clientId) {
      const response = await this.$http.get(`${this.urls.clientsUrl}${clientId}/`);
      this.client = response.data;
      this.selectedClient = this.client.name;
    },
    async fetchInvoice() {
      await this.$http.get(this.urls.invoiceUrl).then(response => {
        this.invoice.id = response.data.id;
        this.invoice.code = response.data.code;
        if (response.data.due_date) {
          this.invoice.due_date = new Date(response.data.due_date);
        }
        if (response.data.displayed_date) {
          this.invoice.displayed_date = new Date(response.data.displayed_date);
        }
        this.vatRatePercent = response.data.vat_rate * 100;
        this.invoice.vat_rate = response.data.vat_rate;
        this.invoice.title = response.data.title;
        this.invoice.description = response.data.description;
        if (response.data.period_start) {
          this.invoice.period_start = response.data.period_start;
        }
        if (response.data.period_end) {
          this.invoice.period_end = response.data.period_end;
        }
        this.invoice.lines = response.data.lines;
        this.invoice.lines.forEach((line) => {
          line.uuid = uuidv4();
        });
        if (this.invoice.lines.length === 0) {
          this.addLine();
        }
        this.updateTotal()
        if (response.data.client) {
          this.fetchClient(response.data.client)
        }
        if (response.data.company) {
          this.fetchCompany(response.data.company)
        }
      }).catch(error => {
        console.error(error)
      });
    },
    async preview(){
      if (this.saving) {
        // create a Promise that resolves when isHandlingClick becomes false
        const waitPromise = new Promise(resolve => {
          this.waitResolve = resolve;
        });
        await waitPromise;
      }
      window.location.href = this.urls.previewUrl;
    },

    async saveInvoice() {
      this.saving = true;
      const data = {
        company: this.company ? this.company.id : null,
        client: this.client ? this.client.id : null,
        due_date: this.invoice.due_date ? moment(this.invoice.due_date).format('YYYY-MM-DD') : null,
        displayed_date: this.invoice.displayed_date ? moment(this.invoice.displayed_date).format('YYYY-MM-DD') : null,
        vat_rate: this.invoice.vat_rate,
        title: this.invoice.title,
        description: this.invoice.description,
        period_start: this.invoice.period_start ? moment(this.invoice.period_start).format('YYYY-MM-DD') : null,
        period_end: this.invoice.period_end ? moment(this.invoice.period_end).format('YYYY-MM-DD') : null,
      }
      await this.$http.patch(this.urls.invoiceUrl, data).then(response => {
        this.invoice.id = response.data.id;
        this.invoice.code = response.data.code;
      }).catch(error => {
        console.error(error)
      }).finally(() => {
        this.saving = false;
        // resolve the waitPromise if it exists
        if (this.waitResolve) {
          this.waitResolve();
        }
      });
    },
    updateCompaniesList() {
      let url = this.urls.companiesUrl;
      this.$http.get(url).then(response => {
        this.companies = response.data.results;
        if (this.companies.length === 1) {
          this.company = this.companies[0].id
        }
      }).catch(error => {
        console.error(error)
      });
    },
    updateClientsList() {
      let url = this.urls.clientsUrl;
      if (this.company.id !== "") {
        url += `?company_uuid=${this.company.id}`;
      }
      this.$http.get(url).then(response => {
        this.clients = response.data.results;
        if (this.clients.length === 1) {
          this.client = this.clients[0].id
        }
      }).catch(error => {
        console.error(error)
      });
    },
    updateDueDate() {
      if (!this.invoice.due_date || this.invoice.due_date < this.invoice.displayed_date) {
        // Calculate the new due date based on the payment_delay_days
        this.invoice.due_date = new Date(this.invoice.displayed_date.getTime() + (this.client.payment_delay_days * 24 * 60 * 60 * 1000));
      }
      this.saveInvoice()
    },
    updatePeriodEnd() {
      if (!this.invoice.period_end || this.invoice.period_end < this.invoice.period_start) {
        const year = this.invoice.period_start.getFullYear();
        const month = this.invoice.period_start.getMonth();

        if (this.invoice.period_start.getDate() === 1) {
          this.invoice.period_end = new Date(
            this.invoice.period_start.getFullYear(),
            this.invoice.period_start.getMonth() + 1,
            0
          );
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
      this.saveInvoice()
    },
    updateTotal() {
      this.invoice.subtotal = this.invoice.lines.reduce((acc, line) => acc + line.total, 0);
      this.invoice.vat = this.invoice.subtotal * this.invoice.vat_rate;
      this.invoice.total = this.invoice.subtotal + this.invoice.vat;
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
    this.$i18n.locale = this.$el.parentNode.dataset.languageCode;
    this.urls.companiesUrl = this.$el.parentNode.dataset.companiesUrl;
    this.urls.clientsUrl = this.$el.parentNode.dataset.clientsUrl;
    this.urls.invoiceUrl = this.$el.parentNode.dataset.invoiceUrl;
    this.urls.linesUrl = this.$el.parentNode.dataset.linesUrl;
    this.urls.previewUrl = this.$el.parentNode.dataset.previewUrl;
    this.fetchInvoice();
    this.updateCompaniesList();
    this.updateClientsList();
    this.updateTotal();
  },
  watch: {
    vatRatePercent: function (value) {
      this.invoice.vat_rate = value / 100;
      this.updateTotal();
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
:root {
  --dp-text-color: #6e707e;
}

.dp__theme_light {
  --dp-text-color: #6e707e;
}

.tox.tox-tinymce {
  border: 1px solid #d1d3e2;
  border-radius: 0.35rem;
}

.tox.tox-tinymce .tox-editor-header {
  box-shadow: none !important;
  border-bottom: 1px solid #d1d3e2 !important;
}

.tox-tinymce .tox-statusbar__branding {
  display: none!important;
}
</style>
