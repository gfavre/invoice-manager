<template>
  <nav class="toolbar">
    <div class="btn-group" role="group">
      <button
        type="button"
        class="btn"
        :class="{ active: activeSection === 'form' }"
        @click="setActiveSection('form')"
      >
        <i class="bi bi-pencil-fill"></i>
      </button>
      <button
        type="button"
        class="btn"
        :class="{ active: activeSection === 'both' }"
        @click="setActiveSection('both')"
      >
        <i class="bi bi-layout-split"></i>
      </button>
      <button
        type="button"
        class="btn"
        :class="{ active: activeSection === 'preview' }"
        @click="setActiveSection('preview')"
      >
        <i class="bi bi-eye-fill"></i>
      </button>
    </div>
  </nav>

  <div class="form-container" ref="container" :class="activeSection" :style="gridStyle">
    <div v-show="activeSection === 'form' || activeSection === 'both'" class="invoice-form" ref="form">
      <FileInput v-model="logo" @input="handleLogoInput" :label="$t('Logo')"></FileInput>
      <p v-if="logoFileName"><i class="bi bi-file-earmark-image"></i> {{ logoFileName }}</p>

      <div id="div_id_contrast_color" class="form-group">
        <FormKit type="color"
                 :label="$t('Contrast color')"
                 validation="required"
                 v-model="contrastColor"></FormKit>
      </div>

      <div id="div_id_invoice_note" class="form-group">
        <label for="id_invoice_note">{{ $t("Notes") }}</label>
        <Editor v-model="invoiceNote"
                api-key="nf16mminr724hh5tj7jgizwldbt3wy1rhmriy9trfwefr4wq"
                :init="tinyMCEConfig"/>
        <small id="hint_id_invoice_note" class="form-text text-muted">
          {{ $t("Displayed between banking details and signature") }}
        </small>
      </div>

      <div id="div_id_thanks" class="form-group">
        <label for="id_thanks">{{ $t("Thanks") }}</label>
        <Editor v-model="thanksMessage"
                api-key="nf16mminr724hh5tj7jgizwldbt3wy1rhmriy9trfwefr4wq"
                :init="tinyMCEConfig"/>

        <small id="hint_id_thanks" class="form-text text-muted">
          {{ $t("thanksMessageHelptext") }}
        </small>
      </div>

      <div id="div_id_signature_text" class="form-group">
        <label for="id_signature_text">{{ $t("Signature (text)") }}</label>
        <input type="text" name="signature_text" maxlength="100" id="id_signature_text"
               class="textinput textInput form-control"
               v-model="signatureText">
      </div>

      <div id="div_id_signature_image" class="form-group">
        <FileInput v-model="signatureImage"
                   @input="handleSignatureImageInput"
                   :label="$t('Signature (image)')"></FileInput>
        <p v-if="signatureFileName"><i class="bi bi-file-earmark-image"></i> {{ signatureFileName }}</p>
      </div>

      <div id="div_id_email_signature" class="form-group">
        <label for="id_email_signature">{{ $t("Signature (email)") }}</label>
        <textarea name="email_signature" cols="40" rows="10" id="id_email_signature"
                  class="textarea form-control"
                  v-model="emailSignature"
        ></textarea>
      </div>

      <div id="div_id_from_email" class="form-group">
        <label for="id_from_email" class="requiredField">
          {{ $t("Reply-to sender email") }}<span class="asteriskField">*</span>
        </label>
        <input type="text" name="from_email" maxlength="255" required="required"
               id="id_from_email" class="textinput textInput form-control"
               v-model="fromEmail">
      </div>

      <div id="div_id_bcc_email" class="form-group">
        <label for="id_bcc_email">{{ $t("BCC email") }}</label>
        <input type="email" name="bcc_email" maxlength="254" id="id_bcc_email" class="emailinput form-control"
               v-model="bccEmail"
        >
        <small id="hint_id_bcc_email" class="form-text text-muted">
          {{ $t("Address that would receive a copy of every outgoing email") }}
        </small>
      </div>


      <div class="buttonHolder">
        <input type="button" name="prev-3" :value="$t('Previous')" class="btn btn btn-secondary white"
               @click="handleSubmit(-1)"
        />
        <input type="submit" :value="$t('Save company')" class="btn btn btn-primary white"
               @click="handleSubmit()"
        />
      </div>
    </div>
    <div class="handle" ref="handle" @mousedown="startResizing" @click="toggleSection" :style="{cursor: handleCursor}">
      <i class="bi bi-arrow-left-right"></i>
    </div>
    <div v-show="activeSection === 'preview' || activeSection === 'both'" class="invoice-preview" ref="preview">
      <InvoicePreview :company="company"
                      :contrast-color="contrastColor" :invoice-note="invoiceNote"
                      :thanks-message="thanksMessage" :logo="logoUrl"
                      :signature-text="signatureText" :signature-image="signatureImageUrl"
      />
    </div>
  </div>

</template>

<script>
import Editor from '@tinymce/tinymce-vue'
import InvoicePreview from "@/components/InvoicePreview.vue";
import {useI18n} from 'vue-i18n'
import FileInput from './FileInput.vue';

