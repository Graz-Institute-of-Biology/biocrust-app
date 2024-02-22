const { defineConfig } = require('@vue/cli-service')

// if PRODUCTION (neded on server)
// module.exports = { 
//   publicPath: ''
// }

// if DEVELOPMENT
module.exports = defineConfig({
  transpileDependencies: true
})
