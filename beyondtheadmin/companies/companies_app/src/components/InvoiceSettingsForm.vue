<template>
  <div class="form-container" ref="container">
    <div class="invoice-form" ref="form">
      <FormKit type="file" :label="$t('Logo')"
               accept=".jpg,.png,.gif,.svg"
               multiple="false"
               v-model="logo"

      ></FormKit>

      <div id="div_id_contrast_color" class="form-group">
        <FormKit type="color"
                 :label="$t('Contrast color')"
                 validation="required"
                 v-model="contrastColor"></FormKit>
      </div>

      <div id="div_id_invoice_note" class="form-group">
        <label for="id_invoice_note">Remarques</label>
        <Editor v-model="invoiceNote"
                api-key="nf16mminr724hh5tj7jgizwldbt3wy1rhmriy9trfwefr4wq"
                :init="tinyMCEConfig"/>
        <small id="hint_id_invoice_note" class="form-text text-muted">Affiché entre les coordonnées bancaires et la
          signature</small>
      </div>

      <div id="div_id_thanks" class="form-group">
        <label for="id_thanks">Merci</label>
        <Editor v-model="thanksMessage"
                api-key="nf16mminr724hh5tj7jgizwldbt3wy1rhmriy9trfwefr4wq"
                :init="tinyMCEConfig"/>

        <small id="hint_id_thanks" class="form-text text-muted">
          Remerciements au bas de la facture. Si cette option est activée, elle figurera sur toutes les factures,
          quelle que soit la langue
        </small>
      </div>

      <div id="div_id_signature_text" class="form-group">
        <label for="id_signature_text">Signature sous forme de texte</label>
        <input type="text" name="signature_text" maxlength="100" id="id_signature_text"
               class="textinput textInput form-control"
               v-model="signatureText">
      </div>

      <div id="div_id_signature_image" class="form-group">
        <label for="id_signature_image">Signature sous forme d'image</label>
        <div class="mb-2">
          <div class="form-control custom-file" style="border: 0px;"><input type="file" name="signature_image"
                                                                            accept="image/*" id="id_signature_image"
                                                                            class="custom-file-input"> <label
              for="id_signature_image" class="custom-file-label text-truncate">---</label></div>
        </div>
      </div>

      <div id="div_id_email_signature" class="form-group">
        <label for="id_email_signature">Signature e-mail</label>
        <textarea name="email_signature" cols="40" rows="10" id="id_email_signature"
                  class="textarea form-control"></textarea>
      </div>

      <div id="div_id_from_email" class="form-group">
        <label for="id_from_email" class="requiredField">
          Email de l’expéditeur<span class="asteriskField">*</span>
        </label>
        <input type="text" name="from_email" value=" <greg@beyondthewall.ch>" maxlength="255" required="required"
               id="id_from_email" class="textinput textInput form-control">
      </div>

      <div id="div_id_bcc_email" class="form-group">
        <label for="id_bcc_email">Copie des factures</label>
        <input type="email" name="bcc_email" maxlength="254" id="id_bcc_email" class="emailinput form-control">
        <small id="hint_id_bcc_email" class="form-text text-muted">
          Adresse e-mail qui recevra chaque facture envoyée en bcc
        </small>
      </div>


      <div class="buttonHolder">
        <input type="button" name="prev-3" value="Précédent" class="btn btn btn-secondary white"
               @click="handleSubmit(-1)"
        />
        <input type="submit" value="Enregistrer" class="btn btn btn-primary white"
               @click="handleSubmit()"
        />
      </div>
    </div>

    <div class="invoice-preview" ref="preview">
      <InvoicePreview :company="company"
                      :contrast-color="contrastColor" :invoice-note="invoiceNote"
                      :thanks-message="thanksMessage" :logo="logo"
                      :signature-text="signatureText" :signature-image="signatureImage"
      />
    </div>
  </div>

</template>

<script>
import Editor from '@tinymce/tinymce-vue'
import InvoicePreview from "@/components/InvoicePreview.vue";
import {useI18n} from 'vue-i18n'

