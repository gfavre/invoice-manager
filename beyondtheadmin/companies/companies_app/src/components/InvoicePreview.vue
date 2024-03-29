<template>
  <div class="body">

  <div class="container invoice" :style="`--background-color: ${contrastColor}`">
    <div class="row">
      <div class="col-3" id="side">
        <h1>{{ $t("Invoice") }}</h1>
        <div itemscope itemtype="http://schema.org/LocalBusiness" id="company-address">
          <span itemprop="name">{{ company.name }}</span> <br>

          <address itemprop="address" itemscope="" itemtype="http://schema.org/PostalAddress">
            <span itemprop="streetAddress">{{ company.address }}</span><br>
            <span itemprop="addressCountry" v-if="displayCountry">{{ company.country }}-</span><span
              itemprop="postalCode">{{ company.zipCode }}</span> <span
              itemprop="addressLocality">{{ company.city }}</span><br>
          </address>
          <div v-if="company.phone">
            <span v-if="!company.additionalPhone">{{ $t("Tel") }}</span>
            {{ company.phone }}
            <br>
          </div>

          <div v-if="company.additionalPhone">
            {{ company.additional_phone }}
            <br>
          </div>

          <div v-if="company.email">
            <a href="mailto:{{ company.email }}" itemprop="email">{{ company.email }}</a><br>
          </div>

          <div v-if="company.website">
            <a href="{{ company.website_url }}">{{ company.website }}</a><br>
          </div>

          <div v-if="company.vatEnabled && company.vatId">
            <span>{{ $t("UID") }}:</span> <span itemprop="vatID">{{ company.vatId }}</span>
            <br>
          </div>
          <div v-else-if="company.vatId">
            <span>{{ $t("IDE") }}:</span> <span itemprop="vatID">{{ company.vatId }}</span>
            <br>
          </div>
        </div>

      </div>
      <div class="col-9" id="content">
        <div class="row justify-content-end">
          <section class="col-12 text-right" id="logo" v-if="logo">
            <img :src="logo">
          </section>
          <section class="col-12 text-right" id="logo" v-else>
            <div class="fake-img"></div>
          </section>

          <section class="col-6" id="customer-address">
            <address>
              {{ client.name }}<br>
              {{ client.contactPerson }}<br>
              {{ client.address }}<br>
              <span v-if="displayCountry">{{ client.country }} - </span>{{ client.zipCode }} {{ client.city }}
            </address>
            <p>{{ company.city }}, {{ invoice.date }}</p>
          </section>
        </div>

        <section id="invoice-content">
          <h3>{{ invoice.title }}</h3>
          <p>{{ invoice.description }}</p>
          <p>{{ $t("workDone", {start: invoice.period_start, end: invoice.period_end})}}</p>

          <dl class="row">
            <dt class="col-3">{{ $t("Invoice ID") }}</dt>
            <dd class="col-9">
              {{ invoice.code }}
            </dd>
            <dt class="col-3">{{ $t("Due date") }}</dt>
            <dd class="col-9">{{ invoice.due_date }}</dd>

          </dl>
          <table class="table">
            <thead>
            <tr>
              <th>{{ $t("Description") }}</th>
              <th>{{ $t("Quantity") }}</th>
              <th>{{ $t("Unit") }}</th>
              <th>{{ $t("Unit price") }}</th>
              <th>{{ $t("Cost") }}</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="line in invoice.lines" :key="line.id">
              <td>{{ line.description }}</td>
              <td class="text-nowrap">
                {{ line.quantity }}
              </td>
              <td class="text-nowrap">{{ line.unit }}</td>
              <td class="text-nowrap">CHF {{ $formatAmount(line.pricePerUnit) }}</td>
              <td class="text-nowrap">CHF {{ $formatAmount(line.total) }}</td>
            </tr>
            </tbody>
            <tfoot>
            <tr v-if="company.vatEnabled && vat_rate">
              <td colspan="4" class="text-right">{{ $t("Subtotal") }}</td>
              <td class="text-nowrap">CHF {{ $formatAmount(invoice.subtotal) }}</td>
            </tr>
            <tr v-if="company.vatEnabled && vat_rate">
              <td colspan="3" class="text-right">{{ $t("VAT") }}</td>
              <td class="text-nowrap">{{ vat_rate }}%</td>
              <td class="text-nowrap">CHF {{ $formatAmount(vat) }}</td>
            </tr>
            <tr>
              <th colspan="4" class="text-right">{{ $t("Total") }}</th>
              <th class="text-nowrap">CHF {{ $formatAmount(total) }}</th>
            </tr>
            </tfoot>
          </table>
        </section>

        <section class="row" id="bank">
          <div class="col-6">{{ $t("Bank details") }}</div>
          <div class="col-6">
            {{ company.nameForBank }}, {{ company.zipCode }} {{ company.city }}<br>
            <span v-if="company.bank" v-html="formattedBank"></span>
            <span v-if="company.swift"><br>BIC: {{ company.swift }}<br></span>
            {{ company.iban }}
          </div>
        </section>
        <section class="mb-4" v-if="invoiceNote" v-html="invoiceNote"></section>
        <section class="row">
          <div :class="{'col-6': hasSignature, 'col': !hasSignature}">
            <span v-if="thanksMessage" v-html="thanksMessage"></span>
            <span v-else>{{ $t("defaultInvoiceThanks") }}</span>
          </div>
          <div v-if="hasSignature" class="col-6" id="signature">
            <img v-if="signatureImage" :src="signatureImage" id="signature-image">
            <p v-if="signatureText">{{ signatureText }}</p>
          </div>
        </section>
      </div>
    </div>
  </div>
      </div>

