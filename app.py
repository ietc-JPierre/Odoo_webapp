from flask import Flask
from controllers.home_controller import home_bp
from controllers.order_controller import order_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "change-me"  
    app.register_blueprint(home_bp)
    
   
    app.register_blueprint(order_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)