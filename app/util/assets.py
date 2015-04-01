from flask.ext.assets import Bundle, Environment
from .. import app

bundles = {
    'app_js': Bundle('js/lib/modernizr-2.7.1.min.js',
                     'js/lib/less-1.5.0.min.js', 'js/lib/jquery-1.10.2.min.js',
                     'js/lib/plugins.js', 'js/lib/H5F.js', 'js/functions.js',
                     output='gen/app.js',
                     filters='jsmin'),
    'app_css': Bundle('css/lib/normalize.css',
                      output='gen/app.css',
                      filters='cssmin'),
}

assets = Environment(app)
assets.register(bundles)
