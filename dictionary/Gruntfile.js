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
              'app/js/app.js',
              'app/js/controllers.js',
              'app/js/directives-event.js',
              'app/js/directives.js',
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
        dest: 'app/<%= pkg.name %>-all.js'
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

  // Load the plugin that provides the "concat" task.
  grunt.loadNpmTasks('grunt-contrib-concat');

  // Default task(s).
  grunt.registerTask('default', ['concat']);

};
