// In your Vue project's webpack.config.js file
const HtmlWebpackPlugin = require('html-webpack-plugin')
module.exports = {
  // ... other webpack options ...
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
      inject: true, // Do not inject anything into <head>
    }),
  ],
}
