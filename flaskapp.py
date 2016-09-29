from flask import Flask, send_from_directory
from models import db

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')
db.init_app(app)

from controllers import ContactController, OrgController

# Init API
app.register_blueprint(ContactController, url_prefix='/api/contacts')
app.register_blueprint(OrgController, url_prefix='/api/organisations')

@app.route('/')
def serve_angular_app():
    '''
    Serves the AngularJS application which is configured
    not to use Html5Mode 
    '''
    return send_from_directory('static/', 'index.html')

@app.route('/static/<path:resource>')
def serve_static_resource(resource):
    '''
    All other static resources
    '''
    return send_from_directory('static/', resource)


if __name__ == '__main__':
    app.run()
