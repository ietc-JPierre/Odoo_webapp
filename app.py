from flask import Flask
from controllers.home_controller import home_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "change-me"  # nécessaire pour flash()
    app.register_blueprint(home_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)