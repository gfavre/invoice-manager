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
  indexPath: path.resolve(__dirname, '../templates/', 'clients_app', 'index.html'),
  outputDir: path.resolve(__dirname, '../static/', 'clients_app'),
  publicPath: process.env.VUE_APP_STATIC_URL,

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
