const withCSS = require('@zeit/next-css')
const Dotenv = require('dotenv-webpack');

module.exports = withCSS({
  exportPathMap: function(defaultPathMap) {
    return {
      '/': { page: '/' }
    }
  },
  webpack: config => {
    config.plugins = config.plugins || []

    config.plugins = [
      ...config.plugins,

      // Read the .env file
      new Dotenv({
        path: '../.env',
        systemvars: true
      })
    ]

    return config
  }
})
