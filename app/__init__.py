from flask import Flask

# application factory function - allows us to set configurations as well as define routes for application
# wraps application object and returns it ultimately allows for different configs to be loaded for differnet
# purposes e.g. testing/production

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    from .views.archive import archive
    app.register_blueprint(archive)

    from .views.defaults import defaults
    app.register_blueprint(defaults)

    from .views.help import help
    app.register_blueprint(help)

    from .views.inputs import inputs
    app.register_blueprint(inputs)

    from .views.outputs import outputs
    app.register_blueprint(outputs)

    from .views.standards import standards
    app.register_blueprint(standards)

    from .views.nrfa import nrfa
    app.register_blueprint(nrfa)

    return app
