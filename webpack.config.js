var path = require('path');

module.exports = {
  entry: './build/index.js',
  output: {
    path: __dirname + '/algocoin/ui/assets/static/js/',
    filename: 'bundle.js',
    publicPath: './static/js/'
  },
  module: {
    rules: [
      { test: /\.css$/, use: ['style-loader', 'css-loader'] },
      { test: /\.png$/, use: 'file-loader' }
    ]
  }
};