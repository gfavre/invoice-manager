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
            <div class="form-group col-md-6 mb-0" v-if="companies.length > 1">
              <div id="div_id_company" class="form-group">
                <label for="id_company" class=" requiredField">
                  {{ $t("Company") }}<span class="asteriskField">*</span>
                </label>
                <typeahead-input :items="companies" @select="handleCompanySelect"
                                 :value="selectedCompanyName"
                                 :class="{ 'is-invalid': v$.company.$error }"
                ></typeahead-input>
                <span class="invalid-feedback" v-if="v$.company.required.$invalid">
                  {{ $t("This field is required") }}
                </span>
              </div>

            </div>
            <div class="form-group col-md-6 mb-0">
              <div id="div_id_client" class="form-group">
                <label for="id_client" class=" requiredField">
                  {{ $t("Client") }}<span class="asteriskField">*</span>
                </label>
                <typeahead-input :items="clients" @select="handleClientSelect"
                                 :value="selectedClientName"
                                 :class="{ 'is-invalid': v$.client.$error }"
                ></typeahead-input>
                <span class="invalid-feedback" v-if="v$.client.required.$invalid">
                  {{ $t("This field is required") }}
                </span>
              </div>
            </div>
          </div>
          <div class="form-row form-row">
            <div class="form-group col-md-6 mb-0">
              <div id="div_id_displayed_date" class="form-group">
                <label for="id_displayed_date" class="">
                  {{ $t("Invoice date") }}<span class="asteriskField">*</span>
                </label>
                <VueDatePicker v-model="invoice.displayed_date"
                               :class="{ 'is-invalid': v$.invoice.displayed_date.$error }"
                               :enable-time-picker="false"
                               :format="formatDate"
                               :locale="datePickerLang"
                               :placeholder="$t('Select date')"

                               @update:model-value="updateDueDate"
                               close-on-scroll auto-apply
                ></VueDatePicker>
                <span class="invalid-feedback" v-if="v$.invoice.displayed_date.required.$invalid">
                  {{ $t("This field is required") }}
                </span>
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
                               :class="{ 'is-invalid': v$.invoice.due_date.$error }"
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
                <span class="invalid-feedback" v-if="v$.invoice.due_date.required.$invalid">
                  {{ $t("This field is required") }}
                </span>
                <span class="invalid-feedback" v-if="v$.invoice.due_date.later_than_displayed_date.$invalid">
                  {{ $t("Due date should happen later than displayed date") }}
                </span>
              </div>
            </div>
          </div>
          <div id="div_id_title" class="form-group">
            <label for="id_title" class="">
              {{ $t("Title") }}<span class="asteriskField">*</span>
            </label>
            <input type="text" name="title" maxlength="100"
                   class="textinput textInput form-control" id="id_title"
                   v-model="invoice.title"
                   :class="{ 'is-invalid': v$.invoice.title.$error }"
            />
            <span class="invalid-feedback" v-if="v$.invoice.title.$error">{{ $t("This field is required") }}</span>
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
            />
          </div>
          <div class="form-row form-row">
            <div class="form-group col-md-6 mb-0">
              <label for="id_period_start" class="">{{ $t("Start of invoice period") }}</label>
              <VueDatePicker v-model="invoice.period_start"
                             :class="{ 'is-invalid': v$.invoice.period_start.$error }"
                             :enable-time-picker="false"
                             :format="formatDate"
                             :locale="datePickerLang"
                             :placeholder="$t('Select date')"
                             @update:model-value="updatePeriodEnd"
                             close-on-scroll auto-apply
              ></VueDatePicker>
              <span class="invalid-feedback" v-if="v$.invoice.period_start.required_if_period_end.$invalid">
                {{ $t("This field is required as end of invoice period has been set") }}
              </span>
            </div>
            <div class="form-group col-md-6 mb-0">
              <label for="id_period_end" class="">{{ $t("End of invoice period") }}</label>
              <VueDatePicker v-model="invoice.period_end"
                             :class="{ 'is-invalid': v$.invoice.period_end.$error }"
                             :enable-time-picker="false"
                             :format="formatDate"
                             :min-date="invoice.period_start"
                             :locale="datePickerLang"
                             :placeholder="$t('Select date')"
                             close-on-scroll auto-apply
              ></VueDatePicker>
              <span class="invalid-feedback" v-if="v$.invoice.period_end.required_if_period_start.$invalid">
                {{ $t("This field is required as start of invoice period has been set") }}
              </span>
              <span class="invalid-feedback" v-if="v$.invoice.period_end.later_than_period_start.$invalid">
                {{ $t("Has to be later than start of invoice period") }}
              </span>
            </div>
            <div class="form-group col-md-12">
              <small id="price_help" class="form-text text-muted">
                {{
                  $t("period-helptext")
                }}
              </small>
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
                    v-for="line in invoice.lines" :key="line.uid" :line="line"
                    @remove="removeLine(line.uid)" @update-line="updateLineItem"
                    ref="invoiceLines"
                />
                <input type="hidden" :class="{ 'is-invalid': v$.invoice.lines.$error }">
                <span class="invalid-feedback" v-if="v$.invoice.lines.required.$invalid">
                  {{ $t("At least one line is required") }}
                </span>
                <button type="button" @click="addLine" class="btn btn btn-info">{{ $t("Add line") }}</button>
              </div>
            </div>
          </div>

          <div id="div_id_vat_rate" class="form-group col-6" v-if="vatEnabled">
            <label for="id_vat_rate">{{ $t("VAT rate") }}</label>
            <div class="input-group">
              <input type="text" id="id_vat_rate" class="form-control"
                     v-model="vatRatePercent" @input="validateFloatValue">
              <div class="input-group-append">
                <span class="input-group-text">%</span>
              </div>
            </div>
            <small id="hint_id_vat_rate" class="form-text"
                   :class="vatWarning ? 'text-warning': 'text-muted'"
                   v-if="client.id && company.id"
            >
              <i class="bi bi-exclamation-triangle" v-if="vatWarning"></i>
              {{
                $t("Default VAT rate for {client} is {vatRate}%", {
                  "client": client.name,
                  "vatRate": client.vat_rate * 100
                })
              }}
            </small>
          </div>
          <hr>
          <dl class="row" v-if="vatEnabled">
            <dt class="col-3 text-right">{{ $t("Total before tax") }}</dt>
            <dd class="col-9 text-left">{{ currency }} {{ $formatAmount(invoice.subtotal) }}</dd>
            <dt class="col-3 text-right">{{ $t("VAT") }} ({{ vatRatePercent }}%)</dt>
            <dd class="col-9 text-left">{{ currency }} {{ $formatAmount(invoice.vat) }}</dd>
            <dt class="col-3 text-right">{{ $t("Total including tax") }}</dt>
            <dd class="col-9 text-left">{{ currency }} {{ $formatAmount(invoice.total) }}</dd>
          </dl>
          <dl class="row" v-else>
            <dt class="col-3 text-right">{{ $t("Total") }}</dt>
            <dd class="col-9 text-left">{{ currency }} {{ $formatAmount(invoice.total) }}</dd>
          </dl>
          <a href="#" @click.prevent="saveInvoice(true)" class="btn btn-primary">{{ $t('Save & Preview') }}</a>&nbsp;
          <a href="#" @click.prevent="saveInvoice(false)" class="btn btn-secondary">{{ $t('Save draft') }}</a>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import {nextTick} from 'vue'

