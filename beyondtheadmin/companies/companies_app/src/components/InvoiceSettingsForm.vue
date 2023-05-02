<template>
  <div id="div_id_logo" class="form-group">
    <label for="id_logo">Logo</label>
    <div class="mb-2">
      <div class="form-control custom-file" style="border: 0px;">
        <input type="file" name="logo" accept="image/*" id="id_logo" class="custom-file-input">
        <label for="id_logo" class="custom-file-label text-truncate">---</label>
      </div>
    </div>
  </div>

  <div id="div_id_contrast_color" class="form-group">
    <label for="id_contrast_color" class="requiredField">
      Couleur de contraste<span class="asteriskField">*</span>
    </label>
    <input type="text" id="id_contrast_color" name="contrast_color" value="#3B4451" placeholder="#3B4451"
                data-jscolor="{hash:true,width:225,height:150,format:'hex',required:true,paletteCols:4,paletteHeight:28,palette:[]}"
                required="required" class="form-control colorfield_field jscolor">
  </div>

  <div id="div_id_invoice_note" class="form-group">
    <label for="id_invoice_note">Remarques</label>
    <div>
      <div data-field-id="id_invoice_note" class="django-ckeditor-widget" style="display: inline-block;"><textarea
          cols="40" id="id_invoice_note" name="invoice_note" rows="10" data-processed="0"
          data-config="{&quot;skin&quot;: &quot;moono-lisa&quot;, &quot;toolbar_Basic&quot;: [[&quot;Source&quot;, &quot;-&quot;, &quot;Bold&quot;, &quot;Italic&quot;]], &quot;toolbar_Full&quot;: [[&quot;Styles&quot;, &quot;Format&quot;, &quot;Bold&quot;, &quot;Italic&quot;, &quot;Underline&quot;, &quot;Strike&quot;, &quot;SpellChecker&quot;, &quot;Undo&quot;, &quot;Redo&quot;], [&quot;Link&quot;, &quot;Unlink&quot;, &quot;Anchor&quot;], [&quot;Image&quot;, &quot;Flash&quot;, &quot;Table&quot;, &quot;HorizontalRule&quot;], [&quot;TextColor&quot;, &quot;BGColor&quot;], [&quot;Smiley&quot;, &quot;SpecialChar&quot;], [&quot;Source&quot;]], &quot;toolbar&quot;: &quot;Full&quot;, &quot;height&quot;: 291, &quot;width&quot;: 835, &quot;filebrowserWindowWidth&quot;: 940, &quot;filebrowserWindowHeight&quot;: 725, &quot;language&quot;: &quot;fr&quot;}"
          data-external-plugin-resources="[]" data-id="id_invoice_note" data-type="ckeditortype"
          class="ckeditorwidget form-control"></textarea></div>
      <small id="hint_id_invoice_note" class="form-text text-muted">Affiché entre les coordonnées bancaires et la
        signature</small></div>
  </div>

  <div id="div_id_signature_text" class="form-group">
    <label for="id_signature_text">Signature sous forme de texte</label>
    <input type="text" name="signature_text" maxlength="100" id="id_signature_text"
                class="textinput textInput form-control">
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

  <div id="div_id_thanks" class="form-group">
    <label for="id_thanks">Merci</label>
    <textarea name="thanks" cols="40" rows="10" id="id_thanks" class="textarea form-control"></textarea>
    <small id="hint_id_thanks" class="form-text text-muted">
      Remerciements au bas de la facture. Si cette option est activée, elle figurera sur toutes les factures,
      quelle que soit la langue
    </small>
  </div>

  <div class="buttonHolder">
    <input type="button" name="prev-3" value="Précédent" class="btn btn btn-secondary white">
    <input type="submit" value="Enregistrer" disabled="disabled" class="btn btn btn-primary white">
  </div>

</template>

<script>
export default {
  name: "InvoiceSettingsForm",
  props: ['company'],
}
</script>

<style scoped>

</style>