export default {
  name: "InvoiceSettingsForm",
  components: {InvoicePreview, Editor, FileInput},
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
      logo: '',
      contrastColor: this.company.contrastColor || '#000000',
      invoiceNote: this.company.invoiceNote,
      thanksMessage: this.company.thanksMessage,
      signatureText: this.company.signatureText,
      signatureImage: '',
      emailSignature: this.company.emailSignature,
      fromEmail: this.company.fromEmail,
      bccEmail: this.company.bccEmail,

      activeSection: "both",
      isResizing: false,
      startX: 0,
      containerWidth: 0,
      formWidth: 0,
      previewWidth: 0,
    }
  },
  computed: {
    logoUrl() {
      if (!this.logo || !this.logo[0] || !this.logo[0].type) {
        return this.company.logo;
      }
      return URL.createObjectURL(this.logo[0]);
    },
    logoFileName(){
      if (!this.logo || !this.logo[0] || !this.logo[0].type) {
        return this.$filename(this.company.logo);
      }
      return this.logo[0].name;
    },
    signatureImageUrl() {
      if (!this.signatureImage || !this.signatureImage[0] || !this.signatureImage[0].type) {
        return this.company.signatureImage;
      }
      return URL.createObjectURL(this.signatureImage[0]);
    },
    signatureFileName(){
      if (!this.signatureImage || !this.signatureImage[0] || !this.signatureImage[0].type) {
        return this.$filename(this.company.signatureImage);
      }
      return this.signatureImage[0].name;
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
    },
    gridStyle() {
      switch (this.activeSection) {
        case 'form':
          return {
            gridTemplateColumns: '1fr 24px 0',
          }
        case 'preview':
          return {
            gridTemplateColumns: '0 24px 1fr',
          }
        default:
          return {
            gridTemplateColumns: '1fr 24px 2fr',
          }
      }
    },

    handleCursor() {
      return this.activeSection === 'both' ? 'col-resize' : 'pointer';
    },
  },
  methods: {
    async uploadImage(url, file){
      const fileObj = file[0];
      if (!fileObj) {
        return;
      }
      try {
        await this.$http.put(url, fileObj, {
          headers: {
            'Content-Type': fileObj.type,
            'X-File-Name': fileObj.name,
          },
        });
      } catch (e) {
        console.log(e);
      }
    },
    async uploadLogo() {
      await this.uploadImage(this.updateLogoUrl, this.logo);
    },
    async uploadSignatureImage(){
      await this.uploadImage(this.updateSignatureImageUrl, this.signatureImage);
    },
    handleLogoInput(files) {
      this.logo = files;
    },
    handleSignatureImageInput(files) {
      this.signatureImage = files;
    },

    async handleSubmit(step) {
      if (this.logo) {
        await this.uploadLogo();
      }
      if (this.signatureImage) {
        await this.uploadSignatureImage();
      }
      if (step === -1) {
        this.$emit("prev");
      } else {
        this.$emit("submit");
      }
    },

    setActiveSection(section) {
      this.$refs.form.style = '';
      this.$refs.preview.style = '';
      this.activeSection = section;
    },
    startResizing(e) {
      if (!this.activeSection === 'both') {
        return;
      }
      this.isResizing = true;
      this.startX = e.clientX;
      this.containerWidth = this.$refs.container.offsetWidth;
      this.formWidth = this.$refs.form.offsetWidth;
      this.previewWidth = this.$refs.preview.offsetWidth;

      document.addEventListener("mousemove", this.resize);
      document.addEventListener("mouseup", this.stopResizing);
    },
    resize(e) {
      if (!this.isResizing) {
        return;
      }

      const delta = e.clientX - this.startX;
      const newFormWidth = this.formWidth + delta;
      const newPreviewWidth = this.previewWidth - delta;
      if (newFormWidth < 200 || newPreviewWidth < 200) {
        return;
      }
      this.$refs.form.style.width = `${newFormWidth}px`;
      this.$refs.preview.style.width = `${newPreviewWidth}px`;
    },
    stopResizing() {
      this.isResizing = false;
      this.formWidth = this.$refs.form.offsetWidth;
      this.previewWidth = this.$refs.preview.offsetWidth;
      document.removeEventListener("mousemove", this.resize);
      document.removeEventListener("mouseup", this.stopResizing);
    },
    toggleSection() {
      if (this.activeSection !== 'both') {
        this.setActiveSection('both');
      }
    }
  },
}
</script>


<style >
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


</style>
<style scoped>

.toolbar {
  background-color: #f5f5f5;
  padding: 10px;
}

.toolbar .btn {
  background-color: transparent;
  border: 1px solid #0077cc;
    align-items: center;
  display: inline-flex;

}

.toolbar .btn.active {
  background-color: #0077cc;
  color: #fff;
}

.btn-group .bi {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  line-height: 1;
}

.btn-group .btn:not(:last-child) {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}

.btn-group .btn:not(:first-child) {
  margin-left: -1px;
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}

.btn.active {
  background-color: #007bff;
  color: #fff;
}

.form-container {
  display: grid;
  grid-template-areas: "form handle preview";
  position: relative;
}

.invoice-form {
  grid-area: form;
  overflow: hidden;
  resize: horizontal;
  min-width: 0;
  background-color: #fff;
  cursor: auto;
  padding: 0 1em;
  border-right: 1px solid #e0e0e0;
}

.handle {
  grid-area: handle;
  cursor: col-resize;
  width: 24px;
  height: 100%;
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  display: flex;
  padding-top: 10em;
  font-size: 0.8em;
  align-items: start;
  justify-content: center;
//background-color: #f5f5f5;
  color: #0077cc;

  box-shadow: 4px 4px 6px #e0e0e0;
}

.invoice-preview {
  grid-area: preview;
  overflow: hidden;
  resize: horizontal;
  min-width: 0;
  background-color: #fff;
  cursor: auto;
  border: 1px solid lightslategray;
  border-left: none;

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
