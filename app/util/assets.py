from flask.ext.assets import Bundle, Environment
from .. import app

bundles = {
    'app_js': Bundle('js/lib/modernizr-2.7.1.min.js',
                     'js/lib/jquery-1.10.2.min.js',
                     'js/lib/picker.js', 'js/lib/picker.date.js',
                     'js/lib/plugins.js', 'js/lib/H5F.js', 'js/functions.js',
                     output='gen/app.js',)
}

assets = Environment(app)
assets.register(bundles)