</template>

<script>
export default {
  name: "InvoicePreview",
  props: [
    "company",
    "contrastColor",
    "invoiceNote",
    "logo",
    "thanksMessage",
    "signatureText",
    "signatureImage",
  ],
  computed: {
    displayCountry() {
      return this.company.country !== "CH";
    },
    vat_rate() {
      if (!this.company.vatId) {
        return 0;
      }
      return 7.7;
    },
    vat() {
      return this.invoice.subtotal * this.vat_rate / 100;
    },
    total() {
      if (this.vatEnabled){
        return this.invoice.subtotal + this.vat;
      }
      return this.invoice.subtotal;
    },
    hasSignature() {
      return Boolean(this.signatureText || this.signatureImage)
    },
    formattedBank() {
      return this.company.bank.replace(/\n/g, "<br>");
    }
  },
  data() {
    return {
      client: {
        name: "Metallic SA",
        contactPerson: "M. Jean Dupont",
        address: "Route des Acacias 1",
        city: "Genève",
        zipCode: "1211",
        country: "CH"
      },
      invoice: {
        title: this.$t("invoiceTitle"),
        code: "dupont-003",
        date: "12 octobre 2023",
        due_date: "12 novembre 2023",
        description: this.$t("invoiceDescription"),
        period_start: "1er septembre 2023",
        period_end: "15 septembre 2023",
        lines: [
          {
            description: "Nettoyage de la toiture",
            quantity: 1,
            unit: "h",
            pricePerUnit: 80,
            total: 80
          },
          {
            description: "Réparation de la cheminée",
            quantity: 1,
            unit: "pièce",
            pricePerUnit: 100,
            total: 100
          },
          {
            description: "Remplacement de tuiles",
            quantity: 5,
            unit: "pièce",
            pricePerUnit: 10,
            total: 50
          },
          {
            description: "Traitement hydrofuge",
            quantity: 1.5,
            unit: "h",
            pricePerUnit: 80,
            total: 120
          }
        ],
        subtotal: 350,
      },
    }
  },
  methods: {
    formatAmount(floatValue) {
      let formatted = floatValue.toFixed(2);
      formatted = formatted.replace(/\.00$/, '.-');
      return formatted;
    }
  },

}
</script>

<style scoped>
.row {
  margin-left: -15px;
  margin-right: -15px;
}
.container {
  padding-right: 15px;
  padding-left: 15px;
}
.body {
  font-family: Roboto, "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 9.3pt;
  font-weight: 300;
  position: relative;
  color: #000;

}
.invoice{
   padding: 10mm 10mm 0 10mm;
}
.invoice a:link, .invoice a:visited, .invoice a:hover, .invoice a:active {
  color: var(--background-color);
}

.invoice h1 {
  font-size: 3.25em;
  font-weight: 100;
  margin-top: 5.5cm;
}

.invoice h3 {
  font-size: 1.25em;
  font-weight: 500;
}

.invoice dt, th {
  font-weight: 400;
}

.invoice .table {
  font-family: Roboto, "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 1em;
  font-weight: 300;
  width: 100%;
}

.invoice .table th {
  background-color: var(--background-color);
  color: white;
  border-right: 0.5px solid white;
  padding: .35em;
  line-height: 1.1em;
}

.invoice .table td {
  padding: .35em;
  line-height: 1.1em;
}

.invoice .table thead th {
  text-align: center;
}

.invoice .table td:first-child {
  text-align: left;
}

.invoice .table td, table tfoot th {
  text-align: right;
}

.invoice .table tbody tr:nth-child(even) {
  background-color: #f2f2f2;
}

.invoice tfoot tr:first-child td {
  border-top: 1px solid var(--background-color);;
}

#company-address {
  position: absolute;
  top: 11.45cm;
  font-size: 0.9em;
}

#logo img, #logo .fake-img {
  height: 2.5cm;
}

#customer-address {
  margin-top: 3.0cm;
  height: 4.5cm;
}

#customer-address address {
  margin-bottom: 4.5rem;
}
#customer-address p {
  margin-bottom: 0;
}

#invoice-content {
  margin-top: 0.7cm;
}

#bank {
  margin-bottom: 1cm;
}

#signature {
  margin-top: 1cm;
  margin-bottom: 2cm;
}

#signature-image {
  width: 5cm;
}

#qrbill, #qrbill svg {
  width: 100%;
  padding: 0;
}

.invoice abbr[title] {
  border-bottom: none !important;
  cursor: inherit !important;
  text-decoration: none !important;
}

section {
  width: 100%;
}


  a:not(.btn) {
    text-decoration: none;
    color: #000;
  }

  .invoice .table th {
    background-color: var(--background-color) !important;
    color: #fff;
  }

  #invoice-content .table td {
    padding-right: 15px;
  }

  #qrbill svg {
    padding: 0;
    margin-top: 17mm;
    height: auto !important;
    position: absolute;
    bottom: 0;
  }

  #qrbill {
    margin-top: 17mm;
    page-break-inside: avoid;
    bottom: 10px;
    position: static;
    min-height: 136vh;
  }

</style>
