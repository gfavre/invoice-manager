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
  transpileDependencies: true
})