import Decimal from 'decimal.js';
import moment from 'moment';
import {v4 as uuidv4} from 'uuid';
import {useI18n} from 'vue-i18n'
import {required, minValue, requiredIf, minLength} from '@vuelidate/validators'
import useValidate from "@vuelidate/core";

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
    vatWarning() {
      return this.vatEnabled && this.client && (this.invoice.vat_rate !== this.client.vat_rate);
    },
  },
  data() {
    return {
      companies: [],
      company: {},
      selectedCompanyName: '',
      clients: [],
      selectedClientName: '',
      client: {},
      invoice: {
        id: null,
        code: "",
        due_date: "",
        displayed_date: new Date(),
        vat_rate: 0.0,
        title: "",
        description: "",
        period_start: "",
        period_end: "",
        lines: [],
        subtotal: 0,
        vat: 0,
        total: 0,
      },
      vatEnabled: true,
      vatRatePercent: 7.7,
      urls: {
        companiesUrl: "",
        clientsUrl: "",
        invoiceUrl: "",
        invoicesUrl: "",
        linesUrl: "",
        previewUrl: "",
      },
      v$: useValidate(),
    }
  },
  methods: {
    addLine() {
      this.invoice.lines.push({
        description: "", quantity: 0.0, unit: "h",
        price_per_unit: this.client.default_hourly_rate, uid: uuidv4(), total: 0
      });
      this.$nextTick(() => {
        if (this.$refs.invoiceLines.length > 1)
          this.$refs.invoiceLines[this.$refs.invoiceLines.length - 1].focus();
      });
    },
    removeLine(uid) {
      const index = this.invoice.lines.findIndex(line => line.uid === uid);
      if (index !== -1) {
        // Remove the line from the invoice.lines array
        this.invoice.lines.splice(index, 1);
      }
      this.updateTotal();
    },

    focusFirstInvalidField() {
      const invalidContainers = document.querySelectorAll('.is-invalid');
      if (invalidContainers.length) {
        let input = invalidContainers[0].querySelector("input")
        if (input) {
          input.focus();
        } else {
          invalidContainers[0].focus();
        }
      }
    },
    formatDate(date) {
      const day = date.getDate();
      const month = date.getMonth() + 1;
      const year = date.getFullYear();
      return `${day}.${month}.${year}`;
    },

    handleClientSelect(client) {
      if (!client) {
        this.client = {};
        return;
      }
      // Handle client selection here
      this.fetchClient(client.id).then(() => {
        if (this.$refs.invoiceLines) {
          this.$refs.invoiceLines.forEach((line) => {
            if (line.localQuantity === 0) {
              line.localPrice = this.client.default_hourly_rate;
            }
          });
        }
        this.regenVat();
        this.vatRatePercent = this.invoice.vat_rate * 100;
        this.updateTotal();
      });
    },
    handleCompanySelect(company) {
      if (!company) {
        this.company = {};
        return;
      }
      this.fetchCompany(company.id).then(() => {
        this.regenVat();
        this.updateClientsList();
      });
    },
    async fetchCompany(companyId) {
      const response = await this.$http.get(`${this.urls.companiesUrl}${companyId}/`);
      this.company = response.data;
      this.selectedCompanyName = this.company.name;
      this.updateClientsList();
    },
    async fetchClient(clientId) {
      const response = await this.$http.get(`${this.urls.clientsUrl}${clientId}/`);
      this.client = response.data;
      this.selectedClientName = this.client.name;
      this.updateDueDate();
    },
    async fetchInvoice() {
      await this.$http.get(this.urls.invoiceUrl).then(response => {
        this.urls.previewUrl = response.data.preview_url;
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
          this.invoice.period_start = new Date(response.data.period_start);
        }
        if (response.data.period_end) {
          this.invoice.period_end = new Date(response.data.period_end);
        }
        this.invoice.lines = response.data.lines;
        this.invoice.lines.forEach((line) => {
          line.uid = uuidv4();
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

    async saveInvoice(redirect) {

      const validationResult = await this.v$.$validate();
      if (!validationResult) {
        nextTick(() => {
          this.focusFirstInvalidField();
        });
      } else {
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
        data["lines"] = this.invoice.lines;
        let success = false;
        if (this.urls.invoiceUrl) {
          // Update invoice
          await this.$http.patch(this.urls.invoiceUrl, data).then(response => {
            this.invoice.id = response.data.id;
            this.invoice.code = response.data.code;
            success = true;
          }).catch(error => {
            console.error(error)
          });
        } else {
          // Create new invoice
          await this.$http.post(this.urls.invoicesUrl, data).then(response => {
            this.urls.invoiceUrl = response.data.url;
            this.urls.previewUrl = response.data.preview_url;
            this.invoice.id = response.data.id;
            this.invoice.code = response.data.code;
            success = true;
          }).catch(error => {
            console.error(error)
          });
        }
        if (success && redirect) {
            window.location.href = this.urls.previewUrl;
        }
      }

    },
    regenVat() {
      this.vatEnabled = this.company.enable_vat;
      if (this.vatEnabled) {
        if (!this.invoice.vat_rate) {
          if (this.client.vat_rate) {
            this.invoice.vat_rate = this.client.vat_rate;
          } else {
            this.invoice.vat_rate = this.company.vat_rate;
          }
        }
      } else {
        this.invoice.vat_rate = 0.0;
      }
    },

    updateClientsList() {
      let url = this.urls.clientsUrl;
      if (this.company.id) {
        url += `?company_uuid=${this.company.id}`;
      }
      this.$http.get(url).then(response => {
        this.clients = response.data.results;
        if (this.clients.length === 1) {
          this.client = this.clients[0].id
          this.fetchClient(this.clients[0].id);
          this.regenVat();
        }
      }).catch(error => {
        console.error(error)
      });
    },
    updateCompaniesList() {
      let url = this.urls.companiesUrl;
      this.$http.get(url).then(response => {
        this.companies = response.data.results;
        if (this.companies.length === 1) {
          this.company = this.companies[0]
          this.selectedCompanyName = this.companies[0].name;
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
    },
    updateLineItem(updatedLine) {
      const index = this.invoice.lines.findIndex(line => line.uid === updatedLine.uid);
      if (index !== -1) {
        this.invoice.lines.splice(index, 1, updatedLine);
      }
      this.updateTotal();
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
    },
    updateTotal() {
      this.invoice.subtotal = this.invoice.lines.reduce((acc, line) => acc + line.total, 0);
      if (this.vatEnabled) {
        this.invoice.vat = this.invoice.subtotal * this.invoice.vat_rate;
      } else {
        this.invoice.vat = 0;
      }
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
      this.vatRatePercent = value;
      return value;
    },
  },

  mounted() {
    this.$i18n.locale = this.$el.parentNode.dataset.languageCode;
    this.urls.companiesUrl = this.$el.parentNode.dataset.companiesUrl;
    this.urls.clientsUrl = this.$el.parentNode.dataset.clientsUrl;
    this.urls.invoicesUrl = this.$el.parentNode.dataset.invoicesUrl;
    this.urls.invoiceUrl = this.$el.parentNode.dataset.invoiceUrl;
    this.urls.linesUrl = this.$el.parentNode.dataset.linesUrl;

    if (this.$el.parentNode.dataset.companyPk) {
      this.fetchCompany(this.$el.parentNode.dataset.companyPk);
    } else {
      this.updateClientsList();
    }
    if (this.$el.parentNode.dataset.clientPk) {
      this.fetchClient(this.$el.parentNode.dataset.clientPk);
    }
    if (this.urls.invoiceUrl) {
      this.fetchInvoice();
      this.updateTotal();
    }
    this.updateCompaniesList();
  },

  validations() {
    return {
      client: {required},
      company: {required},
      invoice: {
        displayed_date: {required},
        due_date: {
          required,
          later_than_displayed_date: minValue(this.invoice.displayed_date)
        },
        lines: {
          required,
          minLength: minLength(1)
        },
        period_start: {
          required_if_period_end: requiredIf(this.invoice.period_end)
        },
        period_end: {
          required_if_period_start: requiredIf(this.invoice.period_start),
          later_than_period_start: minValue(this.invoice.period_start),
        },
        title: {required},
      }
    }
  },

  watch: {
    vatRatePercent: function (value) {
      // Convert the value to a float and use toFixed(2) to limit decimal places to 4
      const decimalValue = new Decimal(value / 100);
      this.invoice.vat_rate = decimalValue.toFixed(4);
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

.is-invalid input.dp__input {
  border-color: var(--red);
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='none' stroke='%23e74a3b' viewBox='0 0 12 12'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23e74a3b' stroke='none'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right calc(0.375em + 0.1875rem) center;
  background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
  padding-right: calc(1.5em + 0.75rem) !important;
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
  display: none !important;
}
</style>
