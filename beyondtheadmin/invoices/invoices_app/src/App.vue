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
      <div class="datatable card">
        <div class="card-body">
          <form>
            <div class="form-row form-row">
              <div class="form-group col-md-6 mb-0">
                <div id="div_id_company" class="form-group">
                  <label for="id_company" class=" requiredField">
                  Entreprise<span class="asteriskField">*</span> </label>
                  <div>
                    <select name="company" class="select custom-select" id="id_company">
                      <option v-for="company in companies"
                              :key="company.id"
                              :value="company.id">{{ company.name }}</option>
                    </select>
                  </div>
                </div>
              </div>
              <div class="form-group col-md-6 mb-0">
                <div id="div_id_client" class="form-group">
                  <label for="id_client" class=" requiredField">Client<span class="asteriskField">*</span> </label>
                  <div>
                    <select name="company" class="select custom-select" id="id_company">
                      <option v-for="client in clients"
                              :key="client.id"
                              :value="client.id">{{ client.name }}</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
            <div class="form-row form-row">
              <div class="form-group col-md-6 mb-0">
                <div id="div_id_displayed_date" class="form-group">
                  <label for="id_displayed_date" class="">
                    Date affichée
                  </label>
                  <div>
                    <div class="input-group date">
                      <input type="text" name="displayed_date" value="16.03.2023"
                             class="form-control datepickerinput" id="id_displayed_date">
                      <div class="input-group-addon input-group-append" data-target="#datetimepicker1"
                           data-toggle="datetimepickerv">
                        <div class="input-group-text">
                          <i class="glyphicon glyphicon-calendar"></i>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="form-group col-md-6 mb-0">
                <div id="div_id_due_date" class="form-group"><label for="id_due_date" class=" requiredField">
                  Date d'échéance<span class="asteriskField">*</span> </label>
                  <div>
                    <div class="input-group date">
                      <input type="text" name="due_date"
                             value="(datetime.datetime(2023, 4, 15, 16, 40, 25, 150590, tzinfo=<UTC>),)"
                             class="form-control datepickerinput" required=""
                             id="id_due_date">
                      <div class="input-group-addon input-group-append" data-target="#datetimepicker1"
                           data-toggle="datetimepickerv">
                        <div class="input-group-text"><i class="glyphicon glyphicon-calendar"></i></div>
                      </div>
                    </div>
                  </div>
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
              <div>
                <div class="django-ckeditor-widget" data-field-id="id_description" style="display: inline-block;">
                  <textarea class="ckeditorwidget form-control" cols="40" id="id_description" name="description"
                            rows="10" data-processed="1"
                            data-config="{&quot;skin&quot;: &quot;moono-lisa&quot;, &quot;toolbar_Basic&quot;: [[&quot;Source&quot;, &quot;-&quot;, &quot;Bold&quot;, &quot;Italic&quot;]], &quot;toolbar_Full&quot;: [[&quot;Styles&quot;, &quot;Format&quot;, &quot;Bold&quot;, &quot;Italic&quot;, &quot;Underline&quot;, &quot;Strike&quot;, &quot;SpellChecker&quot;, &quot;Undo&quot;, &quot;Redo&quot;], [&quot;Link&quot;, &quot;Unlink&quot;, &quot;Anchor&quot;], [&quot;Image&quot;, &quot;Flash&quot;, &quot;Table&quot;, &quot;HorizontalRule&quot;], [&quot;TextColor&quot;, &quot;BGColor&quot;], [&quot;Smiley&quot;, &quot;SpecialChar&quot;], [&quot;Source&quot;]], &quot;toolbar&quot;: &quot;Full&quot;, &quot;height&quot;: 291, &quot;width&quot;: 835, &quot;filebrowserWindowWidth&quot;: 940, &quot;filebrowserWindowHeight&quot;: 725, &quot;language&quot;: &quot;fr&quot;}"
                            data-external-plugin-resources="[]" data-id="id_description" data-type="ckeditortype"
                            style="visibility: hidden; display: none;"></textarea>
                </div>
              </div>
            </div>
            <div class="form-row form-row">
              <div class="form-group col-md-6 mb-0">
                <div id="div_id_period_start" class="form-group"><label for="id_period_start" class="">
                  Début de la période de facturation
                </label>
                  <div>
                    <div class="input-group date"><input type="text" name="period_start"
                                                         class="form-control datepickerinput" id="id_period_start"
                                                         dp_config="{&quot;id&quot;: &quot;dp_3&quot;, &quot;picker_type&quot;: &quot;DATE&quot;, &quot;linked_to&quot;: null, &quot;options&quot;: {&quot;showClose&quot;: true, &quot;showClear&quot;: true, &quot;showTodayButton&quot;: true, &quot;format&quot;: &quot;DD.MM.YYYY&quot;, &quot;locale&quot;: &quot;fr&quot;}}">
                      <div class="input-group-addon input-group-append" data-target="#datetimepicker1"
                           data-toggle="datetimepickerv">
                        <div class="input-group-text"><i class="glyphicon glyphicon-calendar"></i></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="form-group col-md-6 mb-0">
                <div id="div_id_period_end" class="form-group"><label for="id_period_end" class="">
                  Fin de la période de facturation
                </label>
                  <div>
                    <div class="input-group date"><input type="text" name="period_end"
                                                         class="form-control datepickerinput" id="id_period_end"
                                                         dp_config="{&quot;id&quot;: &quot;dp_4&quot;, &quot;picker_type&quot;: &quot;DATE&quot;, &quot;linked_to&quot;: null, &quot;options&quot;: {&quot;showClose&quot;: true, &quot;showClear&quot;: true, &quot;showTodayButton&quot;: true, &quot;format&quot;: &quot;DD.MM.YYYY&quot;, &quot;locale&quot;: &quot;fr&quot;}}">
                      <div class="input-group-addon input-group-append" data-target="#datetimepicker1"
                           data-toggle="datetimepickerv">
                        <div class="input-group-text"><i class="glyphicon glyphicon-calendar"></i></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div id="div_id_vat_rate" class="form-group">
              <label for="id_vat_rate" class="">Taux de TVA</label>
              <div>
                <input type="number" name="vat_rate" value="0.0770" step="0.0001" class="numberinput form-control" id="id_vat_rate">
              </div>
            </div>
            <div class="card border-left-info shadow mb-3">
              <div class="card-body"><h5 class="text-xs font-weight-bold text-info text-uppercase mb-4">Lignes</h5>
                <div class="lines">

                  <div id="add-line" class="pt-2"><input type="button" name="add" value="Ajouter une ligne"
                                                         class="btn btn btn-info" id="button-id-add">

                  </div>

                </div>

              </div>
              <div><input type="submit" name="save" value="Enregistrer" class="btn btn-primary" id="submit-id-save">

              </div>
            </div>
          </form>


        </div>
      </div>
    </section>
  </div>


  <div class="invoice-form">
    <h1>Create Invoice</h1>
    <div v-for="line in invoice.lines" :key="line.id">
      <invoice-line
          :line-id="line.id"
          :initial-description="line.description"
          :initial-quantity="line.quantity"
          :initial-price="line.price"
          @update-line="handleUpdateLine"
      />
    </div>
    <button @click="addLine">Add Line</button>
  </div>
</template>

<script>
import InvoiceLine from './components/InvoiceLine.vue'

export default {
  name: 'App',
  components: {
    InvoiceLine
  },
  data() {
    return {
      companies: [],
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
      clients: [
        {
          id: 1,
          name: 'Client 1',
        },
        {
          id: 2,
          name: 'Client 2',
        },
        {
          id: 3,
          name: 'Client 3',
        }

      ],
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
        code: "",
        due_date: "",
        displayed_date: "",
        vat_rate: 0.077,
        total: 0,
        title: "",
        description: "",
        period_start: "",
        period_end: "",
        lines: [],
      },
      urls: {
        companiesUrl: "",
      },
    }
  },
  methods: {
    addLine() {
      this.invoice.lines.push({
        id: this.invoice.lines.length + 1,
        description: "",
        quantity: 0,
        price: 0,
      })
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

  }
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
