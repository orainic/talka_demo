module.exports = {
  chainWebpack: config => {
    // 完全删除 copy-webpack-plugin 插件，避免 index.html 冲突
    config.plugins.delete('copy');
  }
};