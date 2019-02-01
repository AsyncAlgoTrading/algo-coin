const path = require("path");
const PerspectivePlugin = require("@jpmorganchase/perspective/webpack-plugin");
const webpack = require("webpack");

module.exports = {
    entry: './build/index.js',
    output: {
        path: __dirname + '/algocoin/assets/static/js/',
        filename: 'bundle.js',
        publicPath: './static/js/'
    },
    // resolveLoader: {
    //     alias: {
    //         "file-worker-loader": "@jpmorganchase/perspective-webpack-plugin/src/js/file_worker_loader.js"
    //     }
    // },
    // resolve: {
    //     extensions: [".ts", ".js", ".json"]
    // },
    plugins: [new webpack.ContextReplacementPlugin(/moment[\/\\]locale$/, /(en|es|fr)$/), new PerspectivePlugin()],
    module: {
        rules: [
            {test: /\.css$/, use: [{loader: 'style-loader', }, {loader: 'css-loader', }, ], },
            {test: /\.ts?$/, loader: "ts-loader"}
        ]
    }
};
