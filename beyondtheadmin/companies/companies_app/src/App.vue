<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <CompanyForm />
</template>

<script>
import CompanyForm from './components/CompanyForm.vue'

export default {
  name: 'App',
  components: {
    CompanyForm
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
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
