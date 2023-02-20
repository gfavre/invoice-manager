const { defineConfig } = require('@vue/cli-service')
const path = require('path');

module.exports = defineConfig({
  configureWebpack: {
    resolve: {
      alias: {
        '@shared': path.join( __dirname, '../_shared' ),
      }
    }
  },

  transpileDependencies: true,

  pluginOptions: {
    i18n: {
      locale: 'en',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableLegacy: false,
      runtimeOnly: false,
      compositionOnly: false,
      fullInstall: true
    }
  }
})
