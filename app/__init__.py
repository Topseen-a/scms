from flask import Flask
from app.database import db

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:tope@localhost/student_course_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes.user_route import user_bp
    from app.routes.course_route import course_bp

    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(course_bp, url_prefix="/api/course")

    return app