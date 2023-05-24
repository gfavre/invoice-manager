<template>

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
  <div id="div_id_email_signature" class="form-group">
    <label for="id_email_signature">{{ $t("Signature (email)") }}</label>
    <textarea name="email_signature" cols="40" rows="10" id="id_email_signature"
              class="textarea form-control"
              v-model="emailSignature"
    ></textarea>
  </div>


  <div class="buttonHolder">
    <input type="button" name="prev-3" :value="$t('Previous')" class="btn btn btn-secondary white"
           @click="handleSubmit(-1)"
    />
    <input type="submit" :value="$t('Save company')" class="btn btn btn-primary white"
           @click="handleSubmit()"
    />
  </div>

</template>

<script>
export default {
  name: "InvoiceEmailForm",
  props: {
    company: {
      type: Object,
      required: true,
    },
    onUpdate: {
      type: Function,
      required: true
    },
  },
  emits: ["prev", "next"],
  data: function () {
    return {
      emailSignature: this.company.emailSignature,
      fromEmail: this.company.fromEmail,
      bccEmail: this.company.bccEmail,
    }
  },
  methods: {
    handleSubmit(step) {
      if (step === -1) {
        this.$emit("prev");
      } else {
        this.$emit("submit");
      }
    }
  }
}
</script>

<style scoped>


</style>
