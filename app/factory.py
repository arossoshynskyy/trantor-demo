from connexion import FlaskApp


def create_app(package_name):
    app = FlaskApp(__name__, specification_dir='./')
    app.add_api('openapi.yaml')
    
    return app
