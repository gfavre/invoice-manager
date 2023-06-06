<template>
  <div class="form-group">
    <label>{{ label }}</label>
    <div class="custom-file">
      <input type="file" class="custom-file-input" @change="onFileChange" id="customFile">
      <label class="custom-file-label" for="customFile">{{ $t('Choose file') }}</label>
    </div>

  </div>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      default: 'Upload File'
    }
  },
  methods: {
    onFileChange(e) {
      let files = e.target.files;
      if (files.length > 0){
        this.$emit('input', files);
      }
    }
  }
};
</script>

<style scoped>
</style>
