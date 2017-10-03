var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

const config = {
  context: __dirname,

  entry: './src/build.js', // entry point of our app. src/build.js should require other js modules and dependencies it needs

  output: {
      path: path.resolve('../assets/bundles/'),
      filename: "NKCUP.js",
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
  ],

  module: {
    rules: [
      { test: /\.jsx?$/, exclude: /node_modules/, use: 'babel-loader'}, // to transform JSX into JS
    ],
  },
}

module.exports = config;