'use strict';

module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    concat: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      dist: {
        src: ['common/app/js/services-dicPrefix.js',
              'common/app/js/services-i18nStrings.js',
              'app/js/treeviewAllJson-service.js',
              'app/js/data-i18nTpk-service.js',
              'app/js/i18nTpk-services.js',
              'app/js/app.js',
              'app/js/controllers.js',
              'app/js/directives.js',
              'app/js/services.js',
              'app/js/services-tooltip.js',
              'common/app/js/directives.js',
              'common/app/js/services-jqlext.js',
              'common/app/js/filters.js',
              'common/app/js/services-dic.js',
              'common/app/js/services.js',
              'common/app/js/i18n.js',
              'common/app/js/directive-dropdown.js',
              'common/app/js/ext/tongwen_core.js',
              'common/app/js/ext/tongwen_table_s2t.js',
              'common/app/js/ext/tongwen_table_t2s.js',
              'common/app/js/ext/tongwen_table_ps2t.js',
              'common/app/js/ext/tongwen_table_pt2s.js'],
        dest: 'build/<%= pkg.name %>.js'
      }
    },
    uglify: {
      options: {
        // the banner is inserted at the top of the output
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("dd-mm-yyyy") %> */\n'
      },
      dist: {
        files: {
          //'build/<%= pkg.name %>.min.js': ['<%= concat.dist.dest %>']
          'app/all_compiled.js': ['<%= concat.dist.dest %>']
        }
      }
    },
    watch: {
      scripts: {
        files: ['<%= concat.dist.src %>'],
        tasks: ['concat', 'uglify']
      }
    }
  });

  // Google App Engine server with Grunt
  // @see http://stackoverflow.com/questions/15014127/yeoman-to-use-google-app-engine-server
  grunt.registerTask('run', 'Run app server.', function() {
    var spawn = require('child_process').spawn;
    var PIPE = { stdio: 'inherit' };
    var done = this.async();
    var command = '../../google_appengine/dev_appserver.py';
    var args = ['--datastore_path=GAEDevDatastore', '.']
    spawn(command, args, PIPE).on('exit', function(status) {
      done(status === 0);
    });
  });

  // Load the plugins.
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');

  // Default task(s).
  grunt.registerTask('default', ['concat', 'uglify', 'watch']);

};
