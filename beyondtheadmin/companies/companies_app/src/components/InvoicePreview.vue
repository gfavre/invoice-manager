<template>
<div class="container invoice" :style="`--background-color: ${contrastColor}`">
  <div class="row">
    <div class="col-3" id="side">
      <h1>Invoice</h1>
      <div itemscope itemtype="http://schema.org/LocalBusiness" id="company-address">
        <span itemprop="name">{{ company.name }}</span> <br>

        <address itemprop="address" itemscope="" itemtype="http://schema.org/PostalAddress">
          <span itemprop="streetAddress">{{ company.address }}</span><br>
            <span itemprop="addressCountry" v-if="company.country">{{ company.country }}-</span><span
          itemprop="postalCode">{{ company.zipcode }}</span> <span
          itemprop="addressLocality">{{ company.city }}</span><br>
        </address>
        <div v-if="company.phone">
          <span v-if="!company.additionalPhone">Tél.</span>
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

        <div v-if="company.vatId">
          <span>TVA:</span> <span itemprop="vatID">{{ company.vatId }}</span>
          <br>
        </div>
        {{ company.iban }}
      </div>

    </div>
    <div class="col" id="content">
      <div class="row justify-content-end">
        <!--
        {% if invoice.company.logo %}
          <section class="col-12 text-right" id="logo"><img src="{% buildfullurl invoice.company.logo.url %}"></section>
        {% endif %}
        -->
        <section class="col-6" id="customer-address">
          <address>
            {{ client.name }}<br>
            {{ client.address  }}<br>
            {{ client.country }} - {{ client.zipCode }} {{ client.city }}
          </address>
          <p>{{ company.city }}, {{ invoice.date }}</p>
        </section>
      </div>

      <section id="invoice-content">
        <h3>{{ invoice.title }}</h3>
        <p>{{ invoice.description }}</p>
        <p>Travaux effectués entre le {{ invoice.period_start }} et le {{ invoice.period_end }}</p>

        <dl class="row">
          <dt class="col-3">{{ $t("Invoice ID") }}</dt>
          <dd class="col-9">
            {{ invoice.code }}</dd>
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
          <tr>
            <td colspan="4" class="text-right">{{ $t("Subtotal") }}</td>
            <td class="text-nowrap">CHF {{ $formatAmount(invoice.subtotal) }}</td>
          </tr>
          <tr v-if="vat_rate">
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
          {{ company.nameForBank }}, {{ company.zipcode }} {{ company.city }}<br>
          <span v-if="company.bank">{{ company.bank }}<br></span>
          <span v-if="company.swift">BIC: {{ company.swift }}<br></span>
          {{ company.iban }}
        </div>
      </section>
      <section class="mb-4" v-if="invoiceNote" v-html="invoiceNote"></section>
<section class="row">
  <div :class="{'col-6': hasSignature, 'col': !hasSignature}">
    <span v-if="thanksMessage" v-html="thanksMessage"></span>
    <span v-else>{{ $t("Thank you for your continued confidence.") }}</span>
  </div>
  <div v-if="hasSignature" class="col-6" id="signature">
    <img v-if="signatureImage" :src="signatureImage" id="signature-image">
    <p v-if="signatureText">{{ signatureText }}</p>
  </div>


</section>

<!--

        {% if invoice.company.has_signature %}
          <div class="col-6" id="signature">
            {% if invoice.company.signature_image %}
              <img src="{% buildfullurl invoice.company.signature_image.url %}" id="signature-image">
            {% endif %}
            {% if invoice.company.signature_text %}
              <p>{{ invoice.company.signature_text }}</p>
            {% endif %}
          </div>
        {% endif %}

      </section>
      -->

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
    "thanksMessage",
    "signatureText",
    "signatureImage",
  ],
  computed: {
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
      return this.invoice.subtotal + this.vat;
    },
    hasSignature() {
      return Boolean(this.signatureText || this.signatureImage)
    }
  },
  data() {
    return {
      client: {
        name: "Jean Dupont SA",
        address: "Route des Acacias 1",
        city: "Genève",
        zipCode: "1211",
        country: "CH"
      },
      invoice: {
        title: "Entretien de votre toiture",
        code: "dupont-003",
        date: "12 octobre 2023",
        due_date: "12 novembre 2023",
        description: "Les travaux d'entretien de toiture ont inclus le nettoyage, la vérification des gouttières, " +
          "la réparation de la cheminée, le remplacement de tuiles endommagées et l'application d'un traitement " +
          "hydrofuge. Ils ont été effectués par un couvreur qualifié.",
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
  }
}
</script>

<style scoped>
 body {
        font-family: Roboto, "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-size: 11pt;
        font-weight: 300;
        position: relative;

      }

      .invoice {
        border: 1px solid lightslategray;
      }

      .invoice a:link, .invoice a:visited, .invoice a:hover, .invoice a:active {
        color: var(--background-color);
      }

      .invoice h1 {
        font-size: 36pt;
        font-weight: 100;
        margin-top: 5.5cm;
      }

      .invoice h3 {
        font-size: 14pt;
        font-weight: 500;
      }

      .invoice dt, th {
        font-weight: 400;
      }

      .invoice .table {
        font-family: Roboto, "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-size: 11pt;
        font-weight: 300;
        width: 100%;
      }

      .invoice .table th {
        background-color: var(--background-color);
        color: white;
        border-right: 0.5px solid white;
        padding: 4pt;
        line-height: 12pt;
      }

      .invoice .table td {
        padding: 4pt;
        line-height: 12pt;
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
        top: 12.75cm;
        font-size: 10pt;
      }

      #logo img {
        height: 2.5cm;
      }

      #customer-address {
        margin-top: 3.5cm;
        height: 5cm;
      }

      #customer-address address {
        margin-bottom: 5rem;
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

      @media print {
        @page {
          size: 210mm 297mm;
          margin: 10mm 10mm 0mm 10mm;
        }

        .invoice {
          width: 210mm;
          margin-top: 10mm;
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
      }
</style>
