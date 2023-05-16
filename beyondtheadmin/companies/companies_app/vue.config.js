const { defineConfig } = require('@vue/cli-service')
const path = require('path');


module.exports = defineConfig({
  filenameHashing: false,
  configureWebpack: {
    resolve: {
      alias: {
        '@shared': path.join( __dirname, '../_shared' ),
      }
    },
  },
  chainWebpack: config => {
    config.plugins.delete('html')
  },

  indexPath: path.resolve(__dirname, '../templates/', 'companies_app', 'index.html'),
  outputDir: path.resolve(__dirname, '../static/', 'companies_app'),
  publicPath: process.env.VUE_APP_STATIC_URL,

  // transpileDependencies: true,

  pluginOptions: {
    i18n: {
      locale: 'fr',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableLegacy: false,
      runtimeOnly: false,
      compositionOnly: false,
      fullInstall: true
    }
  }
})
