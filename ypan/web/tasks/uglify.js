module.exports = function (js_dest) {
  return {
    minify: {
      files: [
          //压缩javascripts下每个库的JS文件
          {
              expand: true,
              cwd:js_dest,
              src:['**/**/*.js'],
              dest:js_dest,
              ext:'.min.js'
          }

      ]
    }
  }
}
