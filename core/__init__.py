from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

def create_app():
    # Crear aplicación de flask
    app = Flask(__name__)

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'smavodev@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ayceqokurfikkfgx'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    mail.init_app(app)

    app.config.from_object('config.Config')
    db.init_app(app)

    from flask_ckeditor import CKEditor
    ckeditor = CKEditor(app)

    import locale
    locale.setlocale(locale.LC_ALL, 'es_ES')

    # Manejo de error 404: página no encontrada
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    # Manejo de error 500: error interno del servidor
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('500.html'), 500

    # Registrar vistas
    from core import home
    app.register_blueprint(home.bp)

    from core import auth
    app.register_blueprint(auth.bp)

    from core import posts
    app.register_blueprint(posts.bp)

    from .models import User, Post

    with app.app_context():
        db.create_all()

    return app

