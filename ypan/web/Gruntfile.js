var paths = {

  js_src:   'development/javascripts/',
  js_dest:  'assets/javascripts/',

  css_src:  'development/stylesheets/',
  css_dest: 'assets/stylesheets/'
}

module.exports = function(grunt) {

  /*  Load tasks  */
  require('load-grunt-tasks')(grunt);

  /*  Configure project  */

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    clean: {
      main:{
          options:{
              force:true
          },
          src:[
              paths.js_dest,
              paths.css_dest
          ]
      }
    },
    // Setup tasks
    coffee:   require('./tasks/coffee')(paths.js_src),
    concat:   require('./tasks/concat')(paths.js_src, paths.js_dest),
    uglify:   require('./tasks/uglify')(paths.js_dest),
    less:     require('./tasks/less')(paths.css_src, paths.css_dest),
    cssmin:   require('./tasks/cssmin')(paths.css_dest),
    watch:    require('./tasks/watch')(paths.js_src, paths.css_src)

  });

    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-copy');

  /*  Register tasks  */
  
  // Default task.
  grunt.registerTask('default', ['clean','coffee:compile', 'concat:build', 'uglify:minify', 'less:build', 'cssmin:minify']);

  grunt.registerTask('build-project-sass', ['coffee:compile', 'concat:build', 'uglify:minify','cssmin:minify']);

  grunt.registerTask('compile-less', ['less:build', 'cssmin:minify']);

  grunt.registerTask('compile-js', ['coffee:compile', 'concat:build', 'uglify:minify']);
  grunt.registerTask('dev',['watch']);
};
