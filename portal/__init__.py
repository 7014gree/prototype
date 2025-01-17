import os

from flask import Flask, render_template, flash, session

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'portal.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route('/wip')
    def wip():
        return render_template('wip.html')

    from . import db
    db.init_app(app)


    from . import auth
    app.register_blueprint(auth.bp)


    from . import jobs
    app.register_blueprint(jobs.bp)
    # app.add_url_rule('/', endpoint='index')

    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    from . import reports
    app.register_blueprint(reports.bp)

    from . import adjustments
    app.register_blueprint(adjustments.bp)

    from . import settings
    app.register_blueprint(settings.bp)

    from . import admin
    app.register_blueprint(admin.bp)
    
    return app

