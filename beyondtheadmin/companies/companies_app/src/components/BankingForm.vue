<template>
  <div id="div_id_vat_id" class="form-group">
    <label for="id_vat_id">N° de TVA</label>
    <div>
      <input type="text" name="vatId" maxlength="20" id="id_vat_id" class="textinput textInput form-control">
    </div>
  </div>

  <div class="form-row">
    <div class="col-md-6">
      <div id="div_id_iban" class="form-group">
        <label for="id_iban">IBAN</label>
        <div>
          <input type="text" name="iban" maxlength="34" minlength="15" id="id_iban" class="textinput textInput form-control">
        </div>
      </div>
    </div>
    <div class="col-md-6">
      <div id="div_id_name_for_bank" class="form-group">
        <label for="id_name_for_bank">Nom du propriétaire du compte bancaire</label>
        <input type="text" name="name_for_bank" maxlength="255" id="id_name_for_bank" class="textinput textInput form-control">
      </div>
    </div>
  </div>

  <div class="form-row">
    <div class="col-9">
      <div id="div_id_bank" class="form-group">
        <label for="id_bank">Banque</label>
        <textarea name="bank" cols="40" rows="3" id="id_bank" class="textarea form-control"></textarea>
      </div>
    </div>
    <div class="col">
      <div id="div_id_bic" class="form-group">
        <label for="id_bic">BIC</label>
        <input type="text" name="bic" maxlength="11" id="id_bic" class="textinput textInput form-control">
      </div>
    </div>
  </div>

  <div class="buttonHolder">
    <input type="button" name="prev-2" value="Précédent" class="btn btn btn-secondary white">
    <input type="button" name="next-2" value="Suivant" disabled="disabled" class="btn btn btn-primary white">
  </div>
</template>

<script>
export default {
  name: "BankingForm",
  props: ['company'],
}
</script>

<style scoped>

</style>

