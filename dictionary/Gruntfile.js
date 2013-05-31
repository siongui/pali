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
        src: ['common/app/scripts/services/data/dicBooks.js',
              'common/app/scripts/services/data/succinctTrie.js',
              'common/app/scripts/services/data/i18nStrings.js',
              'app/js/app.js',
              'app/js/controllers.js',
              'app/js/directives-event.js',
              'app/js/directives.js',
              'common/app/scripts/services/paliWordJson.js',
              'common/app/scripts/services/shortExp.js',
              'common/app/scripts/services/ngBits.js',
              'common/app/scripts/services/wordSearch.js',
              'common/app/scripts/directives/dropdown.js',
              'common/app/scripts/filters/expOrder.js',
              'common/app/scripts/i18n.js'],
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
    cssmin: {
      combine: {
        files: {
          'app/css/app.min.css': ['app/css/app.css']
        }
      }
    },
    watch: {
      scripts: {
        files: ['<%= concat.dist.src %>'],
        tasks: ['concat', 'uglify']
      },
      styles: {
        files: ['app/css/app.css'],
        tasks: ['cssmin']
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

  grunt.registerTask('update', 'Upload to App Engine.', function() {
    var spawn = require('child_process').spawn;
    var PIPE = { stdio: 'inherit' };
    var done = this.async();
    var command = '../../google_appengine/appcfg.py';
    var args = ['update', '.']
    spawn(command, args, PIPE).on('exit', function(status) {
      done(status === 0);
    });
  });

  // Load the plugins.
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-watch');

  // Default task(s).
  grunt.registerTask('default', ['concat', 'uglify', 'cssmin', 'watch']);

};