export default {
  name: "InvoiceSettingsForm",
  components: {InvoicePreview, Editor},
  props: {
    company: {
      type: Object,
      required: true,
    },
    updateLogoUrl: {
      type: String,
      required: true
    },
    updateSignatureImageUrl: {
      type: String,
      required: true
    },
    onUpdate: {
      type: Function,
      required: true
    },
  },

  emits: ["prev", "submit"],

  data: function () {
    return {
      logo: this.company.logo,
      contrastColor: this.company.contrastColor || '#000000',
      invoiceNote: this.company.invoiceNote,
      thanksMessage: this.company.thanksMessage,
      signatureText: this.company.signatureText,
      signatureImage: this.company.signatureImage,
    }
  },
  computed: {
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
          return '';
      }
    },
    tinyMCEConfig() {
      let config = {
        height: '16em',
        menubar: false,
        plugins: [
          'lists', 'link', 'searchreplace'
        ],
        toolbar:
          'undo redo | bold italic underline strikethrough | forecolor |\
          bullist numlist outdent indent | removeformat'
      }
      let language = this.tinyMCELang
      if (language) {
        config.language = language
      }
      return config
    }
  },
  methods: {
    async uploadLogo() {
      const logo = this.logo[0];
      if (!logo) {
        console.log('No file selected.');
        return;
      }
      try {
        await this.$http.put(this.updateLogoUrl, logo.file, {
          headers: {
            'Content-Type': logo.file.type,
            'X-File-Name': logo.file.name,
          },
        });
      } catch (e) {
        console.log(e);
      }
    },
    handleSubmit(step) {
      if (this.logo) {
        this.uploadLogo();
      }
      /*this.onUpdate({
        logo: this.logo,
      });*/
      if (step === -1) {
        this.$emit("prev");
      } else {
        this.$emit("submit");
      }
    }
  },
  mounted() {
    const container = this.$refs.container;
    const form = this.$refs.form;
    const preview = this.$refs.preview;
    //let isResizing = false;
    let lastX = 0;
    //let containerWidth = container.offsetWidth;
    let formWidth = form.offsetWidth;
    let previewWidth = preview.offsetWidth;

    const onMouseMove = (e) => {
      const delta = e.clientX - lastX;
      const newFormWidth = formWidth + delta;
      const newPreviewWidth = previewWidth - delta;

      form.style.width = `${newFormWidth}px`;
      preview.style.width = `${newPreviewWidth}px`;
    };

    const onMouseUp = () => {
      //isResizing = false;
      container.style.cursor = null;
      container.style.boxShadow = null;

      container.removeEventListener("mousemove", onMouseMove);
      container.removeEventListener("mouseup", onMouseUp);
    };

    container.addEventListener("mousedown", (e) => {
      //isResizing = true;
      lastX = e.clientX;
      container.style.cursor = "col-resize";
            container.style.boxShadow = "0 0 10px rgba(0, 0, 0, 0.2)";

      container.addEventListener("mousemove", onMouseMove);
      container.addEventListener("mouseup", onMouseUp);
    });

  }
}
</script>

<style scoped>
.tox.tox-tinymce {
  border: 1px solid #d1d3e2;
  border-radius: 0.35rem;
}

.tox.tox-tinymce .tox-editor-header {
  box-shadow: none !important;
  border-bottom: 1px solid #d1d3e2 !important;
}

.tox-tinymce .tox-statusbar__branding {
  display: none;
}
.highlight {
  background-color: #f0f0f0;
}

.form-container {
  display: grid;
  grid-template-columns: 1fr 3fr;
  grid-template-areas: "form preview";
  grid-gap: 10px;
  background-color: #f5f5f5;
  cursor: col-resize;


}
.invoice-form {
  background-color: #fff;
  grid-area: form;
  overflow: hidden;
  resize: horizontal;
  min-width: 0;
    cursor: auto;

}
.invoice-preview {
    background-color: #fff;

  grid-area: preview;
  overflow: hidden;
  resize: horizontal;
  min-width: 0;
    cursor: auto;

}
@media (max-width: 768px) {
  .form-container {
    grid-template-columns: 1fr;
    grid-template-areas:
      "form"
      "preview";
  }

  .invoice-form,
  .invoice-preview {
    resize: none;
  }
}

</style>
