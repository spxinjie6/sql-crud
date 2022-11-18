from flask_sqlalchemy import SQLAlchemy


def init(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:hAv6at_7@172.x.x.x:3306/demo"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config['SQLALCHEMY_ECHO'] = True
    db = SQLAlchemy(app)
    db.init_app(app)
